from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv 
import urllib

load_dotenv()

# Configuration settings loaded from the environment/.env file.
class Settings(BaseSettings):
    
    APP_NAME: str = "Job Board API"
    ENV_STATE: str = "development"

    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str
    DB_NAME_JOB_BOARD_API: str
    DB_USER: str
        
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    GROQ_API_KEY: str
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # LLM Configuration, Defaulting to Groq/Llama, but can be overridden in .env
    LLM_PROVIDER: str = "groq" 
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    
    # Vector / NLP settings
    CHUNK_SIZE: int = 1000          
    CHUNK_OVERLAP: int = 200       

    # AI-Agent tool calling config
    AGENT_EMAIL: str
    AGENT_PASSWORD: str
    INTERNAL_SERVICE_TOKEN: str
    
    vector_store_collection_name: str = "knowledge_base"
    debug: bool = False

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')
    @property
    def SYNC_CONNECTION_STRING(self) -> str:
        """Dynamically build the connection string after variables are loaded."""
        password_encoded = urllib.parse.quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+psycopg://{self.DB_USER}:{password_encoded}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_JOB_BOARD_API}"
        )

settings = Settings()

BYPASS_MIDDLEWARE_PATHS = [
    r"^/$",
    r"^/users/login/?$", r"^/users/register/?$",
    r"^/companies/?$", r"^/companies/\d+/?$",
    r"^/listings/?$", r"^/listings/\d+/?$",
    r"^/seekers/?$", r"^/seekers/\d+/?$",
    r"^/recruiters/?$", r"^/recruiters/\d+/?$",
]