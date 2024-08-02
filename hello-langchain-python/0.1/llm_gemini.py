from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-pro")
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm

response = chain.invoke({"topic": "bears"})
print(response.content)
