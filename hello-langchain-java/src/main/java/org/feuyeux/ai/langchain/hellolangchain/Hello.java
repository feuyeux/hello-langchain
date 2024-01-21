package org.feuyeux.ai.langchain.hellolangchain;

import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.openai.OpenAiChatModel;
import lombok.extern.slf4j.Slf4j;

import java.util.Map;

import static org.feuyeux.ai.langchain.hellolangchain.OpenApi.getKey;

/**
 * @author feuyeux
 */
@Slf4j
public class Hello {
    public static void main(String[] args) {
        Prompt prompt = PromptTemplate
                .from("你是顶级的短片作家，请根据{{title}}的内容，写一篇50字的精品短文，然后翻译成英文。")
                .apply(Map.of("title", "窗外"));
        ChatLanguageModel model = OpenAiChatModel.builder().apiKey(getKey()).build();
        String response = model.generate(prompt.text());
        log.info("{}", response);
    }
}
