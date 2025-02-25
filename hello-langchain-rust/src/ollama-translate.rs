use env_logger::Builder;
use langchain_rust::chain::{Chain, LLMChainBuilder};
use langchain_rust::llm::client::Ollama;
use langchain_rust::prompt::HumanMessagePromptTemplate;
use langchain_rust::schemas::Message;
use langchain_rust::{fmt_message, fmt_template, message_formatter, prompt_args, template_fstring};
use log::LevelFilter;

fn init_logger() {
    let mut builder = Builder::from_default_env();
    builder
        .filter(None, LevelFilter::Debug) // 设置全局日志级别为 DEBUG
        .init();
}

#[tokio::main]
async fn main() {
    init_logger();

    let ollama = Ollama::default().with_model("mistral-nemo");
    let prompt = message_formatter![
        fmt_message!(Message::new_system_message("将{sentence}翻译成{lang}")),
        fmt_template!(HumanMessagePromptTemplate::new(template_fstring!(
            "将{sentence}翻译成{lang}",
            "sentence",
            "lang"
        ))),
    ];

    let chain = LLMChainBuilder::new()
        .prompt(prompt)
        .llm(ollama.clone())
        .build()
        .unwrap();

    let sentence = "飞光飞光，劝尔一杯酒。吾不识青天高，黄地厚。";
    let language = "英语";
    let input_variables = prompt_args! {
        "sentence" => sentence,
        "lang" => language,
    };

    let response = chain.invoke(input_variables).await.unwrap();
    for line in response.lines() {
        println!("{}", line);
    }
}
