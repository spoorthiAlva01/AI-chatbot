from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_response(messages):

    system_prompt = """
You are an assistant with access to a calculator.

Rules:
- If math/calculation is required, respond ONLY:
  TOOL: calculator: <expression>

- If no tool is required, answer normally.

Never call tools for greetings like:
"hi", "hello", "hey"
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ] + messages
    )

    return response.choices[0].message.content