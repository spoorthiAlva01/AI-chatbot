from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class ChatState(TypedDict):
    message: str
    llm_output: str
    tool_result: Optional[str]


def chatbot_node(state: ChatState):

    print("Running chatbot node")

    return {
        "response": f"User said: {state['message']}"
    }


def calculator_node(state: ChatState):

    print("Running calculator node")

    result = eval(state["message"])

    return {
        "result": result
    }


# router
def route_message(state: ChatState):

    message = state["message"]

    if "*" in message:
        return "calculator"

    return END


graph_builder = StateGraph(ChatState)

graph_builder.add_node(
    "chatbot",
    chatbot_node
)

graph_builder.add_node(
    "calculator",
    calculator_node
)


graph_builder.add_edge(
    START,
    "chatbot"
)


graph_builder.add_conditional_edges(
    "chatbot",
    route_message
)


graph_builder.add_edge(
    "calculator",
    END
)


graph = graph_builder.compile()


result = graph.invoke(
    {
        "message": "27 43"
    }
)

print(result)