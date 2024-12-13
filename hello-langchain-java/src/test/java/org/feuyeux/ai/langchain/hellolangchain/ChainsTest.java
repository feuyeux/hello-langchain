package org.feuyeux.ai.langchain.hellolangchain;

import static dev.langchain4j.data.document.loader.FileSystemDocumentLoader.loadDocument;
import static java.time.Duration.ofSeconds;
import static org.feuyeux.ai.langchain.hellolangchain.OpenApi.getKey;

import dev.langchain4j.chain.ConversationalRetrievalChain;
import dev.langchain4j.data.document.Document;
import dev.langchain4j.data.document.parser.TextDocumentParser;
import dev.langchain4j.data.document.splitter.DocumentSplitters;
import dev.langchain4j.data.segment.TextSegment;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.langchain4j.model.chat.ChatLanguageModel;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.embedding.onnx.allminilml6v2.AllMiniLmL6V2EmbeddingModel;
import dev.langchain4j.model.input.PromptTemplate;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.retriever.EmbeddingStoreRetriever;
import dev.langchain4j.store.embedding.EmbeddingStore;
import dev.langchain4j.store.embedding.EmbeddingStoreIngestor;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;
import java.nio.file.Paths;
import java.util.concurrent.TimeUnit;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

@Slf4j
public class ChainsTest {
  public static final String SIMPSON_S_ADVENTURES_TXT =
      "src/test/resources/simpson's_adventures.txt";

  @AfterEach
  public void tearDown() throws InterruptedException {
    TimeUnit.SECONDS.sleep(25);
  }

  @Test
  public void givenChainWithDocument_whenPrompted_thenValidResponse() {
    EmbeddingModel embeddingModel = new AllMiniLmL6V2EmbeddingModel();

    EmbeddingStore<TextSegment> embeddingStore = new InMemoryEmbeddingStore<>();

    EmbeddingStoreIngestor ingestor =
        EmbeddingStoreIngestor.builder()
            .documentSplitter(DocumentSplitters.recursive(500, 0))
            .embeddingModel(embeddingModel)
            .embeddingStore(embeddingStore)
            .build();

    Document document = loadDocument(Paths.get(SIMPSON_S_ADVENTURES_TXT), new TextDocumentParser());
    ingestor.ingest(document);

    ChatLanguageModel chatModel =
        OpenAiChatModel.builder().apiKey(getKey()).timeout(ofSeconds(60)).build();

    ConversationalRetrievalChain chain =
        ConversationalRetrievalChain.builder()
            .chatLanguageModel(chatModel)
            .retriever(EmbeddingStoreRetriever.from(embeddingStore, embeddingModel))
            .chatMemory(MessageWindowChatMemory.withMaxMessages(10))
            .promptTemplate(
                PromptTemplate.from(
                    "Answer the following question to the best of your ability: {{question}}\n\nBase your answer on the following information:\n{{information}}"))
            .build();

    String answer = chain.execute("Who is Simpson?");

    log.info(answer);
    Assertions.assertNotNull(answer);
  }
}
