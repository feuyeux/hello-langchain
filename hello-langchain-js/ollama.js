import { Ollama } from "@langchain/ollama";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

const prompt = ChatPromptTemplate.fromMessages([
    ["human", "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"],
]);
const model = new Ollama({model: "llama3.2"});
const outputParser = new StringOutputParser();
const chain = prompt.pipe(model).pipe(outputParser);
const response = await chain.invoke({
    title: "窗外",
});
console.log(response);