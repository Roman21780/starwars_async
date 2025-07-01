import aiohttp

from starwars_async.models import Character
from starwars_async.database import AsyncSessionLocal
from starwars_async.api_client import fetch_character_data
import asyncio


async def load_character_to_db(character_id):
    character_data = await fetch_character_data(character_id)

    async with AsyncSessionLocal() as session:
        new_character = Character(**character_data)
        session.add(new_character)
        await session.commit()


async def load_all_characters():
    async with aiohttp.ClientSession() as session:
        people_url = "https://swapi.dev/api/people/ "
        while people_url:
            response = await session.get(people_url)
            data = await response.json()
            people_url = data.get("next")

            tasks = [load_character_to_db(int(person["url"].split("/")[-2]))
                     for person in data["results"]]
            await asyncio.gather(*tasks)
