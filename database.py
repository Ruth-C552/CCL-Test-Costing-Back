# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Settings class to read DB config
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    class Config:
        env_file = ".env"

settings = Settings()

# Construct the database URL dynamically
DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
