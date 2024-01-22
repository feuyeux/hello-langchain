from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


question = "Who won the FIFA World Cup in the year 1994? "
template = """Question: {question}
Answer: Let's think step by step."""
prompt = PromptTemplate(template=template, input_variables=["question"])

# Flan, by Google
# See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
repo_id = "google/flan-t5-xxl"
# Dolly, by Databricks
# repo_id = "databricks/dolly-v2-3b"
# Camel, by Writer
# See https://huggingface.co/Writer for other options
# repo_id = "Writer/camel-5b-hf"
# XGen, by Salesforce
# repo_id = "Salesforce/xgen-7b-8k-base"
# Falcon, by Technology Innovation Institute (TII)
# repo_id = "tiiuae/falcon-40b"

llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)

# InternLM-Chat, by Shanghai AI Laboratory
# repo_id = "internlm/internlm-chat-7b"
# llm = HuggingFaceHub(
#     repo_id=repo_id, model_kwargs={"max_length": 128, "temperature": 0.8}
# )

# Qwen, by Alibaba Cloud
# repo_id = "Qwen/Qwen-7B"
# llm = HuggingFaceHub(
#     repo_id=repo_id, model_kwargs={"max_length": 128, "temperature": 0.5}
# )

#
llm_chain = LLMChain(prompt=prompt, llm=llm)
print(llm_chain.run(question))
