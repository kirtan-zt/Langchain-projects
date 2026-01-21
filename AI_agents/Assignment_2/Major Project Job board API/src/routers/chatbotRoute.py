from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from pydantic import BaseModel
from src.crud.ai_search import  (
    get_ai_response, get_job_recommendations, get_improvement_suggestions, ImprovementModes
)
from src.crud.sync_vector_db import sync_listings_to_vector_db
from src.scripts.agent import agent_executor

router = APIRouter(prefix="/ai", tags=["AI"])

# Pydantic model for Q&A in GET /ask-ai route
class ChatRequest(BaseModel):
    message: str

# Pydantic model for AI job recommendation system
class RecommendRequest(BaseModel):
    resume_text: str

# Pydantic model for recruiters to get improvement in job descriptions.
class ImproveDescriptionRequest(BaseModel):
    text: str

@router.post("/ask-agent")
async def ask_agent(query: str):
    """Custom AI agent that fetches real time information from database and helps respond user queries

    Args:
        query (str): User prompt

    Returns:
        LLM response for the user's question.
    """
    try:
        response = agent_executor.invoke({"input": query})
        
        return {
            "status": "success",
            "output": response["output"]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/ask-ai") # Standard RAG endpoint
async def ask_rag_question(query: str = Query(..., description="Ask about jobs or companies")):
    """
    RAG: Directly retrieves context and generates an answer.
    """
    result = get_ai_response(query)
    return result

@router.post("/sync-embeddings")
async def trigger_sync():
    """
    Syncs PostgreSQL data to the Vector Store.
    """
    try:
        count = await sync_listings_to_vector_db()
        return {"status": "success", "synced_records": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sync Error: {str(e)}")

@router.post("/recommend")
async def recommend_jobs(request: RecommendRequest):
    """
    Candidate pastes their resume and receives matching job recommendations.
    """
    try:
        # Generate recommendations based on the resume embedding
        result = get_job_recommendations(request.resume_text)
        
        if not result or not result.get("recommendations"):
            return {
                "status": "Not found",
                "message": "No suitable jobs found matching your profile at this time.",
                "recommendations": []
            }
            
        return {
            "status": "success",
            "recommendations": result["recommendations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation Error: {str(e)}")

@router.post("/improve-description")
async def improve_description(
    request: ImproveDescriptionRequest,
    mode: Annotated[ImprovementModes, Query()] = ImprovementModes.DETAILED
):
    """Generate a well structured response for raw job description

    Args:
        request (ImproveDescriptionRequest): Recruiter's job description that needs polishing

    Raises:
        HTTPException: Empty job description body
        HTTPException: Runtime system error

    Returns:
        Suggestions to improve clarity, grammar, SEO keyword richness in the text.        
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")

    try:
        result = get_improvement_suggestions(request.text, mode)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Improvement Error: {str(e)}")
