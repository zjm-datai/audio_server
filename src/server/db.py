import re

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

_engine = None

def get_engine():
    return _engine

async def get_session():
    async with AsyncSession(_engine) as session:
        yield session

def init_db(db_url: str):
    global _engine
    if _engine is None:
        connect_args = {}
        if db_url.startswith("sqlite://"):
            connect_args = {"check_same_thread": False}
            db_url = re.sub(r'^sqlite://', 'sqlite+aiosqlite://', db_url)
        elif db_url.startswith("postgresql://"):
            db_url = re.sub(r'^postgresql://', 'postgresql+asyncpg://', db_url)
        elif db_url.startswith("mysql://"):
            db_url = re.sub(r'^mysql://', 'mysql+asyncmy://', db_url)
        else:
            raise Exception(f"Unsupported database URL: {db_url}")

        _engine = create_async_engine(
            db_url,
            echo=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            connect_args=connect_args,
        )
