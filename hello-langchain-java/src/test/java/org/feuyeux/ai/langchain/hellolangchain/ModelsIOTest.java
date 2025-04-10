package org.feuyeux.ai.langchain.hellolangchain;

import static dev.langchain4j.model.openai.OpenAiModelName.GPT_3_5_TURBO;
import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getKey;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.openai.OpenAiChatModel;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

@Slf4j
public class ModelsIOTest {
  @AfterEach
  public void tearDown() throws InterruptedException {
    TimeUnit.SECONDS.sleep(25);
  }

  @Test
  public void givenPromptTemplate_whenSuppliedInput_thenValidResponse() {
    PromptTemplate promptTemplate =
        PromptTemplate.from("Tell me a {{adjective}} joke about {{content}}..");
    Map<String, Object> variables = new HashMap<>();
    variables.put("adjective", "funny");
    variables.put("content", "humans");
    Prompt prompt = promptTemplate.apply(variables);

    ChatLanguageModel model =
        OpenAiChatModel.builder()
            .apiKey(getKey())
            .modelName(GPT_3_5_TURBO)
            .temperature(0.3)
            .build();

    String response = model.generate(prompt.text());
    log.info(response);
    Assertions.assertNotNull(response);
  }
}
