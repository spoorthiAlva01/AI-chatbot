from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END
from tools.calculator import calculate
from llm import generate_response


class ChatState(TypedDict):
    message: str
    llm_output: str
    tool_result: Optional[str]


# Node 1 — Ask LLM what to do
def llm_node(state: ChatState):

    print("Running LLM node")

    response = generate_response(
        [
            {
                "role": "user",
                "content": state["message"]
            }
        ]
    )

    return {
        "llm_output": response
    }

def router_node(state: ChatState):

    llm_output = state["llm_output"]

    if llm_output.startswith("TOOL:"):
        return "tool_executor"

    return END

# Node 2 — Execute requested tool
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
def final_response_node(state: ChatState):

    print("Running final response node")

    tool_result = state["tool_result"]

    response = generate_response(
        [
            {
                "role": "user",
                "content": f"The calculator returned: {tool_result}. Respond naturally to the user."
            }
        ]
    )

    return {
        "llm_output": response
    }


graph_builder = StateGraph(ChatState)

graph_builder.add_node("llm", llm_node)
graph_builder.add_node("tool_executor", tool_executor_node)
graph_builder.add_node("final_response", final_response_node)

graph_builder.add_edge(START, "llm")

graph_builder.add_conditional_edges(
    "llm",
    router_node
)

graph_builder.add_edge("tool_executor", "final_response")

graph_builder.add_edge("final_response", END)

graph = graph_builder.compile()

while True:

    user_message = input("You: ")

    result = graph.invoke(
        {
            "message": user_message
        }
    )

    print("GROQ:", result["llm_output"])

print(result)