import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # 加载环境变量


class Settings(BaseSettings):
    app_name: str = "Local RAG"
    debug: bool = True

    # DeepSeek API
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY", "")
    deepseek_api_base: str = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    deepseek_model: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    # Embedding
    embedding_model_name: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
    embedding_device: str = os.getenv("EMBEDDING_DEVICE", "cpu")

    # Paths
    _base_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    sources_path: str = os.path.join(_base_dir, "data", "sources")
    upload_path: str = os.path.join(_base_dir, "data", "uploads")

    vector_store_path: str = os.path.join(_base_dir, "data", "vector_store")

    # Chunk settings
    chunk_size: int = 512
    chunk_overlap: int = 128

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(_base_dir, 'data', 'app.db')}",
    )

    # JWT
    jwt_secret: str = os.getenv("JWT_SECRET", "local-rag-dev-secret-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 72


settings = Settings()
