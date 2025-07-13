from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Базовый класс для моделей
Base = declarative_base()

# Получаем URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session():
    """Генератор сессий базы данных"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Инициализация базы данных - создание таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)