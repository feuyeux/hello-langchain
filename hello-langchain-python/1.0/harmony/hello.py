"""gpt-oss Harmony 协议 tool-call 示例（纯 wire 格式）

全程使用 harmony wire 协议：
  1. 构建 Conversation → 渲染为 wire text（上行）
  2. 通过 Ollama /api/generate (raw) 直接发送 wire text
  3. 用 StreamableParser 解析模型返回的 wire text（下行）
  4. tool-call 闭环：上行 → 下行(tool_call) → 注入结果 → 上行 → 下行(回答)

目标模型: gpt-oss-20b（纯文本：Text → Text）
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

import httpx
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from openai_harmony import (
    Author, Conversation, DeveloperContent, HarmonyEncodingName, Message,
    Role, StreamableParser, SystemContent, ToolDescription,
    load_harmony_encoding,
)

# ── 配置 ──────────────────────────────────────────────────────
OLLAMA_BASE = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("OPENAI_MODEL", "gpt-oss:20b")
QUESTION = "计算 (17 * 23 + 89) / 3.7 的结果，保留两位小数"

encoding = load_harmony_encoding(HarmonyEncodingName.HARMONY_GPT_OSS)
# harmony 停止 token（排除 <|end|> — 它是消息分隔符，不是轮次结束）
# 只保留 <|call|>（tool-call 结束）和 <|return|>（最终回答结束）
END_TOKEN = 200007   # <|end|>  — 消息分隔，模型需继续生成
CALL_TOKEN = 200012  # <|call|> — tool-call 结束
RETURN_TOKEN = 200002  # <|return|> — 完整轮次结束
STOP_STRINGS = [
    encoding.decode_utf8([CALL_TOKEN]),
    encoding.decode_utf8([RETURN_TOKEN]),
]


def fmt(data) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_conversation(
    user_question: str,
    *,
    assistant_messages: list[Message] | None = None,
    tool_result: tuple[str, str] | None = None,
) -> Conversation:
    """构建包含 tool 定义的对话。"""
    msgs: list[Message] = [
        Message.from_role_and_content(
            Role.SYSTEM,
            SystemContent.new().with_conversation_start_date(str(date.today())),
        ),
        Message.from_role_and_content(
            Role.DEVELOPER,
            DeveloperContent.new()
            .with_instructions("Be concise. Use tools when needed.")
            .with_function_tools([
                ToolDescription.new(
                    "calculate", "Evaluate a math expression and return the result.",
                    parameters={
                        "type": "object",
                        "properties": {"expression": {"type": "string", "description": "A Python math expression, e.g. 2**8"}},
                        "required": ["expression"],
                    },
                )
            ]),
        ),
        Message.from_role_and_content(Role.USER, user_question),
    ]
    if assistant_messages:
        msgs.extend(assistant_messages)
    if tool_result:
        tool_name, tool_content = tool_result
        msgs.append(Message.from_author_and_content(
            Author.new(Role.TOOL, tool_name), tool_content,
        ))
    return Conversation.from_messages(msgs)


def complete(prompt_tokens: list[int]) -> tuple[list[Message], str]:
    """发送 wire text → Ollama raw generate → 解析下行 wire。

    Returns: (parsed_messages, raw_wire_text)
    """
    prompt_wire = encoding.decode_utf8(prompt_tokens)

    resp = httpx.post(
        f"{OLLAMA_BASE}/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt_wire,
            "raw": True,          # 不使用 Ollama 模板，直接发送 wire text
            "stream": False,
            "options": {
                "temperature": 0,
                "num_predict": 1024,
                "stop": STOP_STRINGS,
            },
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    raw_text = data["response"]
    done_reason = data.get("done_reason", "")

    # Ollama 会去掉匹配的 stop 字符串，需要补回以便解析器正确关闭消息
    if done_reason == "stop":
        # 判断是 tool-call (<|call|>) 还是最终回答 (<|return|>)
        call_str = encoding.decode_utf8([CALL_TOKEN])
        return_str = encoding.decode_utf8([RETURN_TOKEN])
        # 如果最后一段含 <|constrain|>，说明是 tool-call
        if "<|constrain|>" in raw_text.split("<|end|>")[-1]:
            raw_text += call_str
        else:
            raw_text += return_str

    # 用 StreamableParser 逐 token 解析
    raw_tokens = encoding.encode(raw_text, allowed_special="all")
    parser = StreamableParser(encoding, Role.ASSISTANT)
    for token in raw_tokens:
        parser.process(token)

    return list(parser.messages), raw_text


def main() -> None:
    # ── Round 1: 上行（带 tool 定义的问题）────────────────────
    print("=" * 60)
    print("Round 1: 上行 → Ollama raw → 下行")
    print("=" * 60)

    convo1 = build_conversation(QUESTION)
    prompt1 = encoding.render_conversation_for_completion(convo1, Role.ASSISTANT)

    print(f"\n[上行 wire]\n{encoding.decode_utf8(prompt1)}")
    print("=" * 60)

    messages1, raw1 = complete(prompt1)

    print(f"\n[下行 wire]\n{raw1}")
    print("\n[下行解析]")
    for msg in messages1:
        print(fmt(msg.to_dict()))
    print("=" * 60)
    
    # ── 检查是否触发了 tool call ──────────────────────────────
    tool_call_msg = next(
        (m for m in messages1
         if m.to_dict().get("recipient", "").startswith("functions.")),
        None,
    )
    if not tool_call_msg:
        # 模型直接回答了，展示结果即可
        final = next((m for m in messages1 if m.to_dict().get("channel") == "final"), None)
        if final:
            print(f"\n[最终回答] {final.to_dict()['content'][0]['text']}")
        return

    # ── 解析 tool call 参数 ───────────────────────────────────
    td = tool_call_msg.to_dict()
    tool_name = td["recipient"]  # e.g. "functions.get_current_weather"
    tool_args_raw = td["content"][0]["text"]
    tool_args = json.loads(tool_args_raw)
    print(f"\n[tool call] {tool_name}({fmt(tool_args)})")

    # ── 执行 tool ────────────────────────────────────────────
    expression = tool_args.get("expression", "")
    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as e:
        result = f"Error: {e}"
    tool_result = json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    print(f"[tool result] {tool_result}")

    # ── Round 2: 上行（含 tool 结果）→ 下行（最终回答）────────
    print()
    print("=" * 60)
    print("Round 2: 注入 tool 结果 → 上行 → 下行")
    print("=" * 60)

    convo2 = build_conversation(
        QUESTION,
        assistant_messages=messages1,
        tool_result=(tool_name, tool_result),
    )
    prompt2 = encoding.render_conversation_for_completion(convo2, Role.ASSISTANT)

    print(f"\n[上行 wire]\n{encoding.decode_utf8(prompt2)}")

    messages2, raw2 = complete(prompt2)

    print(f"\n[下行 wire]\n{raw2}")
    print("\n[下行解析]")
    for msg in messages2:
        print(fmt(msg.to_dict()))

    # ── 提取最终回答 ──────────────────────────────────────────
    final = next(
        (m for m in messages2 if m.to_dict().get("channel") == "final"),
        messages2[-1] if messages2 else None,
    )
    if final:
        print(f"\n[最终回答] {final.to_dict()['content'][0]['text']}")


if __name__ == "__main__":
    main()
