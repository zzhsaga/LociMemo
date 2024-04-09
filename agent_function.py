# chat_utils.py

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")


def get_response(user_query: str, chat_history: str) -> str:
    # Define the prompt template
    template = """
    You are a helpful assistant. Answer the following questions like a real human and considering the context of the chat history if needed.

    Chat history: {chat_history}
    User question: {user_query}

    Ask the user to get more information about the problem if you need it.
    """
    prompt = ChatPromptTemplate.from_template(template)

    # Initialize the ChatGroq instance
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="mixtral-8x7b-32768",
        temperature=0.0,
    )

    # Chain the components and get the response
    chain = prompt | llm | StrOutputParser()
    result = chain.stream({"chat_history": chat_history, "user_query": user_query})
    print(result)
    return result


def extract_info(chat_history: str) -> str:
    # Placeholder function to extract info from chat history
    return ""
