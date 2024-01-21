# Hello Langchain(Python)

```sh
python3 -m venv lc_env
source lc_env/bin/activate
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install langchain langchain-core langchain-openai -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install gpt4all -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U langchain-community cohere -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```sh
```

openai

```sh
python hello.py
```

local model

```sh
python local_gpt4.py

AI: As I observe the world outside my window, I see a vibrant and ever-changing landscape. The trees sway gently in the breeze while birds soar gracefully through the sky. Cars zoom by on the highway, their headlights illuminating the night. People pass by on foot, lost in thought or engaged in conversation. It's a symphony of movement and sound that never ceases to amaze me.
```

cohere

```sh
source lc_env/Scripts/activate
#https://dashboard.cohere.com/api-keys
export COHERE_API_KEY=xxx
python cohere.py
```
