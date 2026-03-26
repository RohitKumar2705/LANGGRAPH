
import os
os.environ["GROQ_API_KEY"] = "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"
from langchain_groq import ChatGroq
llm = ChatGroq(model_name = "llama3-70b-8192")

# !pip install langgraph

from langchain_groq import ChatGroq

llm = ChatGroq(model_name="llama-3.3-70b-versatile")  # Recommended replacement

llm.invoke("hi").content

from langgraph.graph import StateGraph, MessagesState,START,END
from langgraph.graph.message import add_messages
from typing import Annotated,Literal,TypedDict
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.prebuilt import ToolNode

def call_model(state:MessagesState):
  messages = state['messages']
  response = llm.invoke(messages)
  return {"messages":[response]}

workflow = StateGraph( MessagesState)
workflow.add_node("chatbot",call_model)
workflow.add_edge(START,"chatbot")
workflow.add_edge("chatbot",END)
app = workflow.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

from langchain_core.messages import AnyMessage
from typing import Annotated,TypedDict
from langgraph.graph.message import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

input = {"messages":["hi, my name is Rohit"]}

app.invoke(input)

for output in app.stream(input):
  for key,value in output.items():
    print(f"Output from {key} Node")
    print("_______")
    print(value)
    print("\n")

@tool
def search(query:str):
  """this is my custom tool."""
  if "sf" in query.lower() or "san francisco" in query.lower():
        return "It's 60 degrees and foggy."
  return "It's 90 degrees and Rohit."

search.invoke("what is a temprature in sf?")

search.invoke("what is a weather in india?")

search

tools = [search]

tool_node = ToolNode(tools)

llm_with_tool = llm.bind_tools(tools)

def call_model(state:MessagesState):
  messages = state['messages']
  response = llm_with_tool.invoke(messages)
  return {"messages": [response]}

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Update the model here
llm = ChatGroq(model_name="llama-3.3-70b-versatile")

def call_model(state):
    messages = state["messages"]
    # Handle both plain strings and message objects
    if isinstance(messages[0], str):
        messages = [HumanMessage(content=m) for m in messages]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Test it
response = call_model({"messages": ["hi how are you?"]})
print(response["messages"][0].content)

messages = response['messages']

last_messages=messages[-1]

last_messages.tool_calls

def router_function(state:MessagesState)->Literal["tools", END]:
  messages = state['messages']
  last_message = messages[-1]
  if last_messages.tool_calls:
    return "tools"
  return END

# DEFINE A GRAPH
workflow = StateGraph(MessagesState)
workflow.add_node("agent",call_model)
workflow.add_node("tools",tool_node)
workflow.add_edge(START,"agent")
workflow.add_conditional_edges("agent",router_function,{"tools": "tools", END: END})
app = workflow.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

app.invoke({"messages": ["hi how are you?"]})

app.invoke({"messages": ["what is the weather in sf"]})

workflow.add_edge("tools", 'agent')

app = workflow.compile()

from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))

for output in app.stream({"messages": ["what is the weather in sf"]}):
    for key,value in output.items():
        print(f"here is output from {key}")
        print("_______")
        print(value)
        print("\n")

from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# Define a new graph
workflow3 = StateGraph(MessagesState)

workflow3.add_node("agent", call_model)
workflow3.add_node("tools", tool_node)

workflow3.add_edge(START, "agent")

workflow3.add_conditional_edges("agent",router_function,{"tools": "tools", END: END})

workflow3.add_edge("tools", 'agent')

app3 = workflow3.compile(checkpointer = memory)

from IPython.display import Image, display

try:
    display(Image(app3.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

config = {"configurable": {"thread_id": "1"}}

events = app3.stream(
    {"messages": ["Hi there! My name is Sunny."]}, config, stream_mode="values"
)

for event in events:
    event["messages"][-1].pretty_print()

events = app3.stream(
    {"messages": ["can you tell me what was my name?"]}, config, stream_mode="values"
)

for event in events:
    event["messages"][-1].pretty_print()

memory.get(config)