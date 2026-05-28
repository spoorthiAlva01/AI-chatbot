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
You are a helpful assistant.

You have access to one tool:

calculator(expression)

If the user asks a math question, respond ONLY in this format:

TOOL: calculator: <expression>

Example:
TOOL: calculator: 27 * 43

For normal conversation, answer normally.
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