from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # API keys (optional for now)
    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None

    # Models
    MODEL_NAME: str = "llama3-70b-8192"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Vector database
    VECTOR_DB_PATH: str = "memory/chroma_db"

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()