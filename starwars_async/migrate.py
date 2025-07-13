from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
import os
import asyncio
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Получаем URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в .env файле")

# Создаем асинхронный движок SQLAlchemy с настройками пула соединений
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)


async def test_connection():
    """Проверка подключения к базе данных"""
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info("Подключение к базе данных успешно")
            return True
    except Exception as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        return False


async def create_tables(drop_existing: bool = False):
    """Создание всех таблиц в базе данных"""
    try:
        async with async_engine.begin() as conn:
            if drop_existing:
                logger.info("Удаление существующих таблиц...")
                await conn.run_sync(Base.metadata.drop_all)

            logger.info("Создание таблиц...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Все таблицы успешно созданы")
            return True
    except Exception as e:
        logger.error(f"Ошибка при создании таблиц: {e}")
        return False


async def main():
    """Основная функция выполнения миграции"""
    if not await test_connection():
        return

    if not await create_tables(drop_existing=True):
        return

    logger.info("Миграция завершена успешно")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Миграция прервана пользователем")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    finally:
        # Явное закрытие соединений при завершении
        asyncio.run(async_engine.dispose())