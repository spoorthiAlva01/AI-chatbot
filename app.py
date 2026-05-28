from llm import generate_response
from memory import load_history, save_history
from graph_bot import graph
history = []

while True:

    user_message = input("You: ")

    history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    result = graph.invoke(
        {
            "message": user_message,
            "history": history
        }
    )

    print("AI:", result["llm_output"])

    history.append(
        {
            "role": "assistant",
            "content": result["llm_output"]
        }
    )