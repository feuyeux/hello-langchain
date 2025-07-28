package org.feuyeux.ai.langchain.hellolangchain;

import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.ollama.OllamaChatModel;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.concurrent.TimeUnit;

import static dev.langchain4j.data.message.UserMessage.userMessage;
import static org.assertj.core.api.Assertions.assertThat;
import static org.feuyeux.ai.langchain.hellolangchain.HelloOllama.buildOllamaModel;

@Slf4j
public class MemoryTest {
    @AfterEach
    public void tearDown() throws InterruptedException {
        TimeUnit.SECONDS.sleep(25);
    }

    @Test
    public void givenMemory_whenPrompted_thenValidResponse() {
        OllamaChatModel model = buildOllamaModel();
        ChatMemory chatMemory = MessageWindowChatMemory.withMaxMessages(10);

        chatMemory.add(userMessage("Hello, my name is Kumar"));
        AiMessage answer = model.chat(chatMemory.messages()).aiMessage();
        log.info(answer.text());
        chatMemory.add(answer);
        Assertions.assertNotNull(answer.text());

        chatMemory.add(userMessage("What is my name?"));
        AiMessage answerWithName = model.chat(chatMemory.messages()).aiMessage();
        log.info(answerWithName.text());
        chatMemory.add(answerWithName);
        assertThat(answerWithName.text()).contains("Kumar");
    }

    @Test
    public void testLog() {
        log.debug("Hello, Java 21!");
        log.info("Hello, Java 21!");
        log.warn("Hello, Java 21!");
        log.error("Hello, Java 21!");
    }
}
