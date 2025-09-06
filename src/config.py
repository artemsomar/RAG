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

class Settings(BaseSettings):
    db: DbSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "allow"

settings = Settings()