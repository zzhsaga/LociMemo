# components.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage


def display_chat(chat_history):
    # Display chat history in column 1
    for message in chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)


def handle_sentence_editing(sentences, to_remove):
    # Edit and remove sentences in column 2
    for i, sentence in enumerate(sentences):
        sentences[i] = st.text_input(f"Sentence {i+1}", value=sentence, key=f"text_{i}")
        to_remove[i] = st.checkbox("Remove", value=to_remove[i], key=f"remove_{i}")

    if st.button("Update"):
        # Remove sentences marked for removal
        return [s for i, s in enumerate(sentences) if not to_remove[i]], [False] * len(
            sentences
        )
    else:
        return sentences, to_remove
