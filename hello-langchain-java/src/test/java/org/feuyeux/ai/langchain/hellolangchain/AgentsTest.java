package org.feuyeux.ai.langchain.hellolangchain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getKey;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;

@Slf4j
public class AgentsTest {
  static class Calculator {
    @Tool("Calculates the length of a string")
    int stringLength(String s) throws InterruptedException {
      log.info("Calculating the length of \"{}\"...", s);
      TimeUnit.SECONDS.sleep(15);
      return s.length();
    }

    @Tool("Calculates the sum of two numbers")
    int add(int a, int b) {
      return a + b;
    }
  }

  interface Assistant {
    String chat(String userMessage);
  }

  @AfterEach
  public void tearDown() throws InterruptedException {
    TimeUnit.SECONDS.sleep(25);
  }

  @Test
  public void givenServiceWithTools_whenPrompted_thenValidResponse() throws InterruptedException {
    Assistant assistant =
        AiServices.builder(Assistant.class)
            .chatLanguageModel(OpenAiChatModel.withApiKey(getKey()))
            .tools(new Calculator())
            .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
            .build();

    String question =
        "What is the sum of the numbers of letters in the words \"language\" and \"model\"?";
    String answer = assistant.chat(question);

    log.info("answer:{}", answer);
    assertThat(answer).contains("13");
  }
}
