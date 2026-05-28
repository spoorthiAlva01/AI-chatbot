from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# shared state
class ChatState(TypedDict):
    message: str
    response: str
    result: int


# node 1
def chatbot_node(state: ChatState):

    print("Running chatbot node")

    return {
        "response": f"User said: {state['message']}"
    }


# node 2
def calculator_node(state: ChatState):

    print("Running calculator node")

    result = eval(state["message"])

    return {
        "result": result
    }


# build graph
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

graph_builder.add_edge(
    "chatbot",
    "calculator"
)

graph_builder.add_edge(
    "calculator",
    END
)

graph = graph_builder.compile()


result = graph.invoke(
    {
        "message": "27 * 43"
    }
)

print(result)