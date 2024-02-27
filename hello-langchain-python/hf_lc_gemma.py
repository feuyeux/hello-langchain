from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

# 指定模型名称
repo_7b = "google/gemma-7b"
repo_2b = "google/gemma-2b"

# 创建模型对象
gemma_2b_llm = HuggingFaceHub(repo_id=repo_2b, model_kwargs={
                              "temperature": 0.1, "max_length": 128, "min_generated_length": 50_000})
gemma_7b_llm = HuggingFaceHub(repo_id=repo_7b, model_kwargs={
                              "temperature": 0.1, "max_length": 256, "min_generated_length": 100_000})

# 指定提示模板
prompt_template = """Question:{question}

Answer:"""
prompt = PromptTemplate(template=prompt_template,
                        input_variables=["question"])

# 创建 LLMChain 对象
gemma_2b_chain = LLMChain(prompt=prompt, llm=gemma_2b_llm)
gemma_7b_chain = LLMChain(prompt=prompt, llm=gemma_7b_llm)

# 指定问题
question = "List ten plans for tourists in Beijing, China."

# 调用 gemma-2b 模型并打印结果
print("==== 2b result ====")
try:
    print(gemma_2b_chain.invoke(question)['text'])
except Exception as e:
    print("An error occurred:", e)

# 调用 gemma-7b 模型并打印结果
print("\n==== 7b result ====")
try:
    for chunk in gemma_7b_chain.stream(question):
        print(chunk['text'], end="", flush=True)
except Exception as e:
    print("An error occurred:", e)
