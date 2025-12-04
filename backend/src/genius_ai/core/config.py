"""Configuration management for Genius AI."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        protected_namespaces=(),
        extra="allow",  # Allow extra fields like groq_api_key
    )

    # Application
    app_name: str = "Genius AI"
    environment: Literal["development", "production", "testing"] = "development"
    debug: bool = True
    log_level: str = "INFO"
    data_dir: str = "./data"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4

    # Security
    secret_key: str = Field(default="change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/genius_ai"
    redis_url: str = "redis://localhost:6379"

    # Vector Database
    chroma_persist_directory: str = "./data/chroma"
    chroma_collection_name: str = "genius_knowledge"

    # Model Configuration
    base_model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"
    model_cache_dir: str = "./models/cache"
    device: Literal["cuda", "mps", "cpu"] = "cpu"

    # Groq API (FREE 70B AI!)
    groq_api_key: str = Field(default="")

    # Fine-tuning
    use_lora: bool = True
    lora_r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.1

    # Memory Settings
    max_conversation_history: int = 50
    memory_window_size: int = 4096
    enable_long_term_memory: bool = True

    # RAG Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_results: int = 5

    # Agent Settings
    max_agent_iterations: int = 10
    agent_temperature: float = 0.7
    agent_max_tokens: int = 2048

    # External APIs
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    google_api_key: str | None = None

    # Monitoring
    enable_telemetry: bool = True
    metrics_port: int = 9090


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
