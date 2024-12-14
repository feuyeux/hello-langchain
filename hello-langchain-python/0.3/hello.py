from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()
# https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys
print(f"{os.environ["ZHIPUAI_API_KEY"]}")
# https://platform.moonshot.cn/console/api-keys
print(f"{os.environ["MOONSHOT_API_KEY"]}")

template = """你是顶级的短片作家，
请根据{title}的内容，使用中文写一篇50字的精品短文，
然后翻译成英文。"""
prompt = ChatPromptTemplate.from_template(template)


def llama():
    llama_model = OllamaLLM(
        model="llama3.3",
        base_url="http://localhost:11434",
        temperature=0,
    )
    chain = prompt | llama_model
    return chain.invoke({"title": "窗外"})


def zhipu():
    # https://open.bigmodel.cn/usercenter/proj-mgmt/rate-limits
    zhipu_model = ChatZhipuAI(
        model="GLM-4-Plus",
        temperature=0,
    )
    chain = prompt | zhipu_model
    return chain.invoke({"title": "窗外"})


def kimi():
    # https://platform.moonshot.cn/docs/api
    kimi_model = MoonshotChat(model="moonshot-v1-8k", temperature=0)
    chain = prompt | kimi_model
    return chain.invoke({"title": "窗外"})


zhipu_response = zhipu()
kimi_response = kimi()
llama_response = llama()

print("Zhipu model response:\n" + "-"*20)
print(zhipu_response)
print("\nKimi model response:\n" + "-"*20)
print(kimi_response)
print("\nLlama model response:\n" + "-"*20)
print(llama_response)
