from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# Example connection string using asyncpg
# (You can manage this via environment variables later)
DATABASE_URL = "postgresql+asyncpg://postgres:admin1234@localhost:5432/framework_db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session factory for handling async database sessions
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI to yield an async database session."""
    async with async_session_maker() as session:
        yield session