import { Ollama } from "@langchain/ollama";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

// 配置 Ollama 模型
const model = new Ollama({
    baseUrl: "http://localhost:11434", // Ollama 默认地址
    model: "qwen2.5", // 使用 qwen2.5 模型
});

// 创建 Prompt Template
const prompt = ChatPromptTemplate.fromMessages([
    ["human", "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"],
]);

// 创建输出解析器
const outputParser = new StringOutputParser();

// 构建处理链
const chain = prompt.pipe(model).pipe(outputParser);

// 异步主函数
async function main() {
    try {
        console.log("🚀 开始生成短文...\n");
        
        const response = await chain.invoke({
            title: "窗外",
        });
        
        console.log("✅ 生成结果：\n");
        console.log(response);
        console.log("\n✨ 完成！");
        
    } catch (error) {
        console.error("❌ 错误:", error.message);
        
        if (error.message.includes("ECONNREFUSED")) {
            console.error("\n💡 提示：请确保 Ollama 服务正在运行");
            console.error("   运行命令：ollama serve");
        } else if (error.message.includes("model")) {
            console.error("\n💡 提示：请确保已下载 qwen2.5 模型");
            console.error("   运行命令：ollama pull qwen2.5");
        }
        
        process.exit(1);
    }
}

// 执行主函数
main();