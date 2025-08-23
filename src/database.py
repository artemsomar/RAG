from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from src.config import settings



db_engine = create_async_engine(
    url=settings.db.url,
    echo=settings.db.echo,
)


session_factory = async_sessionmaker(
    bind=db_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def session_dependency() -> AsyncSession:
    async with session_factory() as session:
        yield session
        await session.close()