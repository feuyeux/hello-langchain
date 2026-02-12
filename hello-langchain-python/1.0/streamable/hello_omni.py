"""qwen3-omni-flash 多模态示例（Text/Image → Text + Audio）

通过 DashScope OpenAI 兼容接口，展示上行请求与下行流式响应的完整数据。
  Demo 1: 纯文本 → 文本 + 语音
  Demo 2: 图片 + 文本 → 文本 + 语音
"""

# Requirements: pip install numpy soundfile openai python-dotenv

from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import numpy as np
import soundfile as sf
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── 配置 ──────────────────────────────────────────────────────
MODEL = "qwen3-omni-flash"
OUTPUT_DIR = Path(__file__).resolve().parent / "omni_output"


def fmt(data) -> str:
    """Pretty-print JSON（截断 base64 避免刷屏）。"""
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def create_client() -> OpenAI:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
    return OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


def save_audio(audio_b64: str, path: Path, sample_rate: int = 24000) -> None:
    wav_bytes = base64.b64decode(audio_b64)
    audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    sf.write(str(path), audio_np, samplerate=sample_rate)


# ── 核心：带上下行日志的流式请求 ─────────────────────────────
def stream_completion(
    client: OpenAI,
    messages: list[dict],
    *,
    audio_file: str | None = None,
) -> None:
    """发送请求并打印上行/下行数据。"""

    # ── 上行 ──────────────────────────────────────────────────
    request_body = {
        "model": MODEL,
        "messages": messages,
        "modalities": ["text", "audio"],
        "audio": {"voice": "Cherry", "format": "wav"},
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    print("\n[上行请求]")
    # 打印时截断图片 URL 避免过长
    print(fmt(request_body))

    completion = client.chat.completions.create(**request_body)

    # ── 下行 ──────────────────────────────────────────────────
    print("\n[下行响应 - 流式 chunks]")
    text_parts: list[str] = []
    audio_b64_parts: list[str] = []
    chunk_count = 0
    usage_info = None

    for chunk in completion:
        chunk_count += 1
        delta = chunk.choices[0].delta if chunk.choices else None

        # 文本
        if delta and delta.content:
            text_parts.append(delta.content)
            print(delta.content, end="", flush=True)

        # 音频（只记录长度，不打印 base64）
        if delta and hasattr(delta, "audio") and delta.audio:
            audio_data = delta.audio.get("data", "")
            if audio_data:
                audio_b64_parts.append(audio_data)

        # usage（最后一个 chunk）
        if chunk.usage:
            usage_info = chunk.usage

    print()  # 换行

    # ── 下行汇总 ──────────────────────────────────────────────
    full_text = "".join(text_parts)
    full_audio_b64 = "".join(audio_b64_parts)

    print(f"\n[下行汇总]")
    print(f"  chunks 数量  : {chunk_count}")
    print(f"  文本内容     : {full_text}")
    if full_audio_b64:
        audio_bytes = len(base64.b64decode(full_audio_b64))
        duration_s = audio_bytes / 2 / 24000  # int16 @ 24kHz
        print(f"  音频大小     : {audio_bytes:,} bytes ({duration_s:.1f}s @ 24kHz)")
    else:
        print(f"  音频         : 无")
    if usage_info:
        print(f"  token 用量   : prompt={usage_info.prompt_tokens}, "
              f"completion={usage_info.completion_tokens}, "
              f"total={usage_info.total_tokens}")

    # ── 保存音频 ──────────────────────────────────────────────
    if full_audio_b64 and audio_file:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / audio_file
        save_audio(full_audio_b64, out_path)
        print(f"  音频已保存   : {out_path}")


# ── Demo 1: 纯文本 → 文本 + 语音 ─────────────────────────────
def demo_text():
    print("=" * 60)
    print("Demo 1: Text → Text + Audio")
    print("=" * 60)

    client = create_client()
    messages = [{"role": "user", "content": "你是谁"}]
    stream_completion(client, messages, audio_file="demo1_text.wav")


# ── Demo 2: 图片 + 文本 → 文本 + 语音 ────────────────────────
def demo_image():
    print()
    print("=" * 60)
    print("Demo 2: Image + Text → Text + Audio")
    print("=" * 60)

    IMAGE_URL = (
        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files"
        "/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
    )
    client = create_client()
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": IMAGE_URL}},
                {"type": "text", "text": "图中描绘的是什么景象？请简要描述"},
            ],
        }
    ]
    stream_completion(client, messages, audio_file="demo2_image.wav")


def main():
    demo_text()
    demo_image()


if __name__ == "__main__":
    main()
