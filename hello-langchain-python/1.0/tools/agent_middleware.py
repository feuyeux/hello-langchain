"""
Agent middleware components for logging, performance monitoring, and response cleaning.
"""
from langchain.agents.middleware.types import (
    AgentMiddleware,
    AgentState,
    ModelRequest,
    ModelResponse,
)
from langgraph.runtime import Runtime
from typing import Any
import time
import re


# ============================================
# Middleware 1: 日志记录
# ============================================
class LoggingMiddleware(AgentMiddleware[AgentState, Any]):
    """记录模型调用的详细信息"""

    def __init__(self):
        super().__init__()
        self.call_count = 0

    def before_model(
        self, state: AgentState, runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """模型调用前记录"""
        self.call_count += 1
        messages = state.get("messages", [])
        print(f"\n📞 [Middleware] 模型调用 #{self.call_count}, 消息数: {len(messages)}")
        return None

    def after_model(
        self, state: AgentState, runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """模型调用后记录"""
        messages = state.get("messages", [])
        if messages:
            last_msg = messages[-1]
            content = getattr(last_msg, "content", "")
            if content:
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"✅ [Middleware] 模型响应: {preview}")
        return None


# ============================================
# Middleware 2: 性能监控
# ============================================
class PerformanceMiddleware(AgentMiddleware[AgentState, Any]):
    """监控模型调用性能"""

    def __init__(self):
        super().__init__()
        self.call_times = []

    def wrap_model_call(self, request: ModelRequest, handler: Any) -> ModelResponse:
        """包装模型调用以测量时间"""
        start = time.time()
        response = handler(request)
        elapsed = time.time() - start

        self.call_times.append(elapsed)
        avg_time = sum(self.call_times) / len(self.call_times)
        print(f"⏱️  [Middleware] 耗时: {elapsed:.2f}s, 平均: {avg_time:.2f}s")

        return response



# ============================================
# Middleware 3: 清理思考标签
# ============================================
class ThinkCleanerMiddleware(AgentMiddleware[AgentState, Any]):
    """自动清理模型响应中的 <think> 标签内容"""

    def after_model(
        self, state: AgentState, runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """模型调用后清理 <think> 标签"""
        messages = state.get("messages", [])
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, "content") and isinstance(last_msg.content, str):
                # 移除 <think>...</think> 标签及其内容
                pattern = r"<think>.*?</think>\s*"
                cleaned_content = re.sub(pattern, "", last_msg.content, flags=re.DOTALL)
                # 更新消息内容
                last_msg.content = cleaned_content
        return None
