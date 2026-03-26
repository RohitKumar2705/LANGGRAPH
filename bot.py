# bot.py
from dotenv import load_dotenv
load_dotenv()  # loads .env into process environment
import os
print("GROQ_API_KEY:", bool(os.getenv("GROQ_API_KEY")))
from langgraph.graph import StateGraph,MessagesState, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, Literal, TypedDict
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults





class chatbot:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. "
                "Set environment variable or provide api_key directly."
            )

        self.llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            api_key=api_key,
        )

    def call_tool(self):
        tool = TavilySearchResults(max_results=2)
        tools = [tool]
        self.tool_node = ToolNode(tools=tools)
        self.llm_with_tool = self.llm.bind_tools(tools)

    def call_model(self, state: MessagesState):
        messages = state["messages"]
        response = self.llm_with_tool.invoke(messages)
        return {"messages": [response]}

    def router_function(self, state: MessagesState) -> str:
        messages = state["messages"]
        last_message = messages[-1]
        if getattr(last_message, "tool_calls", None):
            return "tools"
        return END

    def __call__(self):
        self.call_tool()
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tool_node)
        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            self.router_function,
            {"tools": "tools", END: END},
        )
        workflow.add_edge("tools", "agent")
        self.app = workflow.compile()
        return self.app


if __name__ == "__main__":
    print("Ensuring GROQ_API_KEY is set...")
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY missing. "
            "Set environment variable and rerun."
        )

    mybot = chatbot()
    workflow = mybot()
    response = workflow.invoke(
        {"messages": ["who is the current prime minister of the USA?"]}
    )
    print(response["messages"][-1].content)