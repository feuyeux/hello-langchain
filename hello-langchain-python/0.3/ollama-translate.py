from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """你是顶级的短片作家，
请根据{title}的内容，使用中文写一篇50字的精品短文，
然后翻译成{lang}。"""
prompt = ChatPromptTemplate.from_template(template)

llama_model = OllamaLLM(
    model="llama3.2",
    base_url="http://localhost:11434",
    temperature=0,
)
chain = prompt | llama_model
result = chain.invoke({"title": "窗外", "lang": "法语"})
print(result)
