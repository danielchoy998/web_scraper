import os
from langgraph.graph import StateGraph, START 
from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from dotenv import load_dotenv
from tools import Tools

load_dotenv()

class State(TypedDict): 
    messages: Annotated[list[dict], add_messages]

graph_builder = StateGraph(State)

llm = init_chat_model("openai:gpt-4.1")

tool_list = Tools()
tools = tool_list.get_tools
 
llm_with_tools = llm.bind_tools(tools)
def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1

    return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

def stream_graph_updates(user_input: str): # stream the graph updates to the console
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
         for value in event.values():
            print("Assistant:", value["messages"][-1].content)

def main():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break

if __name__ == "__main__":
    main()

