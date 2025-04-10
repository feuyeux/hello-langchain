package main

import (
	"log"
	"os"

	"github.com/tmc/langchaingo/llms/openai"
)

func main() {
	llm, err := buildModel()
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

func buildModel() (*openai.LLM, error) {
	apiKey := os.Getenv("ZHIPUAI_API_KEY")
	baseUrl := "https://open.bigmodel.cn/api/paas/v4"
	return openai.New(
		openai.WithToken(apiKey),
		openai.WithModel("GLM-4-Plus"),
		openai.WithBaseURL(baseUrl),
	)
}
