from llm import generate_response
from memory import load_history, save_history

conversation_history = load_history()

while True:

    message = input("You: ")

    conversation_history.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = generate_response(conversation_history)

    conversation_history.append(
        {
            "role": "assistant",
            "content": response
        }
    )

    save_history(conversation_history)

    print("AI:", response)