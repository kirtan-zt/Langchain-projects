# Build a retriever using LangChain’s API, swap between vector DB backends and verify results.​

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Load the PDF 
loader = PyPDFLoader("reference.pdf")
docs = loader.load()

# Split into overlapping chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)

# Initialize the Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Build the vector store
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
print("Indexing Complete. System Ready.\n")

# Define the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    streaming=True
)

# Prompt template
template = """
SYSTEM: You are a question-answering assistant. Use ONLY the provided context to answer the question. 
If you don't know the answer based on the context, respond with "I do not know."

QUESTION: {question}
CONTEXT: {context}
"""
prompt = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG chain
chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

question = input("enter a question to ask from pdf \n")

# Swap between vector db and test results
docs = retriever.invoke(question)
print(f"\n--- Verification: Retrieved {len(docs)} chunks ---")
for i, doc in enumerate(docs):
    page = doc.metadata.get('page', 'Unknown')
    print(f"Chunk {i+1} (Page {page}): {doc.page_content[:150]}...")

print(f"User query: {question}")
print("Analyzing the question and retrieving the answer...", end="\r", flush=True)

# Generate response
response = chain.invoke(question)

print(" " * 50, end="\r") 
print(f"\nAI Response:\n{response}")