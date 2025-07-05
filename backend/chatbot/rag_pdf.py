# chatbot/rag_pdf.py
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Set up LLM
llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Define function to load PDF and create FAISS index
def load_pdf_and_create_vectorstore(pdf_path="chatbot/syllabus.pdf"):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1"
    )
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore

# Create RAG-based question answering
def answer_from_pdf(question: str, pdf_path="chatbot/syllabus.pdf"):
    vectorstore = load_pdf_and_create_vectorstore(pdf_path)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
    return qa.run(question)
