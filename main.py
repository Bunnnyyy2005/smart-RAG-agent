from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from dotenv import load_dotenv

# Modern LangGraph and Stable LangChain Imports
from langchain_groq import ChatGroq
from langchain_core.tools import create_retriever_tool
from langgraph.prebuilt import create_react_agent

# Your Custom Modules
from rag_engine import get_retriever
from mcp_tools import get_live_machine_status

# Load API Key
load_dotenv()

app = FastAPI(
    title="Engineering Smart Agent API",
    description="Bulletproof Backend for AI Troubleshooting Agent"
)

class QueryRequest(BaseModel):
    query: str

# 1. THE BRAIN: Using Mixtral - The most stable model for Tool Calling (No XML Bugs)
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.1-8b-instant", 
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# 2. THE TOOLS: Connecting RAG and MCP
retriever = get_retriever()
rag_tool = create_retriever_tool(
    retriever,
    "engineering_manual_search",
    "Searches technical manuals. Use this strictly when the user asks for theory, disadvantages, comparisons, or troubleshooting procedures."
)

tools = [rag_tool, get_live_machine_status]

# 3. THE AGENT: Clean LangGraph Setup
agent_executor = create_react_agent(llm, tools)

# 4. SYSTEM PROMPT: Strict instructions
SYSTEM_PROMPT = """You are a senior Engineering and AI Troubleshooting AI. 
You have access to technical manuals and a live machine database. 
- Use the live status tool ONLY if asked about a machine's current status. 
- Use the manual search tool if asked about concepts, algorithms, disadvantages, or fixes.
Always provide a clear, professional, and complete answer."""

@app.get("/")
def read_root():
    return {"status": "Backend is running perfectly! 🚀"}

@app.post("/ask")
def ask_agent(request: QueryRequest):  # <-- Removed 'async' here!
    try:
        print(f"🚀 Received question: {request.query}")
        print("🧠 Sending request to Groq API... (Please wait)")
        
        result = agent_executor.invoke({
            "messages": [
                ("system", SYSTEM_PROMPT),
                ("user", request.query)
            ]
        })
        
        print("✅ Received response from Groq!")
        final_answer = result["messages"][-1].content
        
        return {
            "query": request.query,
            "response": final_answer
        }
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)