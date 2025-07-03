from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from starwars_async.models import Base
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Функция для создания таблиц
async def migrate():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(migrate())