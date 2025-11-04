from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.agents.middleware.types import AgentMiddleware, AgentState, ModelRequest, ModelResponse
from langchain_core.messages import HumanMessage
from langgraph.runtime import Runtime
from typing import Any
import sys
import time
from hello_utils import clean_think_sections


# ============================================
# Middleware 1: 日志记录
# ============================================
class LoggingMiddleware(AgentMiddleware[AgentState, Any]):
    """记录模型调用的详细信息"""
    
    def __init__(self):
        super().__init__()
        self.call_count = 0
    
    def before_model(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        """模型调用前记录"""
        self.call_count += 1
        messages = state.get("messages", [])
        print(f"\n📞 [Middleware] 模型调用 #{self.call_count}, 消息数: {len(messages)}")
        return None
    
    def after_model(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        """模型调用后记录"""
        messages = state.get("messages", [])
        if messages:
            last_msg = messages[-1]
            content = getattr(last_msg, 'content', '')
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


def main():
    model_name = "qwen3:8b"
    title = "窗外"
    languages = ["英语", "法语", "俄语", "汉语"]
    
    try:
        # 1. 创建 ChatOllama 模型（替换 OllamaLLM）
        llama_model = ChatOllama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
        )
        
        # 2. 创建 Middleware
        middlewares = [
            LoggingMiddleware(),       # 日志记录
            PerformanceMiddleware(),   # 性能监控
        ]
        
        # 3. 创建 Agent（添加 middleware 参数）
        agent = create_agent(
            model=llama_model,
            tools=[],  # 没有工具，只用于文本生成
            system_prompt="你是顶级的短片作家",  # 使用 system_prompt 而不是 state_modifier
            middleware=middlewares,  # ← 添加 middleware 参数
        )
        
        print(f"\n🚀 运行模型: {model_name}")
        print(f"✅ 已配置 {len(middlewares)} 个 middleware")
        
        for lang in languages:
            print(f"\n{'='*60}")
            print(f"===== {lang} =====")
            print(f"{'='*60}")
            
            try:
                # 构建提示
                prompt_text = f"使用{lang}，请根据{title}的内容，写一篇50字的精品短文"
                
                # 调用 Agent
                result = agent.invoke({
                    "messages": [HumanMessage(content=prompt_text)]
                })
                
                # 获取最后的响应
                final_message = result["messages"][-1]
                clean_result = clean_think_sections(final_message.content)
                print(f"\n{clean_result}")
                
            except Exception as e:
                print(f"处理{lang}时出错: {str(e)}")
                
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n程序遇到错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
