package org.feuyeux.ai.langchain.hellolangchain;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import java.util.Map;

import dev.langchain4j.model.ollama.OllamaChatModel;
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
    String modelName = "llama3.2";
    ChatLanguageModel model =
        OllamaChatModel.builder().baseUrl("http://localhost:11434").modelName(modelName).build();
    String response = model.generate(prompt.text());
    log.info("{}", response);
  }
}
