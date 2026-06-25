import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="AI Engineering Agent", page_icon="⚙️", layout="centered")

st.title("⚙️ Smart Engineering Troubleshooting Agent")
st.markdown("Built with **FastAPI, LangGraph, RAG (ChromaDB), and MCP**")
st.divider()

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add a greeting message
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello Engineer! I am connected to the live machine database and technical PDFs. How can I help you today?"
    })

# 3. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle User Input
if prompt := st.chat_input("Ask about machine status or troubleshooting..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show loading spinner while backend thinks
    with st.spinner("AI is analyzing manuals and live data..."):
        try:
            # Send request to your FastAPI backend
            response = requests.post("https://bunnnyyy2005-smart-engineering-rag.hf.space/ask", json={"query": prompt})

            response.raise_for_status()
            
            # Extract the AI's answer
            ai_answer = response.json()["response"]
            
        except requests.exceptions.ConnectionError:
            ai_answer = "❌ Error: Cannot connect to the backend. Is your FastAPI server running?"
        except Exception as e:
            ai_answer = f"❌ Error: {str(e)}"

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(ai_answer)
    st.session_state.messages.append({"role": "assistant", "content": ai_answer})
