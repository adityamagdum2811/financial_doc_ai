from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Financial Document Management API"
    secret_key: str = "my_super_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = "sqlite:///./financial_docs.db"
    upload_dir: str = "app/uploads"
    chroma_path: str = "./chroma_db"

    class Config:
        env_file = ".env"


settings = Settings()