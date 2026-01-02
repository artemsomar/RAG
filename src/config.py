from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class S3Settings(BaseModel):
    project_name: str = "RAG"
    bucket_name: str = "rag-documents"
    endpoint_url: str
    access_key: str
    access_secret_key: str
    region: str


class DbSettings(BaseModel):
    user: str
    password: str
    host: str = "pg"
    port: int = 5432
    database: str = "rag"
    echo: bool = False

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class LlmSettings(BaseModel):
    token: str
    model: str = "command-a-03-2025"


class ChunkingSettings(BaseModel):
    size_in_characters: int = 1000
    overlap_in_characters: int = 200


class TokenizingSettings(BaseModel):
    token: str
    model: str = "command-a-03-2025"


class EmbeddingSettings(BaseModel):
    token: str
    model: str = "embed-v4.0"
    batch_size: int = 96


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_minutes: int = 15
    refresh_token_expires_minutes: int = 30 * 24 * 60


class Settings(BaseSettings):
    s3: S3Settings
    db: DbSettings
    embedding: EmbeddingSettings
    tokenizing: TokenizingSettings
    llm: LlmSettings
    chunking: ChunkingSettings = ChunkingSettings()
    auth: AuthJWT = AuthJWT()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"


settings = Settings()
