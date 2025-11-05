from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
import time
from tools.format_utils import extract_content_after_think, print_section_header, print_content

os.environ["OPENAI_API_KEY"] = "sk-anystring"


def main():
    template = """你是顶级的短片作家，
    使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
    prompt = ChatPromptTemplate.from_template(template)

    # model_name = "qwen3-14b"
    model_name = "qwen3-8b-mlx"
    # languages = ["英语", "法语", "俄语", "汉语"]
    languages = ["英语", "汉语"]

    title = "窗外"
    lm_studio_model = ChatOpenAI(
        model=model_name,
        base_url="http://localhost:1234/v1",
        temperature=0,
    )
    chain = prompt | lm_studio_model

    for lang in languages:
        print_section_header(f"语言: {lang}")
        
        start_time = time.time()
        result = chain.invoke({"title": title, "lang": lang})
        end_time = time.time()
        
        # 处理结果，提取<think>标签之后的内容
        processed_result = extract_content_after_think(result)
        
        print(f"\n响应时间: {end_time - start_time:.2f}秒")
        print_content(processed_result)


if __name__ == "__main__":
    main()
