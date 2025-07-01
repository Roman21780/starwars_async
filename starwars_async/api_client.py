import aiohttp
import asyncio
import logging

BASE_URL = "https://www.swapi.tech/api/"


async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if "result" not in data or "properties" not in data["result"]:
                    raise ValueError(f"Invalid API response structure from {url}")
                return data["result"]["properties"]
            else:
                raise Exception(f"Error fetching {url}: HTTP {response.status}")
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}: {str(e)}")
        raise


async def fetch_resource_name(session, url):
    if not url:
        return None
    try:
        data = await fetch_data(session, url)
        return data.get("name", data.get("title", "unknown"))
    except Exception as e:
        logging.warning(f"Could not fetch resource name from {url}: {str(e)}")
        return "unknown"


def safe_join(items):
    if not items:
        return "unknown"
    return ", ".join(str(item) for item in items if item) or "unknown"


async def fetch_character_data(character_id):
    async with aiohttp.ClientSession() as session:
        try:
            character_url = f"{BASE_URL}people/{character_id}"
            character_data = await fetch_data(session, character_url)

            # Получаем все связанные данные параллельно
            films, species, starships, vehicles, homeworld = await asyncio.gather(
                asyncio.gather(*[
                    fetch_resource_name(session, film_url.strip())
                    for film_url in character_data.get("films", [])
                ]),
                asyncio.gather(*[
                    fetch_resource_name(session, specie_url.strip())
                    for specie_url in character_data.get("species", [])
                ]),
                asyncio.gather(*[
                    fetch_resource_name(session, starship_url.strip())
                    for starship_url in character_data.get("starships", [])
                ]),
                asyncio.gather(*[
                    fetch_resource_name(session, vehicle_url.strip())
                    for vehicle_url in character_data.get("vehicles", [])
                ]),
                fetch_resource_name(session, character_data.get("homeworld", "").strip())
            )

            return {
                "id": character_id,
                "birth_year": str(character_data.get("birth_year", "unknown")),
                "eye_color": str(character_data.get("eye_color", "unknown")),
                "films": safe_join(films),
                "gender": str(character_data.get("gender", "unknown")),
                "hair_color": str(character_data.get("hair_color", "unknown")),
                "height": str(character_data.get("height", "unknown")),
                "homeworld": str(homeworld or "unknown"),
                "mass": str(character_data.get("mass", "unknown")),
                "name": str(character_data.get("name", "unknown")),
                "skin_color": str(character_data.get("skin_color", "unknown")),
                "species": safe_join(species),
                "starships": safe_join(starships),
                "vehicles": safe_join(vehicles),
            }
        except Exception as e:
            logging.error(f"Failed to fetch character {character_id}: {str(e)}")
            raise