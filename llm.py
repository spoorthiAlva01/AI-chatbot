from tools.calculator import calculate


def generate_response(messages):

    latest_message = messages[-1]["content"].lower()

    # calculator tool
    if "*" in latest_message:
        result = calculate(latest_message)
        return f"The answer is {result}"

    # memory retrieval
    if "what is my name" in latest_message:

        for msg in messages:

            content = msg["content"].lower()

            if "my name is" in content:
                name = msg["content"].split("my name is")[-1].strip()
                return f"Your name is {name}"

            elif "i am" in content:
                name = msg["content"].split("I am")[-1].strip()
                return f"Your name is {name}"

    return f"You said: {messages[-1]['content']}"