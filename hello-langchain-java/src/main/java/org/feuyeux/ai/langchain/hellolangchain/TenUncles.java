package org.feuyeux.ai.langchain.hellolangchain;

import static dev.langchain4j.model.openai.OpenAiModelName.GPT_3_5_TURBO;
import static org.feuyeux.ai.langchain.hellolangchain.OpenApi.getKey;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.openai.OpenAiChatModel;
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

    // Connect to an LLM
    ChatLanguageModel model =
        OpenAiChatModel.builder()
            .apiKey(getKey())
            .modelName(GPT_3_5_TURBO)
            .temperature(0.3)
            .build();

    String response = model.generate(prompt.text());
    log.info("GPT_3_5_TURBO:{}", response);
  }
}
