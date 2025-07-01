from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# загружаем переменные окружения из файла .env
load_dotenv()

# получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# создаем фабрику сессий
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# функция для получения сессии базы данных
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session
