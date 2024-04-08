# Import necessary libraries
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from datetime import date

# Load environment variables and set configuration
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
groq_api_key = os.environ.get("GROQ_API_KEY")
today = date.today().strftime("%B %d, %Y")

# Set Streamlit page configuration
st.set_page_config(
    page_title="Streamlit Bot",
    page_icon=":robot_face:",
    layout="wide",
)


# Functions
def get_response(user_query: str, chat_history: str) -> str:
    """Get response from AI based on the user query and chat history."""
    template = """
    You are a helpful assistant. Answer the following questions like a real human and considering the context of the chat history if needed.

    Chat history: {chat_history}
    User question: {user_query}

    Ask the user to get more information about the problem if you need it.
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGroq(
        groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768", temperature=0.0
    )
    chain = prompt | llm | StrOutputParser()
    return chain.stream({"chat_history": chat_history, "user_query": user_query})


def extract_info(chat_history: str) -> str:
    """Extract additional info from the chat history."""
    return ""


# Streamlit app layout
st.title("Streamlit Bot")

# Session state initialization for chat history and sentences
if "chat_history" not in st.session_state:
    initial_message = f"Hi! Today is {today}. How can I help you?"
    st.session_state.chat_history = [AIMessage(content=initial_message)]

if "sentences" not in st.session_state:
    st.session_state["sentences"] = []
if "to_remove" not in st.session_state:
    st.session_state["to_remove"] = []

# Display chat history and handle sentence editing
col1, col2 = st.columns([5, 2])

# Display chat history
with col1:
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)

# Handle sentence editing
with col2:
    for i, sentence in enumerate(st.session_state.sentences):
        st.session_state.sentences[i] = st.text_input(
            f"Sentence {i+1}", value=sentence, key=f"text_{i}"
        )
        st.session_state.to_remove[i] = st.checkbox(
            "Remove", value=st.session_state.to_remove[i], key=f"remove_{i}"
        )

    if st.button("Update"):
        # Update logic for sentences
        st.session_state.sentences = [
            s
            for i, s in enumerate(st.session_state.sentences)
            if not st.session_state.to_remove[i]
        ]
        st.session_state.to_remove = [False] * len(st.session_state.sentences)
        st.experimental_rerun()

    st.subheader("Updated Sentences")
    st.write(st.session_state.sentences)

# Handle new user input
user_query = st.chat_input("Your message", key="user_input")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    ai_response = get_response(user_query, st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=ai_response))

    # Display new messages
    with col1:
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            st.write(ai_response)

    # Debug: Print chat history to the console
    print(st.session_state.chat_history)
