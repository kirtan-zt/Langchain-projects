# Task: Chain retriever and LLM steps for a customized question-answering prompt; experiment with prompt styles.​

import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Setup Data & Embeddings
loader = PyPDFLoader("reference.pdf")
docs = loader.load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Initialize LLM
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.1, api_key=os.getenv("GROQ_API_KEY"))

# Vector Store Setup
persist_path = os.path.join(os.path.dirname(__file__), "db", "chroma_db_metadata")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_path)

# SUMMARIZATION LOGIC
def summarize_chunks(docs):
    summary_prompt = PromptTemplate.from_template("Summarize the following context into key points for a QA task: {text}")
    summarize_chain = summary_prompt | llm | StrOutputParser()
    summarized_text = ""
    for doc in docs:
        summary = summarize_chain.invoke({"text": doc.page_content})
        summarized_text += f"- {summary}\n"
    return summarized_text

# FULL CONCATENATION
def format_docs_full(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Custom Prompt template
template = """SYSTEM: Use the context to answer the question.
CONTEXT: {context}
QUESTION: {question}
ANSWER:"""
prompt = PromptTemplate.from_template(template)

# RUNNING THE DIFFERENT APPROACHES

user_query = "What is the rule for citing more than two authors?"

# TEST APPROACH 1: Full Chunks
print("\n--- APPROACH 1: FULL CHUNKS ---")
chain_full = (
    {"context": vectorstore.as_retriever() | format_docs_full, "question": RunnablePassthrough()} 
    | prompt | llm | StrOutputParser()
    )
print(chain_full.invoke(user_query))

# TEST APPROACH 2: Summarized Chunks 
print("\n--- APPROACH 2: SUMMARIZED CHUNKS ---")
chain_sum = (
    {"context": vectorstore.as_retriever() | summarize_chunks, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
    )
print(chain_sum.invoke(user_query))

# TEST APPROACH 3: Metadata Filtering 
print("\n--- APPROACH 3: METADATA FILTERING ---")
filtered_retriever = vectorstore.as_retriever(
    search_kwargs={"filter": {"page": 17}} 
)
chain_filter = (
    {"context": filtered_retriever | format_docs_full, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
    )
print(chain_filter.invoke(user_query))