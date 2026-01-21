from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.core.database import db 
from src.models.jobListings import Listings
from src.crud.ai_search import embeddings
from langchain_postgres import PGVector
from src.core.config import settings

async def sync_listings_to_vector_db():
    # Connect to the Vector Store
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.vector_store_collection_name, 
        connection=settings.SYNC_CONNECTION_STRING,
        use_jsonb=True,
    )

    # Fetch listings with Company data loaded
    async with db._session_factory() as session:
        statement = select(Listings).options(selectinload(Listings.company))
        result = await session.execute(statement)
        listings = result.scalars().all()

        documents = []
        metadatas = []
        ids = []

        for job in listings:
            job_title = getattr(job, 'title', 'Unknown Role') 
            job_desc = getattr(job, 'description', '')
            company_name = job.company.name if job.company else "Unknown Company"
    
            content = (
                f"Role: {job_title}. "
                f"Company: {company_name}. "
                f"Location: {job.location}. "
                f"Details: {job_desc}"
            )
    
            documents.append(content)
            metadatas.append({
                "listing_id": job.listing_id,
                "company": company_name,
                "location": str(job.location)
            })
            ids.append(str(job.listing_id))

        # Add to Vector Store
        if documents:
            vector_store.add_texts(texts=documents, metadatas=metadatas, ids=ids)
            return len(documents)
            
    return 0