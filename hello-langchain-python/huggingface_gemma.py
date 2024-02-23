from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# https://huggingface.co/google/gemma-2b
repo_id = "google/gemma-2b"

llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)

prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
chain = prompt | llm

response = chain.invoke({"topic": "bears"})
print(response)
