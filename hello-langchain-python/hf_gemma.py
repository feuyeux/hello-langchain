import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# https://huggingface.co/google/gemma-7b
repo_7b = "google/gemma-7b"
# https://huggingface.co/google/gemma-2b
repo_2b = "google/gemma-2b"
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"]

tokenizer = AutoTokenizer.from_pretrained(repo_2b)
model = AutoModelForCausalLM.from_pretrained(repo_2b)

input_text = "List ten plans for tourists in Malaga, Spain."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids, max_length=256)
print(tokenizer.decode(outputs[0]))
