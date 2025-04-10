import {ChatOpenAI} from "@langchain/openai";
import {ChatPromptTemplate} from "@langchain/core/prompts";
import {StringOutputParser} from "@langchain/core/output_parsers";

// 配置聊天提示模板
const prompt = ChatPromptTemplate.fromMessages([
    ["system", "你是顶级的短片作家"],
    ["human", "请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"],
]);

// 配置自定义的智谱 AI 模型
const model = new ChatOpenAI({
    modelName: "GLM-4-Plus",
    apiKey: process.env.ZHIPUAI_API_KEY,
    temperature: 0.7,
});

// 创建输出解析器
const outputParser = new StringOutputParser();

// 构建处理链
const chain = prompt.pipe(model).pipe(outputParser);

// 异步主函数
async function main() {
    try {
        // 使用 chain.invoke 方法调用链
        const response = await chain.invoke({
            title: "窗外",
        });
        console.log(response);
    } catch (error) {
        console.error("错误:", error.message);
        if (error.response) {
            console.error("响应错误:", error.response);
        }
    }
}

// 执行主函数
main();