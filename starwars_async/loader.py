import aiohttp
import asyncio
import logging
from typing import Optional, List, Any
from sqlalchemy.exc import SQLAlchemyError
from starwars_async.models import Character, Starship, Vehicle, Planet
from starwars_async.database import AsyncSessionLocal, init_db
from starwars_async.api_client import (
    fetch_character_data,
    fetch_starship_data,
    fetch_vehicle_data,
    fetch_planet_data,
    BASE_URL,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        self.session = None
        self.semaphore = asyncio.Semaphore(5)

    def clean_string(self, value: Any) -> Optional[str]:
        """Очистка и нормализация строковых значений"""
        if value is None or value in ("unknown", "n/a", ""):
            return None
        if isinstance(value, list):
            return ", ".join(str(v).strip() for v in value if v and str(v).strip() not in ("unknown", "n/a"))
        return str(value).strip()

    async def load_entity(self, entity_id: int, model, fetch_func, entity_type: str) -> bool:
        """Загрузка одной сущности"""
        async with self.semaphore:
            try:
                entity_data = await fetch_func(self.session, entity_id)
                if not entity_data:
                    logger.warning(f"No data for {entity_type} {entity_id}")
                    return False

                # Очищаем данные
                cleaned_data = {k: self.clean_string(v) for k, v in entity_data.items()}
                cleaned_data['id'] = entity_id

                # Сохраняем в БД
                async with AsyncSessionLocal() as db_session:
                    existing = await db_session.get(model, entity_id)
                    if existing:
                        for key, value in cleaned_data.items():
                            setattr(existing, key, value)
                    else:
                        db_session.add(model(**cleaned_data))

                    await db_session.commit()
                    logger.info(f"Saved {entity_type} {entity_id}")
                    return True

            except Exception as e:
                logger.error(f"Error processing {entity_type} {entity_id}: {str(e)}", exc_info=True)
                return False

    async def process_entity_type(self, endpoint: str, model, fetch_func, entity_type: str):
        """Обработка всех сущностей одного типа"""
        logger.info(f"Starting {entity_type}s loading...")
        url = f"{BASE_URL}{endpoint}/"

        while url:
            try:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    url = data.get("next")

                    tasks = []
                    for entity in data.get("results", []):
                        entity_url = entity.get('url', '')
                        if not entity_url:
                            continue

                        try:
                            entity_id = int(entity_url.strip("/").split("/")[-1])
                            tasks.append(self.load_entity(entity_id, model, fetch_func, entity_type))
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Invalid {entity_type} URL {entity_url}: {str(e)}")

                    # Ограничиваем скорость запросов
                    for i in range(0, len(tasks), 5):
                        batch = tasks[i:i + 5]
                        await asyncio.gather(*batch)
                        await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(f"Error loading {entity_type}s: {str(e)}", exc_info=True)
                break

        logger.info(f"Finished loading {entity_type}s")

    async def run(self):
        """Основной метод запуска загрузки"""
        await init_db()

        timeout = aiohttp.ClientTimeout(total=300)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            self.session = session

            # Загружаем данные последовательно для стабильности
            await self.process_entity_type("planets", Planet, fetch_planet_data, "planet")
            await self.process_entity_type("people", Character, fetch_character_data, "character")
            await self.process_entity_type("starships", Starship, fetch_starship_data, "starship")
            await self.process_entity_type("vehicles", Vehicle, fetch_vehicle_data, "vehicle")


if __name__ == "__main__":
    loader = DataLoader()
    asyncio.run(loader.run())