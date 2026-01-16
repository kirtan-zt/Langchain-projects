# Task: Build a retriever using LangChain’s API, swap between vector DB backends and verify results.​

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_community.vectorstores import FAISS

load_dotenv()

# Load and Split PDF
loader = PyPDFLoader("reference.pdf")
docs = loader.load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)

# Setup Embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize Backends
persist_path = os.path.join(os.path.dirname(__file__), "db", "chroma_db_with_metadata")
db_chroma = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_path)
db_faiss = FAISS.from_documents(chunks, embeddings)

# Optimized Query Function
def query_vector_store(vector_store, query, search_type="similarity", k=3):
    """
    Unified query function for any LangChain vector store.
    """
    retriever = vector_store.as_retriever(search_type=search_type, search_kwargs={"k": k})
    relevant_docs = retriever.invoke(query)
    
    print(f"\n--- Results for {type(vector_store).__name__} ({search_type}) ---")
    for i, doc in enumerate(relevant_docs, 1):
        source = doc.metadata.get('page', doc.metadata.get('source', 'N/A'))
        print(f"[{i}] (Page/Source: {source}): {doc.page_content[:180]}...")

# Swapping Backends
user_query = "What is the difference between references and bibliographies?"

# Test Chroma (Standard Similarity)
query_vector_store(db_chroma, user_query, search_type="similarity")

# Test FAISS (Max Marginal Relevance)
query_vector_store(db_faiss, user_query, search_type="mmr")