from sqlalchemy.orm import Session
from src.core.database import SessionLocal
from src.models.jobListings import Listings
from src.models.jobSeekers import JobSeekers
from src.models.companies import Company
from src.crud.embeddings_crud import embeddings_model, prepare_job_text

def rebuild_all_listings():
    """Create and update fresh embeddings for listings"""
    db: Session = SessionLocal()
    jobs = db.query(Listings).all()
    
    for job in jobs:
        text = prepare_job_text(job)
        vector = embeddings_model.embed_query(text)
        job.embedding = vector # Saving directly to the postgres column
    
    db.commit()
    print(f"Successfully rebuilt {len(jobs)} job embeddings.")

if __name__ == "__main__":
    rebuild_all_listings()