# Hello LangChain (JavaScript)

## 快速开始

### 1. 环境准备

**安装 Node.js**

```sh
node --version

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts
```

**安装 Ollama (本地模型)**

```sh
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# 下载模型
ollama pull qwen2.5
```

### 2. 配置环境变量

**方式 1: 创建 `.env.sh` (推荐用于脚本运行)**

```sh
#!/bin/bash
export ZHIPUAI_API_KEY="your_zhipu_api_key_here"
```

**方式 2: 创建 `.env` (用于 dotenv 加载)**

```env
ZHIPUAI_API_KEY=your_zhipu_api_key_here
```

### 3. 安装依赖

```sh
npm install
# 或
yarn install
# 或
pnpm install
```

### 4. 运行示例

#### 使用 Ollama 本地模型

```sh
# 方式 1: 直接运行脚本
./run_ollama.sh

# 方式 2: 使用 Node.js
node ollama.js

# Windows
run_ollama.bat
```

#### 使用 OpenAI 兼容 API

```sh
./run_openai.sh

source .env.sh
node openai.js

# Windows
run_openai.bat
```

## References

- [LangChain.js 官方文档](https://js.langchain.com/)
- [LangChain.js GitHub](https://github.com/langchain-ai/langchainjs)
- [Ollama 官网](https://ollama.com/)
- [智谱 AI 开放平台](https://open.bigmodel.cn/)
- [LangChain Expression Language (LCEL)](https://js.langchain.com/docs/expression_language/)
