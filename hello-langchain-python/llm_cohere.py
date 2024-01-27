from langchain_community.llms import Cohere
from langchain_core.prompts import PromptTemplate

model = Cohere(model="command", max_tokens=256, temperature=0.75)
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | model

response = chain.invoke({"topic": "bears"})
print(response)
