from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from tools.calculator import calculate

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





def tool_executor_node(state: ChatState):

    print("Running tool executor node")

    llm_output = state["llm_output"]

    if llm_output.startswith("TOOL:"):

        parts = llm_output.split(":")

        tool_name = parts[1].strip()
        tool_input = parts[2].strip()

        if tool_name == "calculator":
            result = calculate(tool_input)

            return {
                "tool_result": str(result)
            }

    return {
        "tool_result": None
    }


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