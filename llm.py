def generate_response(messages):

    latest_message = messages[-1]["content"].lower()

    if "what is my name" in latest_message:

        for msg in messages:

            if "my name is" in msg["content"].lower():

                name = msg["content"].split("my name is")[-1].strip()

                return f"Your name is {name}"

    return f"You said: {messages[-1]['content']}"