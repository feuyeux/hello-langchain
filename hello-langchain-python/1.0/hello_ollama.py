from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from tools.agent_middleware import (
    LoggingMiddleware,
    PerformanceMiddleware,
    ThinkCleanerMiddleware,
)
from tools.format_utils import print_section_header, print_content


def main():
    model_name = "qwen3:8b"
    title = "窗外"
    languages = ["英语", "法语", "俄语", "汉语"]

    agent = create_agent(
        model=ChatOllama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
        ),
        system_prompt="你是顶级的短片作家",
        middleware=[
            LoggingMiddleware(),
            PerformanceMiddleware(),
            ThinkCleanerMiddleware(),
        ],
    )


    for lang in languages:
        print_section_header(f"语言: {lang}")
        try:
            prompt_text = f"使用{lang}，请根据{title}的内容，写一篇50字的精品短文"
            result = agent.invoke({"messages": [HumanMessage(content=prompt_text)]})
            final_message = result["messages"][-1]
            
            print_content(final_message.content)
        except Exception as e:
            print(f"❌ 错误: {str(e)}\n")


if __name__ == "__main__":
    main()
