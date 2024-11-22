use anyhow::Result;
use langchain_rs::llms::OpenAI;
use langchain_rs::prompts::Prompt;
use langchain_rs::prompts::PromptArgs;
use langchain_rs::prompts::PromptTemplate;
use langchain_rs::prompts::TemplateFormat;
use langchain_rs::schema::LLM;

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
