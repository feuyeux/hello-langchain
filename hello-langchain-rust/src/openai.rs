use anyhow::Result;
use langchain_rust::chain::{Chain, LLMChainBuilder};
use langchain_rust::llm::OpenAI;
use langchain_rust::schemas::Message;
use langchain_rust::{fmt_message, message_formatter, prompt_args};

#[tokio::main]
async fn main() -> Result<()> {
    dotenvy::dotenv()?;
    let openai = OpenAI::default();

    let prompt = message_formatter![fmt_message!(Message::new_system_message(
        "你是顶级的短片作家，请根据{title}的内容，写一篇50字的精品短文，然后翻译成英文。"
    ))];

    //We can now combine these into a simple LLM chain:

    let chain = LLMChainBuilder::new()
        .prompt(prompt)
        .llm(openai.clone())
        .build()
        .unwrap();

    match chain.invoke(prompt_args! {"title" => "窗外"}).await {
        Ok(result) => {
            println!("Result: {:?}", result);
        }
        Err(e) => panic!("Error invoking LLMChain: {:?}", e),
    }
    Ok(())
}
