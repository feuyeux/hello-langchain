from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_community.chat_models import ChatZhipuAI
from langchain_community.chat_models.moonshot import MoonshotChat
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from tools.format_utils import print_model_result

load_dotenv()
# https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys
print(f"ZHIPUAI_API_KEY={os.environ['ZHIPUAI_API_KEY']}")
#
print(f"QIANFAN_ACCESS_KEY={os.environ['QIANFAN_ACCESS_KEY']}")
print(f"QIANFAN_SECRET_KEY={os.environ['QIANFAN_SECRET_KEY']}")
#
# https://platform.moonshot.cn/console/api-keys
# print(f"{os.environ["MOONSHOT_API_KEY"]}")


template = """你是顶级的短片作家，
请根据{title}的内容，使用中文写一篇50字的精品短文，
然后翻译成英文。"""
prompt = ChatPromptTemplate.from_template(template)


def ollama():
    llama_model = ChatOllama(
        model="qwen2.5",
        base_url="http://localhost:11434",
        temperature=0,
    )
    chain = prompt | llama_model
    return chain.invoke({"title": "窗外"})


def zhipu():
    # https://open.bigmodel.cn/usercenter/proj-mgmt/rate-limits
    zhipu_model = ChatZhipuAI(
        model="GLM-4.7",
        temperature=0,
    )
    chain = prompt | zhipu_model
    return chain.invoke({"title": "窗外"})


def kimi():
    # https://platform.moonshot.cn/docs/api
    kimi_model = MoonshotChat(model="moonshot-v1-8k", temperature=0)
    chain = prompt | kimi_model
    return chain.invoke({"title": "窗外"})


def wenxin():
    wenxin_model = QianfanChatEndpoint(
        model="ERNIE-3.5-8K",
        temperature=0.2,
        timeout=30,
    )
    chain = prompt | wenxin_model
    return chain.invoke({"title": "窗外"})


def deepseek():
    llm = ChatOpenAI(
        model="deepseek-chat",
        openai_api_key=os.environ["DS_API_KEY"],
        openai_api_base="https://api.deepseek.com",
        max_tokens=1024,
    )
    chain = prompt | llm
    return chain.invoke({"title": "窗外"})

####

# 执行各个模型
print_model_result("智谱AI", zhipu)
# print_model_result("文心一言", wenxin)
# print_model_result("月之暗面", kimi)
# print_model_result("深度求索", deepseek)
# print_model_result("OLLAMA", ollama)
