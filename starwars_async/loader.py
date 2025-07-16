import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from starwars_async.models import Character, Starship, Vehicle, Planet, Base
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

# Тип для моделей SQLAlchemy
ModelType = TypeVar('ModelType', bound=Base)


class DataLoader:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(5)  # Ограничение параллельных запросов
        self.request_delay = 0.5  # Задержка между пакетами запросов

    def clean_string(self, value: Any) -> Optional[str]:
        """Улучшенная очистка строковых значений"""
        if value is None:
            return None

        if isinstance(value, list):
            cleaned = [
                str(v).strip() for v in value
                if v and str(v).strip().lower() not in ("unknown", "n/a", "none", "")
            ]
            return ", ".join(cleaned) if cleaned else None

        value = str(value).strip()
        return value if value.lower() not in ("unknown", "n/a", "none", "") else None

    async def load_entity(
            self,
            entity_id: int,
            model: Type[ModelType],
            fetch_func: callable,
            entity_type: str
    ) -> bool:
        """Улучшенная загрузка одной сущности с обработкой транзакций"""
        async with self.semaphore:
            try:
                # Загрузка данных
                entity_data = await fetch_func(self.session, entity_id)
                if not entity_data:
                    logger.warning(f"No data for {entity_type} {entity_id}")
                    return False

                # Очистка данных
                cleaned_data = {
                    k: self.clean_string(v)
                    for k, v in entity_data.items()
                    if k != 'id'  # Исключаем id из очистки
                }
                cleaned_data['id'] = entity_id

                # Сохранение в БД
                async with AsyncSessionLocal() as db_session:
                    try:
                        existing = await db_session.get(model, entity_id)
                        if existing:
                            for key, value in cleaned_data.items():
                                setattr(existing, key, value)
                        else:
                            db_session.add(model(**cleaned_data))

                        await db_session.commit()
                        logger.info(f"Successfully saved {entity_type} {entity_id}")
                        return True

                    except SQLAlchemyError as e:
                        await db_session.rollback()
                        logger.error(f"Database error for {entity_type} {entity_id}: {str(e)}")
                        return False

            except asyncio.TimeoutError:
                logger.warning(f"Timeout loading {entity_type} {entity_id}")
                return False

            except Exception as e:
                logger.error(
                    f"Unexpected error processing {entity_type} {entity_id}: {str(e)}",
                    exc_info=True
                )
                return False

    async def process_entity_type(
            self,
            endpoint: str,
            model: Type[ModelType],
            fetch_func: callable,
            entity_type: str
    ) -> None:
        """Оптимизированная обработка всех сущностей одного типа"""
        logger.info(f"Starting {entity_type}s loading...")
        url = f"{BASE_URL}{endpoint}/"

        try:
            while url:
                async with self.session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    url = data.get("next")

                    tasks = []
                    for entity in data.get("results", []):
                        if not (entity_url := entity.get('url')):
                            continue

                        try:
                            entity_id = int(entity_url.strip("/").split("/")[-1])
                            tasks.append(
                                self.load_entity(entity_id, model, fetch_func, entity_type)
                            )
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Invalid {entity_type} URL {entity_url}: {str(e)}")

                    # Обработка пакетами с задержкой
                    for i in range(0, len(tasks), 5):
                        batch = tasks[i:i + 5]
                        await asyncio.gather(*batch, return_exceptions=True)
                        await asyncio.sleep(self.request_delay)

        except aiohttp.ClientError as e:
            logger.error(f"HTTP error loading {entity_type}s: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error loading {entity_type}s: {str(e)}", exc_info=True)
        finally:
            logger.info(f"Finished loading {entity_type}s")

    async def run(self) -> None:
        """Улучшенный основной метод запуска с обработкой ошибок"""
        try:
            await init_db()

            timeout = aiohttp.ClientTimeout(total=300)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                self.session = session

                # Порядок загрузки важен для ссылочной целостности
                await self.process_entity_type("planets", Planet, fetch_planet_data, "planet")
                await self.process_entity_type("people", Character, fetch_character_data, "character")
                await self.process_entity_type("starships", Starship, fetch_starship_data, "starship")
                await self.process_entity_type("vehicles", Vehicle, fetch_vehicle_data, "vehicle")

        except Exception as e:
            logger.critical(f"Fatal error in DataLoader: {str(e)}", exc_info=True)
            raise


if __name__ == "__main__":
    loader = DataLoader()
    try:
        asyncio.run(loader.run())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.critical(f"Application crashed: {str(e)}", exc_info=True)
