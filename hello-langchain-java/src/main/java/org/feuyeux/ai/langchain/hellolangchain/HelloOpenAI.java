package org.feuyeux.ai.langchain.hellolangchain;

import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getKey;
import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getZhipuKey;

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
public class HelloOpenAI {
  public static void main(String[] args) {
    Prompt prompt =
        PromptTemplate.from("你是顶级的短片作家，请根据{{title}}的内容，写一篇50字的精品短文，然后翻译成英文。")
            .apply(Map.of("title", "窗外"));
    String apiKey = getZhipuKey();
    ChatLanguageModel model = OpenAiChatModel.builder()
            .apiKey(apiKey)
            .baseUrl( "https://open.bigmodel.cn/api/paas/v4")
            .modelName("GLM-4-Plus")
            .temperature(0.7)
            .build();
    String response = model.generate(prompt.text());
    log.info("{}", response);
  }
}
