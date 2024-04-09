# Import necessary libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os, pymongo
from datetime import date
from pymongo import MongoClient
from agent_function import get_response
from components import display_chat, handle_sentence_editing
from db_handler import insert_memo, fetch_or_create_memo

load_dotenv()
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "Project_Temp_1"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")
os.environ["MONGODB_URI"] = os.environ.get("MONGO_URI")
groq_api_key = os.environ.get("GROQ_API_KEY")

today = date.today().strftime("%B %d, %Y")

initial_message = fetch_or_create_memo(today)["content"]
if not initial_message:
    memo = [AIMessage(content=f"Hi! Today is  {today}   How can I help you?")]
else:
    history = initial_message.split("|")
    memo = [""] * len(history)
    for i in range(len(history)):
        if i % 2 == 0:
            memo[i] = HumanMessage(content=history[i])
        else:
            memo[i] = AIMessage(content=history[i])


st.set_page_config(page_title="Streamlit Bot", page_icon=":robot_face:", layout="wide")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = memo
if "sentences" not in st.session_state:
    st.session_state["sentences"] = []
if "to_remove" not in st.session_state:
    st.session_state["to_remove"] = []

st.title("Streamlit Bot")

# Display chat history and handle sentence editing
col1, col2 = st.columns([5, 2])

# Display chat history
with col1:
    display_chat(st.session_state.chat_history)

# Handle sentence editing
with col2:
    handle_sentence_editing(st.session_state.sentences, st.session_state.to_remove)

# Handle new user input

user_query = st.chat_input("Your message")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with col1:
        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            ai_response = st.write_stream(
                get_response(user_query, st.session_state.chat_history)
            )

    st.session_state.chat_history.append(AIMessage(content=ai_response))

    memo_string = "|".join(
        [message.content for message in st.session_state.chat_history]
    )
    # print(str(st.session_state.chat_history))
    insert_memo(memo_string, today)
