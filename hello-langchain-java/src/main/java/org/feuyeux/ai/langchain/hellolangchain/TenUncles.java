package org.feuyeux.ai.langchain.hellolangchain;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.ollama.OllamaChatModel;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;

/**
 * @author feuyeux
 */
@Slf4j
public class TenUncles {
  public static void main(String[] args) {
    PromptTemplate promptTemplate = PromptTemplate.from("根据{{message}}中的描述告诉我，钱是被谁偷的，钱是谁的。");

    Prompt prompt =
        promptTemplate.apply(
            Map.of("message", "大大爷带着二大爷到三大爷家说四大爷被五大爷骗到六大爷家偷七大爷放在八大爷柜子里九大爷给十大爷的一千块钱"));
    String modelName = "llama3.2";
    ChatLanguageModel model =
        OllamaChatModel.builder().baseUrl("http://localhost:11434").modelName(modelName).build();
    String response = model.generate(prompt.text());
    log.info("GPT_3_5_TURBO:{}", response);
  }
}
