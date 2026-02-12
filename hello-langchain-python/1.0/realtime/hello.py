#!/usr/bin/env python3
# Requirements: pip install websocket-client pyaudio

"""
Qwen-Omni-Realtime Client
Real-time audio conversation with AI using WebSocket
"""

import json
import websocket
import pyaudio
import base64
import os
import uuid
import threading
import time


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
            # Suppress ALSA warnings
            import os
            os.environ['ALSA_CARD'] = 'default'
            
            self.output_stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                output=True,
                frames_per_buffer=1024
            )
            print("Audio output ready\n")
        except Exception as e:
            print(f"Audio output initialization failed: {e}")
            print("Continuing without audio output...\n")
    
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
            print("\nAI speaking, recording paused...")
    
    def resume_recording(self):
        """Resume recording after AI finishes (with delay)"""
        if self.ai_is_speaking:
            self.ai_stop_time = time.time()
            print(f"\nAI finished, resuming in {self.resumption_delay}s...")
    
    def check_resume_recording(self):
        """Check if recording should resume"""
        if self.ai_is_speaking and self.ai_stop_time > 0:
            elapsed = time.time() - self.ai_stop_time
            if elapsed >= self.resumption_delay:
                self.ai_is_speaking = False
                self.stop_recording = False
                self.ai_stop_time = 0
                print("\nRecording resumed, please speak...\n")
    
    def on_open(self, ws):
        """WebSocket connection opened"""
        self.is_connected = True
        print("Connected to Qwen-Omni-Realtime\n")
        
        # Send session configuration
        ws.send(json.dumps(self.create_session_config()))
        
        print("=" * 60)
        print(f"Voice: {self.voice}")
        print("Please start speaking...")
        print("Press Ctrl+C to exit")
        print("=" * 60)
        
        self.init_audio_output()
        self.is_running = True
        self.start_recording()
    
    def on_message(self, ws, message):
        """Handle WebSocket messages"""
        try:
            data = json.loads(message)
            event_type = data.get("type")
            
            if event_type == "input_audio_buffer.speech_started":
                if not self.ai_is_speaking:
                    print("\nRecording...")
            
            elif event_type == "conversation.item.created":
                item = data.get("item", {})
                if item.get("role") == "user":
                    content_list = item.get("content", [])
                    if content_list and isinstance(content_list[0], dict):
                        transcript = content_list[0].get("transcript", "")
                        if transcript:
                            print(f"\n{'=' * 60}")
                            print(f"You: {transcript}")
                            print(f"{'=' * 60}")
                            print("AI: ", end="", flush=True)
            
            elif event_type == "response.created":
                self.pause_recording()
            
            elif event_type == "response.audio_transcript.delta":
                text = data.get("delta", "")
                if text:
                    print(text, end="", flush=True)
            
            elif event_type == "response.audio.delta":
                audio_delta = data.get("delta", "")
                if audio_delta and self.output_stream:
                    try:
                        audio_data = base64.b64decode(audio_delta)
                        self.output_stream.write(audio_data)
                    except:
                        pass
            
            elif event_type == "response.done":
                print()
                self.resume_recording()
                print(f"{'=' * 60}\n")
            
            elif event_type == "error":
                error = data.get("error", {})
                print(f"\nError: {error.get('message', 'Unknown error')}")
        
        except Exception:
            pass
    
    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"\nConnection error: {error}")
    
    def on_close(self, ws, *args):
        """WebSocket connection closed"""
        print("\nConnection closed")
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
                            "audio": audio_base64
                        }
                        self.ws.send(json.dumps(msg))
                
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
            print("Recording started\n")
    
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


def create_client(voice: str = "Cherry"):
    """Create realtime client"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    
    return RealtimeClient(api_key, voice)


def main():
    import sys
    
    voice = sys.argv[1] if len(sys.argv) > 1 else "Cherry"
    
    print("\n" + "=" * 60)
    print("Qwen-Omni-Realtime Client")
    print("=" * 60)
    print(f"Voice: {voice}")
    print(f"Strategy: Pause recording during playback")
    
    try:
        client = create_client(voice)
        client.start()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()
