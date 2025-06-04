import os
from langgraph.graph import StateGraph, START,END
from typing import TypedDict,Annotated,Literal
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from tools import Tools
from langgraph.types import Command, interrupt
from graph_display import display
from print import print_event
load_dotenv()

class State(TypedDict): 
    messages: Annotated[list[dict], add_messages]

graph_builder = StateGraph(State)

llm = init_chat_model("openai:gpt-4.1")

tool_list = Tools()
tools = tool_list.get_tools
 
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def human_approval(state: State) -> Command[Literal["chatbot", "tools"]]:

    last_messages = state["messages"][-1]
    tool_call = last_messages.tool_calls[-1]

    human_response = interrupt({
        "question": "The assistant wants to execute a tool. Do you approve?",
        "tool_calls": tool_call,
    })

    review_action = human_response["action"]
    if review_action == "approve":
        return Command(goto="tools")
    else:
        return Command(goto="chatbot")

tool_node = ToolNode(tools)

def route_after_llm(state) -> Literal[END, "human_approval"]:
    if len(state["messages"][-1].tool_calls) == 0:
        return END
    else:
        return "human_approval"
    
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("human_approval", human_approval)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    route_after_llm,
)
graph_builder.add_edge("tools", "chatbot")


memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}
graph = graph_builder.compile(checkpointer=memory)

display(graph)

def stream_graph_updates(user_input : dict):
    user_input = {"messages": [{"role": "user", "content": user_input}]}
    for event in graph.stream(user_input,
                            config = config,
                            stream_mode = "values",):
        print_event(event, graph, config)

def main():
   test_input = {"messages": [{"role": "user", "content": "what's the weather in sf?"}]}
   while True:
      user_input = input("User: ")
      if user_input.lower() in ["quit", "exit", "q"]:
         print("Goodbye!")
         break
      stream_graph_updates(user_input)
       

if __name__ == "__main__":
    main()