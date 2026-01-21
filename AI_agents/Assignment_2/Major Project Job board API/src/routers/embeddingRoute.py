from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.core.database import db  
from src.models.jobListings import Listings  
from src.crud.ai_search import vector_store

router = APIRouter(prefix="/sync", tags=["Search Sync"])

@router.post("/listings/{listing_id}")
async def sync_listing_embedding(listing_id: int):
    async with db._session_factory() as session:
        result = await session.execute(
            select(Listings).filter(Listings.listing_id == listing_id)
        )
        job = result.scalars().first()

        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        text = f"Job Title: {job.title}. Location: {job.location}. Description: {job.description}"
        
        # Sync to the vector store
        vector_store.add_texts(
            texts=[text],
            metadatas=[{"listing_id": job.listing_id, "title": job.title}],
            ids=[str(job.listing_id)]
        )

        return {
            "status": "success", 
            "message": f"Embedding synced for: {job.title}"
        }