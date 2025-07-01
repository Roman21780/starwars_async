import aiohttp
import asyncio
import logging
from starwars_async.models import Character
from starwars_async.database import AsyncSessionLocal
from starwars_async.api_client import fetch_character_data, BASE_URL

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Логи будут записываться в файл app.log
    filemode="w",  # Режим записи: "a" (append) — добавление в конец файла
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def load_character_to_db(character_id):
    try:
        # Получаем данные персонажа
        character_data = await fetch_character_data(character_id)
        logging.info(f"Fetched data for character ID {character_id}: {character_data}")

        # Сохраняем данные в базу данных
        async with AsyncSessionLocal() as session:
            new_character = Character(**character_data)
            session.add(new_character)
            await session.commit()
            logging.info(f"Character ID {character_id} successfully saved to the database.")
    except Exception as e:
        logging.error(f"Error saving character ID {character_id} to the database: {e}")


async def load_all_characters():
    async with aiohttp.ClientSession() as session:
        page = 1
        while True:
            people_url = f"{BASE_URL}people?page={page}&limit=10"
            logging.info(f"Fetching page: {people_url}")

            try:
                response = await session.get(people_url)
                if response.status != 200:
                    break

                data = await response.json()
                if not data.get('results'):
                    break

                tasks = []
                for person in data['results']:
                    try:
                        # Извлекаем ID из URL формата "https://www.swapi.tech/api/people/1"
                        person_url = person['url']
                        person_id = int(person_url.split('/')[-1])
                        tasks.append(load_character_to_db(person_id))
                    except (ValueError, IndexError, KeyError) as e:
                        logging.error(f"Invalid person URL: {person_url}. Error: {e}")

                await asyncio.gather(*tasks)

                page += 1
                if page > 10:  # Предотвращаем бесконечный цикл
                    break

            except Exception as e:
                logging.error(f"Error fetching page {page}: {str(e)}")
                break


