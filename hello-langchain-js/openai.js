import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

// 配置智谱 AI 模型
const model = new ChatOpenAI({
    modelName: "GLM-4-Plus",
    apiKey: process.env.ZHIPUAI_API_KEY,
    baseUrl: "https://open.bigmodel.cn/api/paas/v4",
    temperature: 0.7,
});

// 配置聊天提示模板
const prompt = ChatPromptTemplate.fromMessages([
    ["system", "你是顶级的短片作家"],
    ["human", "请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"],
]);

// 创建输出解析器
const outputParser = new StringOutputParser();

// 构建处理链
const chain = prompt.pipe(model).pipe(outputParser);

// 异步主函数
async function main() {
    try {
        console.log("🚀 开始生成短文...\n");
        
        // 使用 chain.invoke 方法调用链
        const response = await chain.invoke({
            title: "窗外",
        });
        
        console.log("✅ 生成结果：\n");
        console.log(response);
        console.log("\n✨ 完成！");
        
    } catch (error) {
        console.error("❌ 错误:", error.message);
        
        if (error.message.includes("API key")) {
            console.error("\n💡 提示：请设置智谱 AI API Key");
            console.error("   export ZHIPUAI_API_KEY=your_api_key");
            console.error("   或运行：source .env.sh");
        } else if (error.response) {
            console.error("响应错误:", error.response.data || error.response);
        }
        
        process.exit(1);
    }
}

// 执行主函数
main();