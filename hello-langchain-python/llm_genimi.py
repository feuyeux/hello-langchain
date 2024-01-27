import os
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
# print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
# print("GOOGLE_API_KEY:", os.environ['GOOGLE_API_KEY'])
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
#
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(
    "List 5 planets each with an interesting fact")
print(response.text)
#
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | model
response = chain.invoke({"topic": "bears"})
print(response.content)
