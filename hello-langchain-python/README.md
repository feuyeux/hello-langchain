# Hello Langchain(Python)

```sh
python3 -m venv lc_env
# On Linux and macOS
source lc_env/bin/activate
# On Windows
source lc_env/Scripts/activate

python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install langchain langchain-core langchain-openai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install gpt4all -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U langchain-community cohere -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U huggingface_hub -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```sh
```

## openai

```sh
python hello.py
```

## support local models

```sh
python local_gpt4.py

AI: As I observe the world outside my window, I see a vibrant and ever-changing landscape. The trees sway gently in the breeze while birds soar gracefully through the sky. Cars zoom by on the highway, their headlights illuminating the night. People pass by on foot, lost in thought or engaged in conversation. It's a symphony of movement and sound that never ceases to amaze me.
```

## support llms

```sh
#https://dashboard.cohere.com/api-keys
export COHERE_API_KEY=xxx
python llm_cohere.py

What color socks do bears wear?

They don’t wear socks, they have bear feet. 

OW! Okay, that was pretty bad, sorry. Would you like me to tell you a better joke? 
```

```sh
# https://huggingface.co/settings/tokens
export HUGGINGFACEHUB_API_TOKEN=xxx
python llm_huggingface.py

The FIFA World Cup in the year 1994 was won by France. The answer: France.
```
