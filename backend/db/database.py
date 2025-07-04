from abc import ABC, abstractmethod
from typing import Optional
from contextlib import asynccontextmanager

from pydantic.v1 import BaseSettings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession

from .base import Base


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "my_tasks"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"


database_settings = DatabaseSettings()


class Database(ABC):
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.session: Optional[async_sessionmaker[AsyncSession]] = None

    async def init(self) -> None:
        try:
            self.engine = create_async_engine(
                self._create_url(),
                echo=False,
                pool_pre_ping=True
            )
            self.session = async_sessionmaker(
                self.engine,
                expire_on_commit=False,
                autoflush=False,
            )
            await self._create_tables()
        except SQLAlchemyError as e:
            raise RuntimeError(f'Database initialization failed: {str(e)}')

    async def close(self) -> None:
        if self.engine:
            await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.session() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    async def _create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @abstractmethod
    def _create_url(self) -> str:
        pass


class PostgresDB(Database):
    def __init__(self):
        super().__init__()

    def _create_url(self) -> str:
        return database_settings.database_url
