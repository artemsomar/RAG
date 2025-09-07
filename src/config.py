from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)

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


class Chunking(BaseModel):
    chunk_size_in_characters: int = 500
    overlap_in_characters: int = 100


class Tokenizing(BaseModel):
    token: str
    model: str = "command-a-03-2025"


class Embedding(BaseModel):
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
    db: DbSettings
    embedding: Embedding
    tokenizing: Tokenizing
    chunking: Chunking = Chunking()
    auth: AuthJWT = AuthJWT()

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"

settings = Settings()