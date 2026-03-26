# 🤖 LangGraph Chatbot

An AI-powered conversational chatbot built with **LangGraph**, **Groq LLM**, and **Tavily Web Search** — capable of answering real-time questions by searching the internet.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-latest-green?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-llama--3.3--70b-orange?style=flat-square)
![Tavily](https://img.shields.io/badge/Tavily-Search-purple?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## 📌 Overview

This chatbot uses a **ReAct-style agent loop** — it reasons, decides whether to call a web search tool, and responds — all orchestrated through LangGraph's `StateGraph`. Powered by Groq's blazing-fast `llama-3.3-70b-versatile` model.

---

## ✨ Features

- 💬 Conversational AI via Groq's `llama-3.3-70b-versatile`
- 🔍 Real-time web search using Tavily Search API
- 🔁 Stateful agent graph with LangGraph `StateGraph`
- 🧠 Conditional routing — agent decides when to search vs. respond directly
- 🔐 Secure API key management via `.env`
- 🏗️ Clean object-oriented `chatbot` class design

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | Groq — `llama-3.3-70b-versatile` |
| Agent Framework | LangGraph (StateGraph) |
| Web Search | Tavily Search API |
| LLM Integration | LangChain + `langchain-groq` |
| Env Management | `python-dotenv` |

---

## 📁 Project Structure

```
langgraph-chatbot/
├── bot.py              # Main chatbot implementation
├── .env                # API keys (not committed to git)
├── .env.example        # Template for environment variables
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## ✅ Prerequisites

- Python 3.9+
- Groq API Key — get one free at [console.groq.com](https://console.groq.com)
- Tavily API Key — get one free at [app.tavily.com](https://app.tavily.com)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langgraph-chatbot.git
cd langgraph-chatbot
```

### 2. Install Dependencies

```bash
pip install langchain-groq langgraph langchain-tavily python-dotenv
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run the Chatbot

```bash
python bot.py
```

---

## ⚙️ How It Works

```
User Message
     │
     ▼
┌─────────┐     tool_calls?     ┌───────┐
│  agent  │ ─── YES ──────────► │ tools │
│  (LLM)  │                     │(Tavily│
└─────────┘ ◄── results ─────── │Search)│
     │                          └───────┘
     │ NO tool_calls
     ▼
Final Response
```

1. User message enters the **agent** node
2. LLM decides: respond directly OR call Tavily web search
3. **router_function** checks for tool calls in the response
4. If tool called → runs search → feeds results back to agent
5. Agent generates the final answer

---

## 📖 Code Overview

```python
class chatbot:
    def __init__(self):
        # Initialize Groq LLM
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=...)

    def call_tool(self):
        # Bind Tavily Search to the LLM
        tool = TavilySearch(max_results=2)
        self.llm_with_tool = self.llm.bind_tools([tool])

    def router_function(self, state):
        # Route to tools or END based on LLM output
        if last_message.tool_calls:
            return "tools"
        return END

    def __call__(self):
        # Build and compile the StateGraph
        workflow = StateGraph(MessagesState)
        workflow.add_node("agent", self.call_model)
        workflow.add_node("tools", self.tool_node)
        workflow.add_conditional_edges("agent", self.router_function, ...)
        return workflow.compile()
```

---

## 💡 Usage Example

```python
mybot = chatbot()
app = mybot()

response = app.invoke({
    "messages": ["Who is the current Prime Minister of the UK?"]
})

print(response["messages"][-1].content)
```

---

## 🐛 Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `GROQ_API_KEY not set` | Missing key in `.env` | Add `GROQ_API_KEY` to `.env` |
| `TAVILY_API_KEY not set` | Missing key in `.env` | Add `TAVILY_API_KEY` to `.env` |
| `model_decommissioned (400)` | Old model name used | Switch to `llama-3.3-70b-versatile` |
| `TavilySearchResults deprecated` | Old import from `langchain_community` | Use `from langchain_tavily import TavilySearch` |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ using LangGraph · Groq · Tavily</p>
