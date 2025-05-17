# Hello LangChain Python

This repository contains scripts for running different LLM applications using LangChain.

## Installation

```bash
uv pip install -r requirements.txt
```

## Run

### Run with OpenAI API

```bash
uv run hello.py
```

### Run with Ollama

```bash
uv run hello_ollama.py
```

### Run Profile

```bash
uv run hello_profile.py
uv run hello_profile_png.py
```

### Monitor NVIDIA GPU (WSL)

```bash
wsl -d ubuntu -u han bash -c 'nvidia-smi -l 5'
```
