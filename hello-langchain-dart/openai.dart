import 'package:langchain/langchain.dart';
import 'package:langchain_openai/langchain_openai.dart';

main(List<String> args) async {
  final llm = ChatOpenAI(apiKey: "");

  final prompt = PromptTemplate.fromTemplate(
      "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。");

  final chain = prompt.pipe(llm);
  final LanguageModelResult result = await chain.invoke({"title": "窗外"});
  print(result.generations[0].output);
}
