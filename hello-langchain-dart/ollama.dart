import 'package:langchain_ollama/langchain_ollama.dart';

import 'infer.dart';

main(List<String> args) async {
  await infer("你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。", {"title": "窗外"},
      buildModel());
}

ChatOllama buildModel() {
  final llm = ChatOllama(
      baseUrl: 'http://localhost:11434/api',
      defaultOptions: const ChatOllamaOptions(
        model: 'llama3.2',
        temperature: 0.7,
      ),
      encoding: 'cl100k_base');

  return llm;
}
