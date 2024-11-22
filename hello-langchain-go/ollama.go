package main

import (
	"context"
	"fmt"
	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/ollama"
	"github.com/tmc/langchaingo/prompts"
	"log"
)

func main() {
	ctx := context.Background()
	llm, err := ollama.New(ollama.WithModel("llama3.2"))
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
