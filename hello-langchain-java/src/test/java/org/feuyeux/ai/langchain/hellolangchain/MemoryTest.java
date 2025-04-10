package org.feuyeux.ai.langchain.hellolangchain;

import static dev.langchain4j.data.message.UserMessage.userMessage;
import static dev.langchain4j.model.openai.OpenAiModelName.GPT_3_5_TURBO;
import static org.assertj.core.api.Assertions.assertThat;
import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getKey;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.TokenWindowChatMemory;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.openai.OpenAiTokenizer;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

@Slf4j
public class MemoryTest {
  @AfterEach
  public void tearDown() throws InterruptedException {
    TimeUnit.SECONDS.sleep(25);
  }

  @Test
  public void givenMemory_whenPrompted_thenValidResponse() {
    ChatLanguageModel model = OpenAiChatModel.withApiKey(getKey());
    ChatMemory chatMemory =
        TokenWindowChatMemory.withMaxTokens(300, new OpenAiTokenizer(GPT_3_5_TURBO));

    chatMemory.add(userMessage("Hello, my name is Kumar"));
    AiMessage answer = model.generate(chatMemory.messages()).content();
    log.info(answer.text());
    chatMemory.add(answer);
    Assertions.assertNotNull(answer.text());

    chatMemory.add(userMessage("What is my name?"));
    AiMessage answerWithName = model.generate(chatMemory.messages()).content();
    log.info(answerWithName.text());
    chatMemory.add(answerWithName);
    assertThat(answerWithName.text()).contains("Kumar");
  }
}
