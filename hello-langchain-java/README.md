# Hello Langchain(Java)

```sh
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# 下载模型
ollama pull qwen2.5
```

**设置 API Keys (如使用在线服务)**

```sh
# OpenAI API Key
export OPENAI_API_KEY={YOUR_OPENAI_API_KEY}

# 智谱 AI API Key (用于 HelloOpenAI 示例)
export ZHIPU_API_KEY={YOUR_ZHIPU_API_KEY}
```

```sh
# HelloOllama - 基础对话示例
java -cp target/hello-langchain-0.0.1-SNAPSHOT.jar \
  org.feuyeux.ai.langchain.hellolangchain.HelloOllama

# TenUnclesOllama - 中文推理示例
java -cp target/hello-langchain-0.0.1-SNAPSHOT.jar \
  org.feuyeux.ai.langchain.hellolangchain.TenUnclesOllama

java -cp target/hello-langchain-0.0.1-SNAPSHOT.jar \
  org.feuyeux.ai.langchain.hellolangchain.HelloOpenAI
```

```sh
mvn clean test
mvn test -Dtest=MemoryTest
mvn test -Dtest=AgentsTest
```

## References

- [LangChain4j 官方文档](https://docs.langchain4j.dev/)
- [LangChain4j GitHub](https://github.com/langchain4j/langchain4j)
- [Ollama 官网](https://ollama.com/)
- [智谱 AI 开放平台](https://open.bigmodel.cn/)
