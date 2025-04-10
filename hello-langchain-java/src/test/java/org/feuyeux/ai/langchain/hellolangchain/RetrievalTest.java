package org.feuyeux.ai.langchain.hellolangchain;

import static dev.langchain4j.data.document.loader.FileSystemDocumentLoader.loadDocument;
import static dev.langchain4j.model.openai.OpenAiChatModelName.GPT_4;
import static java.time.Duration.ofSeconds;
import static java.util.stream.Collectors.joining;
import static org.feuyeux.ai.langchain.hellolangchain.utils.OpenApi.getKey;

import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.DocumentSplitter;
import dev.langchain4j.data.document.parser.TextDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.embedding.Embedding;
import dev.langchain4j.data.message.AiMessage;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.embedding.onnx.allminilml6v2.AllMiniLmL6V2EmbeddingModel;
import dev.langchain4j.model.input.Prompt;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.model.openai.OpenAiTokenizer;
import dev.langchain4j.store.embedding.EmbeddingMatch;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

@Slf4j
public class RetrievalTest {

  public static final String SIMPSON_S_ADVENTURES_TXT =
      "src/test/resources/simpson's_adventures.txt";

  @AfterEach
  public void tearDown() throws InterruptedException {
    TimeUnit.SECONDS.sleep(25);
  }

  @Test
  public void givenDocument_whenPrompted_thenValidResponse() {
    Document document = loadDocument(Paths.get(SIMPSON_S_ADVENTURES_TXT), new TextDocumentParser());
    DocumentSplitter splitter = DocumentSplitters.recursive(100, 0, new OpenAiTokenizer(GPT_4));
    List<TextSegment> segments = splitter.split(document);

    EmbeddingModel embeddingModel = new AllMiniLmL6V2EmbeddingModel();
    List<Embedding> embeddings = embeddingModel.embedAll(segments).content();
    EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();
    embeddingStore.addAll(embeddings, segments);

    String question = "Who is Simpson?";
    Embedding questionEmbedding = embeddingModel.embed(question).content();
    int maxResults = 3;
    double minScore = 0.7;
    List<EmbeddingMatch<TextSegment>> relevantEmbeddings =
        embeddingStore.findRelevant(questionEmbedding, maxResults, minScore);

    PromptTemplate promptTemplate =
        PromptTemplate.from(
            "Answer the following question to the best of your ability:\n"
                + "\n"
                + "Question:\n"
                + "{{question}}\n"
                + "\n"
                + "Base your answer on the following information:\n"
                + "{{information}}");

    String information =
        relevantEmbeddings.stream().map(match -> match.embedded().text()).collect(joining("\n\n"));

    Map<String, Object> variables = new HashMap<>();
    variables.put("question", question);
    variables.put("information", information);

    Prompt prompt = promptTemplate.apply(variables);
    ChatLanguageModel chatModel =
        OpenAiChatModel.builder().apiKey(getKey()).timeout(ofSeconds(60)).build();
    AiMessage aiMessage = chatModel.generate(prompt.toUserMessage()).content();

    log.info(aiMessage.text());
    Assertions.assertNotNull(aiMessage.text());
  }
}
