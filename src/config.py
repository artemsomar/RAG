from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DbSettings(BaseModel):
    user: str
    password: str
    host: str = "localhost"
    port: int = 5432
    database: str = "rag"
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class EmbeddingSettings(BaseModel):
    token: str
    model: str = "embed-v4.0"
    chunk_size_in_words: int = 50
    overlap_in_words: int = 20
    batch_size: int = 96


class Settings(BaseSettings):
    db: DbSettings
    embedding: EmbeddingSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"

settings = Settings()