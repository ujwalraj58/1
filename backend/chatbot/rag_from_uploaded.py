import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import OpenAI

pdf_path = "chatbot/static/data/AI Chatbot for Student Assistance.pdf"

if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"File not found: {pdf_path}")

loader = PyPDFLoader(pdf_path)

def get_answer_from_file(file_path, question):
    if not file_path.endswith(".pdf"):
        raise Exception("Only PDF files are supported for now.")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever()
    relevant_docs = retriever.get_relevant_documents(question)

    llm = OpenAI(temperature=0)  # replace with your preferred LLM
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=relevant_docs, question=question)

    return result
