import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

# Load environment variable from .env file
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
llm_name = "gpt-3.5-turbo"
client = OpenAI(api_key=openai_key)
model = ChatOpenAI(api_key=openai_key, model=llm_name)

# STEP 1: Build a Basic Chatbot

from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated
class State(TypedDict):
    messages: Annotated[list, add_messages]

def bot(state:State):
    #print(state.items())
    print(state["messages"])
    return { "messages": [model.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("bot", bot)

graph_builder.set_entry_point("bot")

graph_builder.set_finish_point("bot")

graph = graph_builder.compile()

# res = graph.invoke({"messages": ["Hello, how are you ?"]})
# print(res["messages"])

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodby!")
        break
    for event in graph.stream({"messages": ("user", user_input)}):
        for value in event.values():
            print("Assistant:", value["messages"][-1])