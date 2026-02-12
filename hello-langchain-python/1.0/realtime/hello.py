#!/usr/bin/env python3
"""qwen3-omni-flash-realtime WebSocket 实时语音对话示例

通过 DashScope Realtime API（WebSocket），展示上行/下行消息的完整数据流：
  上行: session.update / input_audio_buffer.append
  下行: response.audio.delta / response.audio_transcript.delta / response.done 等

使用方式: uv run realtime/hello.py [voice]
  voice: Cherry(默认) / Serena / Ethan 等
  按 Ctrl+C 退出
"""

# Requirements: pip install websocket-client pyaudio python-dotenv

from __future__ import annotations

import base64
import json
import os
import threading
import time
import uuid
from pathlib import Path

import pyaudio
import websocket
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── 日志工具 ──────────────────────────────────────────────────
def fmt_event(data: dict, *, max_audio_len: int = 40) -> str:
    """格式化事件 JSON，截断 base64 音频数据避免刷屏。"""
    d = dict(data)
    # 截断上行音频
    if "audio" in d and isinstance(d["audio"], str) and len(d["audio"]) > max_audio_len:
        d["audio"] = d["audio"][:max_audio_len] + f"...({len(data['audio'])} chars)"
    # 截断下行音频
    if "delta" in d and isinstance(d["delta"], str) and len(d["delta"]) > max_audio_len:
        d["delta"] = d["delta"][:max_audio_len] + f"...({len(data['delta'])} chars)"
    return json.dumps(d, ensure_ascii=False, indent=2)


