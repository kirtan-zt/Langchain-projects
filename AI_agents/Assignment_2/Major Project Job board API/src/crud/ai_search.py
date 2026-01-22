from typing import List
from pydantic import BaseModel, Field
from enum import Enum
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from src.core.config import settings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Pydantic response models for job recommendations
class JobMatch(BaseModel):
    job_title: str
    match_reason: str
    confidence_score: int

class RecommendationResponse(BaseModel):
    recommendations: List[JobMatch]

class ImprovementModes(str, Enum):
    SHORT="SHORT AND CRISP"
    DETAILED="DETAILED AND FORMAL"
    MARKETING="MARKETING ORIENTED"

class ImprovementResponse(BaseModel):
    improved_description: str = Field(description="The rewritten job description text")
    clarity_improvements: str = Field(description="Summary of clarity fixes")
    grammar_fixes: str = Field(description="Summary of grammar corrections")
    professionalism_score: str = Field(description="Critique of the professional tone")
    seo_keywords_added: list[str] = Field(description="List of SEO keywords incorporated")

# Setup Embeddings & LLM
embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
llm = init_chat_model(
            model=settings.LLM_MODEL,
            model_provider=settings.LLM_PROVIDER,
            temperature=0,
            api_key=settings.GROQ_API_KEY
        )

# Setup Vector Store 
vector_store = PGVector(
    connection=settings.SYNC_CONNECTION_STRING, 
    collection_name=settings.vector_store_collection_name,
    embeddings=embeddings
)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5, 
        "score_threshold": 0.25
    }
)

# Prompt template
template = """
You are a Job Board assistant. Based ONLY on the following context, list the matching jobs. 
Provide the details clearly.

Context:
{context}

Question: {question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    if not docs:
        return "NO_DATA"
    return "\n\n".join(doc.page_content for doc in docs)

# Create the Base Chain
base_rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def get_ai_response(query: str):
    # Fetch documents manually to check existence
    docs = retriever.invoke(query)
    
    # Strict check for empty results
    if not docs or len(docs) == 0:
        return {
            "status": "Not found",
            "answer": f"No results found for the '{query}' in our database."
        }
    
    # If docs exist, run the chain
    response = base_rag_chain.invoke(query)
    
    return {
        "status": "success",
        "answer": response
    }

def get_job_recommendations(resume_text: str):
    """Job recommendation service to match resumes with jobs

    Args:
        resume_text (str): Input text for profile or resume

    Returns:
        LLM Response: JSON array of job recommendation text
    """
    docs_with_scores = vector_store.similarity_search_with_relevance_scores(resume_text, k=5)
    
    filtered_docs = [doc for doc, score in docs_with_scores if score >= 0.45]

    if not filtered_docs:
        return {"recommendations": []}

    # Prepare the LLM for structured output
    parser = JsonOutputParser(pydantic_object=RecommendationResponse)
    
    prompt = ChatPromptTemplate.from_template(
        "You are an expert recruiter. Analyze the provided resume against the retrieved job listings.\n"
        "For each listing, explain why it matches the candidate's profile and provide a confidence score (0-100).\n"
        "{format_instructions}\n\n"
        "Resume:\n{resume}\n\n"
        "Job Listings:\n{context}\n"
    )

    # Build the context from retrieved jobs
    context = ""
    for doc, score in docs_with_scores:
        context += f"- {doc.page_content}\n"

    # Invoke LLM
    chain = prompt | llm | parser
    response = chain.invoke({
        "resume": resume_text,
        "context": context,
        "format_instructions": parser.get_format_instructions()
    })

    return response

def get_improvement_suggestions(job_description: str, mode: ImprovementModes):
    """Recruiters get AI assistance directly inside the platform.

    Args:
        job_description (str): Raw job description containing minor flaws 

    Returns:
        LLM response: A clean, structured output with SEO keyword richness, correct grammar, etc.
    """
    # Prepare the LLM for structured output
    parser = JsonOutputParser(pydantic_object=ImprovementResponse)

    prompt=ChatPromptTemplate.from_template(
    """
    You are a professional Paraphraser assistant and SEO specialist.\n
    Rewrite the following job description to improve its quality while following the requested style: {mode}.\n
    Ensure the output addresses clarity, grammar, and professionalism.\n\n
    {format_instructions}\n\n
    Raw Job Description:\n{context}
    """
    )

    chain = prompt | llm | parser

    response = chain.invoke({
        "context": job_description,
        "mode": mode.value,
        "format_instructions": parser.get_format_instructions()
    })

    return response
