package main

import (
	"log"

	"github.com/tmc/langchaingo/llms/ollama"
)

func main() {
	llm, err := ollama.New(buildOllamaModel())
	if err != nil {
		log.Fatal(err)
	}

	infer(
		"你是顶级的短片作家，请根据{{.title}}的内容，写一篇50字的精品短文，然后翻译成英文。",
		map[string]any{
			"title": "窗外",
		},
		llm)
}

func buildOllamaModel() ollama.Option {
	return ollama.WithModel("llama3.2")
}
