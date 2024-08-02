from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "描述图片展示的内容，例如：图片出自北欧的一本画册，画上有两只猫慵懒地躺在沙发里，白色的那只望着窗外，黑色的那只眯着眼。"
        },
        {
            "type": "image_url",
            "image_url": "test/20230502_105954.jpg"
        }
    ]
)
response = llm.invoke([message])
print(response.content)
