package org.feuyeux.ai.langchain.hellolangchain;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.message.UserMessage;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.ollama.OllamaChatModel;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;

/**
 * @author feuyeux
 */
@Slf4j
public class HelloOllama {
  public static void main(String[] args) {
    Prompt prompt =
        PromptTemplate.from("你是顶级的短片作家，请根据{{title}}的内容，写一篇50字的精品短文，然后翻译成英文。")
            .apply(Map.of("title", "窗外"));
    ChatModel model = buildOllamaModel();
    String input = prompt.text();
    String result = model.chat(input);
    log.info("{}", result);
    log.info("{}", "=====================");
    AiMessage response = model.chat(UserMessage.from(input)).aiMessage();
    log.info("{}", response.text());
  }

  public static OllamaChatModel buildOllamaModel() {
    String modelName = "qwen2.5";
    return OllamaChatModel.builder().baseUrl("http://localhost:11434").modelName(modelName).build();
  }
}
