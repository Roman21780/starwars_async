import aiohttp
import asyncio
from starwars_async.models import Character
from starwars_async.database import AsyncSessionLocal
from starwars_async.api_client import fetch_character_data, BASE_URL


async def load_character_to_db(character_id):
    try:
        # Получаем данные персонажа
        character_data = await fetch_character_data(character_id)

        # Сохраняем данные в базу данных
        async with AsyncSessionLocal() as session:
            new_character = Character(**character_data)
            session.add(new_character)
            await session.commit()
            return True  # Успешное сохранение
    except Exception as e:
        return f"Error saving character ID {character_id} to the database: {e}"


async def load_all_characters():
    async with aiohttp.ClientSession() as session:
        people_url = f"{BASE_URL}people/"
        while people_url:
            try:
                response = await session.get(people_url)
                if response.status != 200:
                    return f"Error fetching page: HTTP status {response.status}"

                data = await response.json()
                people_url = data.get("next")  # Если нет следующей страницы, будет None

                tasks = []
                for person in data["results"]:
                    try:
                        # Извлекаем ID из URL формата "https://www.swapi.tech/api/people/1/ "
                        person_url = person['url']
                        person_id = int(person_url.strip("/").split("/")[-1])
                        tasks.append(load_character_to_db(person_id))
                    except (ValueError, IndexError, KeyError) as e:
                        return f"Invalid person URL: {person_url}. Error: {e}"

                await asyncio.gather(*tasks)

            except Exception as e:
                return f"Error fetching page: {str(e)}"