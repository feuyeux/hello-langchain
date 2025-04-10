import 'dart:io';

import 'package:langchain/langchain.dart';

Future<void> infer(
    String template, Map<String, String> map, BaseChatModel model) async {
  final prompt = PromptTemplate.fromTemplate(template);
  final chain = prompt.pipe(model);
  final stream = chain.stream(map);
  await stream
      .forEach((final chunk) => stdout.write('${chunk.output.content}|'));
}
