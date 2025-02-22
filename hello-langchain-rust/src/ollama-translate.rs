use langchain_rust::chain::{Chain, LLMChainBuilder};
use langchain_rust::llm::client::Ollama;
use langchain_rust::prompt::HumanMessagePromptTemplate;
use langchain_rust::schemas::Message;
use langchain_rust::{fmt_message, fmt_template, message_formatter, prompt_args, template_fstring};

#[tokio::main]
async fn main() {
    let ollama = Ollama::default().with_model("mistral-nemo");

    let prompt = message_formatter![
        fmt_message!(Message::new_system_message(
            "根据{sentence}的内容，翻译成英语和法语，每种语言占一行。"
        )),
        fmt_template!(HumanMessagePromptTemplate::new(template_fstring!(
            "{sentence}",
            "sentence"
        ))),
    ];

    let chain = LLMChainBuilder::new()
        .prompt(prompt)
        .llm(ollama.clone())
        .build()
        .unwrap();

    let sentence = "飞光飞光，劝尔一杯酒。吾不识青天高，黄地厚。";
    let response = chain
        .invoke(prompt_args! {"sentence" => sentence})
        .await
        .unwrap();
    for line in response.lines() {
        println!("{}", line);
    }
}
