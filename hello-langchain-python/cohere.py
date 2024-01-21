from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatCohere
from langchain_core.messages import HumanMessage

chat = ChatCohere(model="command", max_tokens=256, temperature=0.75)
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | chat

chain.invoke({"topic": "bears"})