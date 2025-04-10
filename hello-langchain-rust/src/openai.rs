use langchain_rust::chain::{Chain, LLMChainBuilder};
use langchain_rust::llm::{OpenAI, OpenAIConfig};
use langchain_rust::prompt::HumanMessagePromptTemplate;
use langchain_rust::schemas::Message;
use langchain_rust::{fmt_message, fmt_template, message_formatter, prompt_args, template_fstring};
use std::collections::HashMap;

#[tokio::main]
async fn main() {
    let model = build_model();

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

    // called `Result::unwrap()` on an `Err` value: LLMError(OpenAIError(JSONDeserialize(Error("missing field `object`", line: 1, column: 584))))
    let resp = chain
        .invoke(prompt_args! {
            "title" => "窗外"
        })
        .await
        .unwrap();
    println!("{}", resp);
}

pub fn build_model() -> OpenAI<OpenAIConfig> {
    // Using OpenAI's endpoint structure which LangChain expects
    let mut headers = HashMap::new();
    // Add custom headers for Zhipu AI compatibility
    headers.insert("Accept".to_string(), "application/json".to_string());

    let config = OpenAIConfig::default()
        .with_api_key("5b7ce4e838e088c6f25358fa2972fd58.Ms4ACrwG3jQ97yma")
        .with_api_base("https://open.bigmodel.cn/api/paas/v4".to_string());

    OpenAI::new(config)
        // Use explicit model name
        .with_model("GLM-4-Plus".to_string())
}
