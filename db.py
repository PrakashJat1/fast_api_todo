from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_URL = os.getenv("DB_URL") or "postgresql+asyncpg://postgres:Prakash%40123@localhost:5432/fastapi_todo"

engine = create_async_engine(url=DB_URL,pool_size=5,max_overflow=10)

AsyncSessionLocal = async_sessionmaker(bind=engine,autoflush=False,expire_on_commit=False,autocommit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        except Exception:
            await db.rollback()
            raise
