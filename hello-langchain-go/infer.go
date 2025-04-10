package main

import (
	"context"
	"fmt"
	"log"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/prompts"
)

func infer(template string, mapping map[string]any, llm llms.Model) {
	prompt := prompts.PromptTemplate{
		Template:       template,
		InputVariables: []string{"title"},
		TemplateFormat: prompts.TemplateFormatGoTemplate,
	}
	result, err := prompt.Format(mapping)
	if err != nil {
		log.Fatal(err)
	}
	completion, err := llms.GenerateFromSinglePrompt(
		context.Background(),
		llm,
		result,
		llms.WithTemperature(0.7),
	)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Response:\n", completion)
}