class RealtimeClient:
    """WebSocket client for Qwen-Omni-Realtime API"""
    
    # Audio configuration
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 24000
    CHUNK = 960
    
    def __init__(self, api_key: str, voice: str = "Cherry"):
        self.api_key = api_key
        self.voice = voice
        self.api_url = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-omni-flash-realtime"
        
        # State management
        self.is_running = False
        self.is_connected = False
        self.ai_is_speaking = False
        self.stop_recording = False
        self.ai_stop_time = 0
        self.resumption_delay = 0.9
        
        # 统计
        self.audio_chunks_sent = 0
        self.audio_chunks_recv = 0
        self.turn_count = 0
        
        # Audio streams
        self.audio = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        
        # WebSocket and threading
        self.ws = None
        self.recording_thread = None
    
    def generate_event_id(self) -> str:
        """Generate unique event ID"""
        return str(uuid.uuid4())
    
    def create_session_config(self) -> dict:
        """Create session configuration"""
        return {
            "event_id": self.generate_event_id(),
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": self.voice,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "instructions": "你是一个友好的AI助手，请简洁自然地回答。",
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "silence_duration_ms": 800
                }
            }
        }
    
    def init_audio_output(self):
        """Initialize audio output stream"""
        try:
            self.output_stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=1024,
            )
            print("[音频] 输出设备就绪\n")
        except Exception as e:
            print(f"[音频] 输出设备初始化失败: {e}")
            print("  继续运行（无音频播放）…\n")
    
    def init_audio_input(self):
        """Initialize audio input stream"""
        try:
            self.input_stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK,
                input_device_index=None  # Use default device
            )
        except Exception as e:
            print(f"Audio input initialization failed: {e}")
            raise
    
    def pause_recording(self):
        """Pause recording when AI is speaking"""
        if not self.ai_is_speaking:
            self.ai_is_speaking = True
            self.stop_recording = True
            print("\n[录音] AI 说话中，暂停录音…")
    
    def resume_recording(self):
        """Resume recording after AI finishes (with delay)"""
        if self.ai_is_speaking:
            self.ai_stop_time = time.time()
            print(f"[录音] AI 结束, {self.resumption_delay}s 后恢复录音…")
    
    def check_resume_recording(self):
        """Check if recording should resume"""
        if self.ai_is_speaking and self.ai_stop_time > 0:
            elapsed = time.time() - self.ai_stop_time
            if elapsed >= self.resumption_delay:
                self.ai_is_speaking = False
                self.stop_recording = False
                self.ai_stop_time = 0
                print("\n[录音] 已恢复，请说话…\n")
    
    def on_open(self, ws):
        """WebSocket connection opened"""
        self.is_connected = True
        print("[连接] 已连接 Qwen-Omni-Realtime\n")
        
        # Send session configuration
        config = self.create_session_config()
        print("[上行] session.update")
        print(fmt_event(config))
        ws.send(json.dumps(config))
        
        print()
        print("=" * 60)
        print(f"语音角色: {self.voice}")
        print("请开始说话… 按 Ctrl+C 退出")
        print("=" * 60)
        
        self.init_audio_output()
        self.is_running = True
        self.start_recording()
    
    def on_message(self, ws, message):
        """Handle WebSocket messages — 打印所有下行事件"""
        try:
            data = json.loads(message)
            event_type = data.get("type", "")

            # 音频数据 chunk 只计数，不逐条打印
            if event_type == "response.audio.delta":
                self.audio_chunks_recv += 1
                audio_delta = data.get("delta", "")
                if audio_delta and self.output_stream:
                    try:
                        self.output_stream.write(base64.b64decode(audio_delta))
                    except Exception:
                        pass
                return

            # 文本 transcript delta — 实时打印文字
            if event_type == "response.audio_transcript.delta":
                text = data.get("delta", "")
                if text:
                    print(text, end="", flush=True)
                return

            # 其余事件完整打印
            print(f"\n[下行] {event_type}")
            print(fmt_event(data))

            if event_type == "input_audio_buffer.speech_started":
                if not self.ai_is_speaking:
                    print("  → 检测到用户语音…")
            
            elif event_type == "conversation.item.created":
                item = data.get("item", {})
                if item.get("role") == "user":
                    content_list = item.get("content", [])
                    if content_list and isinstance(content_list[0], dict):
                        transcript = content_list[0].get("transcript", "")
                        if transcript:
                            self.turn_count += 1
                            print(f"\n{'=' * 60}")
                            print(f"[Turn {self.turn_count}] 你: {transcript}")
                            print(f"{'=' * 60}")
                            print("AI: ", end="", flush=True)
            
            elif event_type == "response.created":
                self.pause_recording()
            
            elif event_type == "response.done":
                print()
                print(f"  → 音频 chunks 接收: {self.audio_chunks_recv}")
                self.audio_chunks_recv = 0
                self.resume_recording()
                print(f"{'=' * 60}\n")
            
            elif event_type == "session.created":
                print("  → 会话已创建")

            elif event_type == "session.updated":
                print("  → 会话配置已更新")
            
            elif event_type == "error":
                error = data.get("error", {})
                print(f"  → 错误: {error.get('message', 'Unknown error')}")
        
        except Exception:
            pass
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"\n[错误] 连接异常: {error}")
    
    def on_close(self, ws, *args):
        """WebSocket connection closed"""
        print(f"\n[连接] 已断开 (共 {self.turn_count} 轮对话, 上行音频 chunks: {self.audio_chunks_sent})")
        self.is_running = False
        self.is_connected = False
        
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
    
    def record_audio(self):
        """Recording thread - controlled by stop_recording flag"""
        while not self.is_connected:
            time.sleep(0.1)
        
        self.init_audio_input()
        
        try:
            while self.is_running:
                self.check_resume_recording()
                
                if self.stop_recording:
                    time.sleep(0.01)
                    continue
                
                try:
                    data = self.input_stream.read(self.CHUNK, exception_on_overflow=False)
                    
                    if not self.stop_recording and self.is_connected and self.ws and self.ws.sock:
                        audio_base64 = base64.b64encode(data).decode('utf-8')
                        
                        msg = {
                            "event_id": self.generate_event_id(),
                            "type": "input_audio_buffer.append",
                            "audio": audio_base64,
                        }
                        self.ws.send(json.dumps(msg))
                        self.audio_chunks_sent += 1
                
                except Exception:
                    if self.is_running:
                        pass
                    break
        finally:
            if self.input_stream:
                self.input_stream.stop_stream()
                self.input_stream.close()
    
    def start_recording(self):
        """Start recording thread"""
        if self.recording_thread is None or not self.recording_thread.is_alive():
            self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
            self.recording_thread.start()
            print("[录音] 已启动\n")
    
    def start(self):
        """Start WebSocket connection"""
        self.ws = websocket.WebSocketApp(
            self.api_url,
            header={"Authorization": f"Bearer {self.api_key}"},
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        
        self.ws.run_forever()


def create_client(voice: str = "Cherry") -> RealtimeClient:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
    return RealtimeClient(api_key, voice)


def main():
    import sys

    voice = sys.argv[1] if len(sys.argv) > 1 else "Cherry"

    print("\n" + "=" * 60)
    print("Qwen-Omni-Realtime 实时语音对话")
    print("=" * 60)
    print(f"语音角色  : {voice}")
    print(f"录音策略  : AI 说话时暂停录音")
    print(f"上行事件  : session.update / input_audio_buffer.append")
    print(f"下行事件  : response.audio.delta / response.done 等")

    try:
        client = create_client(voice)
        client.start()
    except KeyboardInterrupt:
        print("\n\n再见!")
    except Exception as e:
        print(f"\n错误: {e}")


if __name__ == "__main__":
    main()
