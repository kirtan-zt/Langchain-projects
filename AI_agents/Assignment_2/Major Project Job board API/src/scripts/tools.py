import requests
import json
from langchain_core.tools import tool
from src.crud.ai_search import vector_store
from src.core.config import settings
from src.scripts.authorise_agent import get_auth_token

AUTH_ERROR_MESSAGE = "Error: Could not authenticate Agent service account."

@tool
def vector_job_search(query: str) -> str:
    """
    Use this tool when you need to find jobs based on semantic meaning or skills 
    (e.g., 'Cloud Computing' or 'Python expert'). Returns best matches from the vector DB.
    """
    docs = vector_store.similarity_search(query, k=3)
    if not docs:
        return "No matching jobs found in Vector DB."
    return "\n\n".join([doc.page_content for doc in docs])

@tool
def list_jobs() -> str:
    """Fetches recently posted jobs from the API to see raw data like dates and IDs."""
    API_URL = "http://127.0.0.1:8000/listings/"

    token = get_auth_token()
    if not token:
        return AUTH_ERROR_MESSAGE
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        jobs = response.json()
        data=[
            {
                "listing_id": job['listing_id'],
                "title": job['title'],
                "Type of work": job['employment'],
                "Status": job['is_active']
            } for job in jobs
        ]
        return json.dumps(data)
    except Exception as e:
        return f"Error: {e}"

@tool
def list_companies() -> str:
    """Fetches all company names with their company_id and industry it operates"""
    API_URL="http://127.0.0.1:8000/companies/"

    token = get_auth_token()
    if not token:
        return AUTH_ERROR_MESSAGE
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response=requests.get(API_URL, headers=headers)
        response.raise_for_status()
        companies=response.json()
        data=[
            {
                "Company name": company['name'],
                "ID": company['company_id'], 
                "Industry": company['industry']
            } for company in companies
        ]
        return json.dumps(data)
    except Exception as e:
        return f"Error: {e}"

@tool
def list_resumes() -> str:
    """Fetches all profile first name with their desired_job_title, past_experience and skillset"""
    API_URL="http://127.0.0.1:8000/seekers/"

    token = get_auth_token()
    if not token:
        return AUTH_ERROR_MESSAGE
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response=requests.get(API_URL, headers=headers)
        response.raise_for_status()
        resumes=response.json()
        data=[
            {
                "name": resume['first_name'], 
                "title": resume['desired_job_title'],
                "past experience": resume['past_experience'], 
                "skills": resume['skill_set']
            } for resume in resumes
        ]
        return json.dumps(data)
    except Exception as e:
        return f"Error: {e}"