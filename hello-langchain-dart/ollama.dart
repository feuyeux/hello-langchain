import 'package:langchain/langchain.dart';
import 'package:langchain_ollama/langchain_ollama.dart';

main(List<String> args) async {
  final prompt = PromptTemplate.fromTemplate(
      "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。");
  final llm = ChatOllama();
  final runnableLlm =
      llm as Runnable<PromptValue, BaseLangChainOptions, Object?>;
  final chain = prompt.pipe(runnableLlm);
  final result =
      await chain.invoke({"title": "窗外"}) as LanguageModelResult<Object>;
  print(result.generations[0].output);
}
