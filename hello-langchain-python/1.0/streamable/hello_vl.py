"""qwen3-vl-plus 视觉语言理解示例（Image + Text → Text）

通过 DashScope OpenAI 兼容接口，展示上行请求与下行响应的完整数据。
  Demo 1: 流式输出（stream=True）
  Demo 2: 非流式输出（stream=False）
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# ── 配置 ──────────────────────────────────────────────────────
MODEL = "qwen3-vl-plus"
IMAGE_URL = (
    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files"
    "/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
)
QUESTION = "图中描绘的是什么景象？请简要描述"


def fmt(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


def create_client() -> OpenAI:
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量")
    return OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


def build_messages(image_url: str, text: str) -> list[dict]:
    return [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": text},
            ],
        }
    ]


# ── Demo 1: 流式 ─────────────────────────────────────────────
def demo_streaming():
    print("=" * 60)
    print("Demo 1: 流式输出（stream=True）")
    print("=" * 60)

    client = create_client()
    messages = build_messages(IMAGE_URL, QUESTION)

    request_body = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "stream_options": {"include_usage": True},
    }

    # ── 上行 ──
    print("\n[上行请求]")
    print(fmt(request_body))

    stream = client.chat.completions.create(**request_body)

    # ── 下行 ──
    print("\n[下行响应 - 流式 chunks]")
    text_parts: list[str] = []
    chunk_count = 0
    usage_info = None

    for chunk in stream:
        chunk_count += 1
        delta = chunk.choices[0].delta if chunk.choices else None

        if delta and delta.content:
            text_parts.append(delta.content)
            print(delta.content, end="", flush=True)

        if chunk.usage:
            usage_info = chunk.usage

    print()

    # ── 汇总 ──
    print(f"\n[下行汇总]")
    print(f"  chunks 数量  : {chunk_count}")
    print(f"  文本内容     : {''.join(text_parts)}")
    if usage_info:
        print(f"  token 用量   : prompt={usage_info.prompt_tokens}, "
              f"completion={usage_info.completion_tokens}, "
              f"total={usage_info.total_tokens}")


# ── Demo 2: 非流式 ───────────────────────────────────────────
def demo_normal():
    print()
    print("=" * 60)
    print("Demo 2: 非流式输出（stream=False）")
    print("=" * 60)

    client = create_client()
    messages = build_messages(IMAGE_URL, QUESTION)

    request_body = {
        "model": MODEL,
        "messages": messages,
    }

    # ── 上行 ──
    print("\n[上行请求]")
    print(fmt(request_body))

    completion = client.chat.completions.create(**request_body)

    # ── 下行 ──
    print("\n[下行响应]")
    choice = completion.choices[0]
    print(f"  finish_reason: {choice.finish_reason}")
    print(f"  文本内容     : {choice.message.content}")
    if completion.usage:
        print(f"  token 用量   : prompt={completion.usage.prompt_tokens}, "
              f"completion={completion.usage.completion_tokens}, "
              f"total={completion.usage.total_tokens}")


def main():
    demo_streaming()
    demo_normal()


if __name__ == "__main__":
    main()
