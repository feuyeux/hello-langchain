from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "sk-anystring"


def main():
    template = """你是顶级的短片作家，
    使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
    prompt = ChatPromptTemplate.from_template(template)

    model_name = "qwen3-14b"
    title = "窗外"
    languages = ["英语", "法语", "俄语", "汉语"]
    lm_studio_model = ChatOpenAI(
        model=model_name,
        base_url="http://localhost:1234/v1",
        temperature=0,
    )
    chain = prompt | lm_studio_model
    for lang in languages:
        print(f"\n===== {lang} =====")
        result = chain.invoke({"title": title, "lang": lang})
        print(result)


if __name__ == "__main__":
    main()
