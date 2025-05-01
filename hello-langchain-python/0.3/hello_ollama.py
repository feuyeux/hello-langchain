from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """你是顶级的短片作家，
使用{lang},请根据{title}的内容，写一篇50字的精品短文"""
prompt = ChatPromptTemplate.from_template(template)

model_name = "qwen3:14b"
llama_model = OllamaLLM(
    model=model_name,
    base_url="http://localhost:11434",
    temperature=0,
)
chain = prompt | llama_model
languages = ["英语", "法语", "俄语", "汉语"]
for lang in languages:
    print(f"\n===== {lang} =====")
    result = chain.invoke({"title": "窗外", "lang": lang})    
    print(result)
