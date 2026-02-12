# Requirements: pip install numpy soundfile openai

import os
import base64
import soundfile as sf
import numpy as np
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


def create_text_message(text: str):
    """Create a simple text message"""
    return [{"role": "user", "content": text}]


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


def save_audio(audio_base64: str, output_file: str, sample_rate: int = 24000):
    """Decode and save audio from base64 string"""
    wav_bytes = base64.b64decode(audio_base64)
    audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    sf.write(output_file, audio_np, samplerate=sample_rate)


def stream_omni_completion(client, model: str, messages: list, output_audio: str = None):
    """Stream completion with text and audio output"""
    print("Model response:")
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        modalities=["text", "audio"],
        audio={"voice": "Cherry", "format": "wav"},
        stream=True,
        stream_options={"include_usage": True},
    )
    
    audio_base64_string = ""
    for chunk in completion:
        # Handle text
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
        
        # Collect audio
        if chunk.choices and hasattr(chunk.choices[0].delta, "audio") and chunk.choices[0].delta.audio:
            audio_base64_string += chunk.choices[0].delta.audio.get("data", "")
    
    print()
    
    # Save audio if available
    if audio_base64_string and output_audio:
        save_audio(audio_base64_string, output_audio)
        print(f"Audio saved to: {output_audio}")


def demo_text_to_audio():
    """Demo: Text input -> Text + Audio output"""
    print("=== Demo 1: Text to Audio ===\n")
    
    client = create_client()
    messages = create_text_message("你是谁")
    stream_omni_completion(client, "qwen3-omni-flash", messages, "audio_text.wav")


def demo_image_to_audio():
    """Demo: Image + Text input -> Text + Audio output"""
    print("\n=== Demo 2: Image to Audio ===\n")
    
    IMAGE_URL = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
    QUESTION = "图中描绘的是什么景象？请详细描述一下"
    
    client = create_client()
    messages = create_image_message(IMAGE_URL, QUESTION)
    stream_omni_completion(client, "qwen3-omni-flash", messages, "audio_image.wav")


def main():
    try:
        demo_text_to_audio()
        demo_image_to_audio()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
