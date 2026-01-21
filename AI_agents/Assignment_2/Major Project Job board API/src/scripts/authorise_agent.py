import requests
from src.core.config import settings

_CACHED_TOKEN=None

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_auth_token():
    """
    Retrieves a fresh JWT token by logging in. 
    Caches the token to avoid redundant login calls.
    """
    global _CACHED_TOKEN
    
    if _CACHED_TOKEN:
        return _CACHED_TOKEN

    LOGIN_URL = "http://127.0.0.1:8000/users/login" 
    payload = {
        "username": settings.AGENT_EMAIL,
        "password": settings.AGENT_PASSWORD
    }
    try:
        response = requests.post(LOGIN_URL, data=payload, timeout=5)
        response.raise_for_status()
        token_data = response.json()
        
        _CACHED_TOKEN = token_data.get("access_token")
        return _CACHED_TOKEN
    except Exception as e:
        print(f"Auth Error: Could not retrieve service token: {e}")
        return None
