from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
import time
import re

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
    def extract_content_after_think(text):
        """
        提取<think>标签之后的内容，如果没有<think>标签则返回原文本
        """
        if isinstance(text, str):
            # 如果响应中包含</think>标签，则只保留其后的内容
            if '</think>' in text:
                content = text.split('</think>', 1)[1].lstrip()
                return content
            return text
        # 如果是消息对象而非字符串，则提取content属性
        if hasattr(text, 'content'):
            content = text.content
            if '</think>' in content:
                return content.split('</think>', 1)[1].lstrip()
            return content
        return str(text)
    
    for lang in languages:
        print(f"\n===== {lang} =====")
        start_time = time.time()
        result = chain.invoke({"title": title, "lang": lang})
        end_time = time.time()
        print(f"Generation time: {end_time - start_time:.2f} seconds")
        
        # 处理结果，提取<think>标签之后的内容
        processed_result = extract_content_after_think(result)
        print(processed_result)


if __name__ == "__main__":
    main()
