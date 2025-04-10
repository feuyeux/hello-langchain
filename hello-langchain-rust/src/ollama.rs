use langchain_rust::chain::{Chain, LLMChainBuilder};
use langchain_rust::llm::client::Ollama;
use langchain_rust::prompt::HumanMessagePromptTemplate;
use langchain_rust::schemas::Message;
use langchain_rust::{fmt_message, fmt_template, message_formatter, prompt_args, template_fstring};

#[tokio::main]
async fn main() {
    let model = Ollama::default().with_model("llama3.2");

    let prompt = message_formatter![
        fmt_message!(Message::new_system_message(
            "你是顶级的短片作家，请根据{title}的内容，用中文写一篇50字的精品短文，然后翻译成英文。"
        )),
        fmt_template!(HumanMessagePromptTemplate::new(template_fstring!(
            "{title}", "title"
        ))),
    ];

    let chain = LLMChainBuilder::new()
        .prompt(prompt)
        .llm(model.clone())
        .build()
        .unwrap();

    let title = "窗外";
    let response = chain.invoke(prompt_args! {"title" => title}).await.unwrap();

    for line in response.lines() {
        println!("{}", line);
    }
}
