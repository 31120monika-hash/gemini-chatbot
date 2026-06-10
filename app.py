import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_core.messages import AIMessage, HumanMessage

# ------------------ LOAD ENV ------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ------------------ GEMINI SETUP ------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Gemini AI Chatbot")
st.markdown("Chat with Gemini AI. It remembers your conversation.")

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    else:
        with st.chat_message("assistant"):
            st.write(msg.content)

# ------------------ USER INPUT ------------------
user_input = st.chat_input("Ask Gemini anything...")

if user_input:
    # show user message
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.write(user_input)

    # build context
    chat_history = ""
    for m in st.session_state.messages:
        role = "User" if isinstance(m, HumanMessage) else "Assistant"
        chat_history += f"{role}: {m.content}\n"

    # call Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(chat_history)
                answer = response.text

                st.write(answer)
                st.session_state.messages.append(AIMessage(content=answer))

            except Exception as e:
                st.error(f"Error: {e}")