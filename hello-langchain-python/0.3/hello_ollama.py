from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import sys
from hello_utils import clean_think_sections

def main():
    template = """你是顶级的短片作家，
    使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
    prompt = ChatPromptTemplate.from_template(template)

    model_name = "qwen3:8b"
    title = "窗外"
    languages = ["英语", "法语", "俄语", "汉语"]
    
    try:
        # Initialize model with more explicit parameters
        llama_model = OllamaLLM(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=0,
            # Set a reasonable timeout
        )
        
        chain = prompt | llama_model
        
        print(f"\n🚀 运行模型: {model_name}")
        for lang in languages:
            print(f"\n===== {lang} =====")
            try:
                result = chain.invoke({"title": title, "lang": lang})
                clean_result = clean_think_sections(result)
                print(clean_result)
            except Exception as e:
                print(f"处理{lang}时出错: {str(e)}")
                
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n程序遇到错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
