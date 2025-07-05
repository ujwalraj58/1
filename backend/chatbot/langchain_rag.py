import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import requests # Ensure requests is imported for potential direct API calls if needed for debugging

# Load variables from .env
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print("🔑 Loaded OPENROUTER_API_KEY:", OPENROUTER_API_KEY)

# Use OpenRouter with LangChain-compatible ChatOpenAI
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    openai_api_key=OPENROUTER_API_KEY, # Use the loaded API key directly
    openai_api_base="https://openrouter.ai/api/v1"
)

def get_answer(question):
    print("🟡 Incoming question:", question)
    try:
        # Use llm.invoke to send the question to the configured LLM
        answer = llm.invoke(question)
        print("🟢 Response:", answer)
        return answer
    except Exception as e:
        # Catch any exceptions during the LLM invocation and re-raise with more context
        error_message = f"Error calling LLM: {e}"
        print("🔴 Exception occurred during LLM invocation:", error_message)
        raise Exception(error_message) # Re-raise to be caught by views.py
