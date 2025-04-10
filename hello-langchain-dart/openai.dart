import 'dart:io';

import 'package:langchain_openai/langchain_openai.dart';

import 'infer.dart';

main(List<String> args) async {
  await infer("你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。", {"title": "窗外"},
      buildModel());
}

ChatOpenAI buildModel() {
  final apiKey = Platform.environment['ZHIPUAI_API_KEY'];
  final baseUrl = "https://open.bigmodel.cn/api/paas/v4";
  final llm = ChatOpenAI(
      apiKey: apiKey,
      baseUrl: baseUrl,
      defaultOptions:
          const ChatOpenAIOptions(model: "GLM-4-Plus", temperature: 0.7));
  return llm;
}
