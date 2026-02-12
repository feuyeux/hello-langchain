import os
from openai import OpenAI


def create_client():
    """Create OpenAI client for Alibaba Cloud DashScope"""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")
    
    return OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )


def create_image_message(image_url: str, text: str):
    """Create a message with image and text"""
    return [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": text},
            ],
        }
    ]


def stream_completion(client, model: str, messages: list):
    """Stream completion and print results"""
    print("Streaming output:")
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end='', flush=True)
    print()


def normal_completion(client, model: str, messages: list):
    """Get normal completion and print result"""
    print("Normal output:")
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
    print(completion.choices[0].message.content)


def demo_streaming():
    """Demo: Streaming mode"""
    print("=== Demo 1: Streaming Mode ===\n")
    
    IMAGE_URL = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
    QUESTION = "图中描绘的是什么景象?"
    
    client = create_client()
    messages = create_image_message(IMAGE_URL, QUESTION)
    stream_completion(client, "qwen3-vl-plus", messages)


def demo_normal():
    """Demo: Normal mode"""
    print("\n=== Demo 2: Normal Mode ===\n")
    
    IMAGE_URL = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
    QUESTION = "图中描绘的是什么景象?"
    
    client = create_client()
    messages = create_image_message(IMAGE_URL, QUESTION)
    normal_completion(client, "qwen3-vl-plus", messages)


def main():
    try:
        demo_streaming()
        demo_normal()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
