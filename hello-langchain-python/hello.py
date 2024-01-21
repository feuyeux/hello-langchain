from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"
)
llm = ChatOpenAI()
chain = prompt | llm
response = chain.invoke({"title": "窗外"})
print(response)
