import os
import textwrap
import google.generativeai as genai
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is the meaning of life?")

print(to_markdown(response.text))
print(response.prompt_feedback)
print(response.candidates)
