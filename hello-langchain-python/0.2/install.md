# LangChain v0.2

```sh
python3 -m venv lc_env
source lc_env/bin/activate

pip install --upgrade pip
pip install langchain-core langchain langchain-community langgraph langsmith
pip install -qU langchain_ollama
```

- `langchain-core`: Base abstractions and LangChain Expression Language.
- `langchain-community`: Third party integrations.
  - Partner packages (e.g. langchain-openai, langchain-anthropic, etc.): Some integrations have been further split into their own lightweight packages that only depend on langchain-core.
- `langchain`: Chains, agents, and retrieval strategies that make up an application's cognitive architecture.
- LangGraph: Build robust and stateful multi-actor applications with LLMs by modeling steps as edges and nodes in a graph. Integrates smoothly with LangChain, but can be used without it.
- LangSmith: A developer platform that lets you debug, test, evaluate, and monitor LLM applications.
