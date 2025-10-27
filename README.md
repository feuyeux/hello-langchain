# Hello LangChain 🦜️

A straightforward, equally capable demonstration for tracking the evolution of multiple programming languages across the iterations of LangChain.


## Resources

### SDK

1. [LangChain Python](https://github.com/langchain-ai/langchain)
2. [Langchain4j](https://github.com/langchain4j/langchain4j)
3. [LangChain Rust](https://github.com/Abraxas-365/langchain-rust)
4. [LangChain Go](https://github.com/tmc/langchaingo)
5. [LangChain Dart](https://github.com/davidmigloz/langchain_dart)
6. [LangChain JS](https://github.com/langchain-ai/langchainjs)

### Documentation

- [LangChain Python](https://python.langchain.com/docs/introduction/)
- [Langchain4j](https://docs.langchain4j.dev/)
- [LangChain Rust](https://docs.rs/crate/langchain-rust/latest)
- [LangChain Go](https://docs.langchain.com/)
- [LangChain Dart](https://pub.dev/packages/langchain)
- [LangChain JS](https://js.langchain.com/docs/introduction/)
- [Gemini](https://ai.google.dev/tutorials/python_quickstart)


## Quick Start

### 1. Python

`hello-langchain-python\0.3\run.sh`

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """你是顶级的短片作家，
请根据{title}的内容，使用中文写一篇50字的精品短文，
然后翻译成英文。"""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(
    model="qwen2.5",
    base_url="http://localhost:11434"
)
chain = prompt | model
response = chain.invoke({"title": "窗外"})
print(response)
```

```sh
窗外是一片宁静的世界，阳光洒在绿树上，微风轻拂着花朵。草地上，孩子们欢笑嬉戏，快乐的声音传遍整个街区。鸟儿在天空中自由地飞翔，歌唱着美妙的旋律。这一切，让我感受到了生活的美好和希望。

Outside the window is a peaceful world, with sunlight streaming on the green trees and a gentle breeze caressing the flowers. On the grass, children laugh and play, their joyful voices echoing throughout the neighborhood. Birds soar freely in the sky, singing beautiful melodies. All of this makes me feel the beauty and hope of life.
```

### 2. Java

```java
@Slf4j
public class HelloOllama {
  public static void main(String[] args) {
    Prompt prompt =
        PromptTemplate.from("你是顶级的短片作家，请根据{{title}}的内容，写一篇50字的精品短文，然后翻译成英文。")
            .apply(Map.of("title", "窗外"));
    String modelName = "qwen2.5";
    ChatLanguageModel model =
        OllamaChatModel.builder().baseUrl("http://localhost:11434").modelName(modelName).build();
    String response = model.generate(prompt.text());
    log.info("{}", response);
  }
}
```

```sh
窗外，阳光洒在青翠欲滴的树叶上，微风轻拂着花朵般的云朵。小鸟欢快地歌唱着，似乎在述说着大自然的美妙。这一幕幕景象，如同一幅绚丽的画卷，勾勒出宁静与和谐的生活。窗外的世界，如此美好！

Outside the window, the sun shines on the lush green leaves, while a gentle breeze caresses the cloud-like blossoms. The birds sing joyfully, seemingly narrating the wonders of nature. These scenes, like a magnificent painting, depict a life of tranquility and harmony. The world outside the window is truly beautiful!
```

### 3. Rust

```rust
#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv()?;
    let template =
        "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"
            .to_string();
    let variables = vec!["title".to_string()];
    let mut args = PromptArgs::new();
    args.insert("title", "窗外");
    let prompt_template = PromptTemplate::new(template, variables, TemplateFormat::FString);
    let text = prompt_template.format(args)?;

    let openai = OpenAI::default();
    let result = openai.generate(&text).await?;
    print!("{:#?}", result.generation);
    Ok(())
}
```

```sh
窗外的世界充满了生机和活力。阳光洒在绿树上，微风轻拂着花朵。小鸟在天空中欢快地歌唱，给大地带来了春天的气息。这个美丽的景象让心情愉悦，仿佛世界都变得更加美好了。

The world outside the window is full of vitality and vigor. The sunlight sprinkles on the green trees, and the breeze gently brushes the flowers. Birds sing joy.
```

### 4. Go

```go
func main() {
 ctx := context.Background()
 llm, err := ollama.New(ollama.WithModel("qwen2.5"))
 if err != nil {
  log.Fatal(err)
 }
 prompt := prompts.PromptTemplate{
  Template:       "你是顶级的短片作家，请根据{{.title}}的内容，写一篇50字的精品短文，然后翻译成英文。",
  InputVariables: []string{"title"},
  TemplateFormat: prompts.TemplateFormatGoTemplate,
 }
 result, err := prompt.Format(map[string]any{
  "title": "窗外",
 })
 if err != nil {
  log.Fatal(err)
 }
 completion, err := llms.GenerateFromSinglePrompt(ctx, llm, result)
 if err != nil {
  log.Fatal(err)
 }
 fmt.Println("Response:\n", completion)
}
```

### 5. Dart

```dart
main(List<String> args) async {
  final prompt = PromptTemplate.fromTemplate(
      "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。");
  final llm = ChatOllama();
  final runnableLlm =
      llm as Runnable<PromptValue, BaseLangChainOptions, Object?>;
  final chain = prompt.pipe(runnableLlm);
  final result =
      await chain.invoke({"title": "窗外"}) as LanguageModelResult<Object>;
  print(result.generations[0].output);
}
```

```sh
标题：春天的绽放

春风轻柔地吹拂着大地，万物苏醒。细嫩的枝叶迎着太阳微笑绽放，花朵争相绽放，予人惊艳的美景。阳光温暖地洒在大地上，金黄的麦田翠绿欲滴，阳台上的花朵散发出迷人的芳香。春天，是大自然的画家，也是生命的奇迹，让我们为春天的绽放欢呼！

Translation：

Title: The Blooming of Spring

The gentle spring breeze brushes the earth as everything awakens. Tender branches smile and bloom against the sun, while flowers vie for attention, presenting stunning views. The warm sunlight pours onto the land, turning the golden wheat fields into lush greens, and balcony flowers release captivating fragrances. Spring, the artist of nature and a miracle of life, let us cheer for the blooming of spring!
```

```sh
窗外阳光明媚，鲜花盛开。鸟儿欢快地跳跃，小动物们在草地上嬉戏。一棵高大的树在微风中舒展枝叶，为这个美丽的世界增添了绿意。这个窗外的景象宛如一幅生动的画卷，让人心旷神怡。

Outside the window, the sun is shining brightly with vibrant flowers blooming. Birds are happily hopping, and small animals play on the grass. A tall tree stretches its branches and leaves in the gentle breeze, adding a touch of green to this beautiful world. The view outside the window is like a vivid painting, bringing a sense of tranquility and joy.
```

### 6. Node.js

```javascript
const prompt = ChatPromptTemplate.fromMessages([
  [
    "human",
    "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。",
  ],
]);
const model = new Ollama({ model: "qwen2.5" });
const outputParser = new StringOutputParser();
const chain = prompt.pipe(model).pipe(outputParser);
const response = await chain.invoke({
  title: "窗外",
});
console.log(response);
```

```sh
窗外，立秋之时，金色的阳光洒满大地。一树树的绿叶轻轻摇曳，和风微拂，如诗如画。小鸟在空中飞翔，欢快地歌唱。这是大自然的交响乐，美妙而神奇。

Outside the window, as autumn begins, golden sunlight bathes the earth. The green leaves of trees sway gently, kissed by a gentle breeze, creating a picturesque sight. Birds soar through the sky, singing joyfully. This is nature’s symphony, enchanting and marvelous.
```
