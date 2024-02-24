from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# https://huggingface.co/google/gemma-7b
repo_7b = "google/gemma-7b"
# https://huggingface.co/google/gemma-2b
repo_2b = "google/gemma-2b"
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]
#
# tokenizer = AutoTokenizer.from_pretrained(
#     repo_7b, token=HUGGINGFACEHUB_API_TOKEN)
# model = AutoModelForCausalLM.from_pretrained(
#     repo_7b, token=HUGGINGFACEHUB_API_TOKEN)

# input_text = "Write me a poem about Machine Learning."
# input_ids = tokenizer(input_text, return_tensors="pt")

# outputs = model.generate(**input_ids)
# print(tokenizer.decode(outputs[0]))
#

gemma_2b_llm = HuggingFaceHub(
    repo_id=repo_2b, model_kwargs={"temperature": 0, "max_length": 64}
)

gemma_7b_llm = HuggingFaceHub(
    repo_id=repo_7b, model_kwargs={"temperature": 0, "max_length": 64})


prompt_template = """Question: {question}
 
Answer: Let's think step by step."""
prompt = PromptTemplate(template=prompt_template,
                        input_variables=["question"])

gemma_2b_chain = LLMChain(prompt=prompt, llm=gemma_2b_llm)
gemma_7b_chain = LLMChain(prompt=prompt, llm=gemma_7b_llm)

question = "In the first movie of Harry Potter, what is the name of the three-headed dog?"

print("==== 2b result ====")
for chunk in gemma_2b_chain.stream(question):
    print(chunk['text'], end="", flush=True)
#
print("\n==== 7b result ====")
for chunk in gemma_7b_chain.stream(question):
    print(chunk['text'], end="", flush=True)
