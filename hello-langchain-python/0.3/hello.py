from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """你是顶级的短片作家，
请根据{title}的内容，使用中文写一篇50字的精品短文，
然后翻译成英文。"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434"
)
chain = prompt | model
response = chain.invoke({"title": "窗外"})
print(response)