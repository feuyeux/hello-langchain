from langchain_community.llms import GPT4All
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文"
)

# https://gpt4all.io/index.html
gpt4all = GPT4All(
    model="C:/Users/han/Downloads/nous-hermes-llama2-13b.Q4_0.gguf",
    max_tokens=2048,
)

chain = prompt | gpt4all
response = chain.invoke({"title": "窗外"})
print(response)
