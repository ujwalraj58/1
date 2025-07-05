import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from chatbot.models import ChatHistory

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")

def create_vectorstore_from_pdf(pdf_path: str):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(docs, embedding=embeddings)

    return vectorstore.as_retriever()

def get_qa_chain(retriever):
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=OPENAI_API_KEY,
        model_name="mistralai/mistral-7b-instruct:free"
    )
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

def handle_user_query(user_input, retriever, session_id):
    qa_chain = get_qa_chain(retriever)
    result = qa_chain(user_input)

    answer = result["result"]
    source_docs = result.get("source_documents", [])
    sources = "\n".join([doc.metadata.get("source", "Unknown") for doc in source_docs])
    token_count = len(user_input.split()) + len(answer.split())

    ChatHistory.objects.create(
        session_id=session_id,
        user_input=user_input,
        bot_response=answer,
        source_documents=sources,
        tokens_used=token_count,
    )

    return answer
