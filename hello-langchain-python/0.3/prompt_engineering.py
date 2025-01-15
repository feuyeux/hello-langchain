from langchain import hub
from langchain.prompts import load_prompt
from langchain_community.chat_models import ChatZhipuAI
import os
from dotenv import load_dotenv

load_dotenv()

# https://open.bigmodel.cn/usercenter/proj-mgmt/rate-limits
# https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys
print(f"ZHIPUAI_API_KEY={os.environ["ZHIPUAI_API_KEY"]}")
llm = ChatZhipuAI(
    model="GLM-4-Plus",
    temperature=0,
)

context = "俄国文化和民俗"
question = "谢尔盖维奇的父亲叫什么？"

# https: // github.com/hwchase17/langchain-hub/blob/master/prompts/pal/colored_objects.json
prompt = load_prompt("resources/prompt.yml")
chain = prompt | llm
answer = chain.invoke({"context": context, "question": question})
print(answer)

# https://smith.langchain.com/
print(f"LANGSMITH_API_KEY={os.environ["LANGSMITH_API_KEY"]}")
prompt = hub.pull("feuyeux/hello")
chain = prompt | llm
answer = chain.invoke({"context": context, "question": question})
print(answer)
