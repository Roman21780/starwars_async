import aiohttp
import asyncio

BASE_URL = "https://swapi.dev/api/ "


async def fetch_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            raise Exception(f"Error fetching {url}: {response.status}")


async def fetch_resource_name(session, url):
    if not url:
        return None
    data = await fetch_data(session, url)
    return data.get("name", data.get("title"))


async def fetch_character_data(character_id):
    async with aiohttp.ClientSession() as session:
        character_url = f"{BASE_URL}people/{character_id}"
        character_data = await fetch_data(session, character_url)

        # Параллельно получаем названия фильмов, планет, кораблей и т.д.
        films = await asyncio.gather(
            *[fetch_resource_name(session, film_url.strip())
              for film_url in character_data["films"]]
        )
        species = await asyncio.gather(
            *[fetch_resource_name(session, specie_url.strip())
              for specie_url in character_data["species"]]
        )
        starships = await asyncio.gather(
            *[fetch_resource_name(session, starship_url.strip())
              for starship_url in character_data["starships"]]
        )
        vehicles = await asyncio.gather(
            *[fetch_resource_name(session, vehicle_url.strip())
              for vehicle_url in character_data["vehicles"]]
        )
        homeworld = await fetch_resource_name(
            session, character_data["homeworld"].strip())

        return {
            "id": character_id,
            "birth_year": character_data["birth_year"],
            "eye_color": character_data["eye_color"],
            "films": ", ".join(films),
            "gender": character_data["gender"],
            "hair_color": character_data["hair_color"],
            "height": character_data["height"],
            "homeworld": homeworld,
            "mass": character_data["mass"],
            "name": character_data["name"],
            "skin_color": character_data["skin_color"],
            "species": ", ".join(species),
            "starships": ", ".join(starships),
            "vehicles": ", ".join(vehicles),
        }
