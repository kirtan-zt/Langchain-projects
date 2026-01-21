from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from src.core.config import settings

# Initialize OpenAI Embeddings
embeddings_model = HuggingFaceEmbeddings(model=settings.EMBEDDING_MODEL)

def get_vector_store(table_name: str):
    return PGVector(
        embeddings=embeddings_model,
        collection_name=table_name,
        connection=settings.SYNC_CONNECTION_STRING,
        use_jsonb=True,
    )

def prepare_job_text(job):
    return f"Title: {job.title}. Location: {job.location}. Description: {job.description}. Salary: {job.salary_range}"

def prepare_seeker_text(seeker):
    return f"Skills: {seeker.skill_set}. Experience: {seeker.past_experience}. Location: {seeker.location}"