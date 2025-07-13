import aiohttp
import asyncio
from typing import Optional, Dict, Any

# Конфигурация
BASE_URL = "https://www.swapi.tech/api/"
REQUEST_TIMEOUT = 30  # секунд
MAX_RETRIES = 3
CONCURRENT_REQUESTS_LIMIT = 5

async def fetch_with_retry(
    session: aiohttp.ClientSession,
    url: str,
    max_retries: int = MAX_RETRIES
) -> Optional[Dict[str, Any]]:
    """Выполнение запроса с повторами при ошибках"""
    for attempt in range(max_retries):
        try:
            async with session.get(url.strip(), timeout=REQUEST_TIMEOUT) as response:
                if response.status == 429:  # Rate limiting
                    wait_time = 2 ** (attempt + 1)  # Экспоненциальная задержка
                    await asyncio.sleep(wait_time)
                    continue

                if response.status != 200:
                    if attempt == max_retries - 1:
                        return None
                    continue

                data = await response.json()
                if not data or "result" not in data:
                    return None

                return data["result"]["properties"]

        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == max_retries - 1:
                return None
            await asyncio.sleep(1 * (attempt + 1))

    return None

def safe_join(items: list, separator: str = ", ") -> str:
    """Безопасное объединение списка в строку"""
    if not items:
        return "unknown"
    return separator.join(str(item).strip() for item in items if item and str(item).strip())

def extract_id(url: str) -> Optional[int]:
    """Извлечение ID из URL"""
    try:
        return int(url.strip("/").split("/")[-1])
    except (ValueError, IndexError, AttributeError):
        return None

async def fetch_character_data(session: aiohttp.ClientSession, character_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о персонаже"""
    url = f"{BASE_URL}people/{character_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    return {
        "id": character_id,
        "birth_year": data.get("birth_year", "unknown"),
        "eye_color": data.get("eye_color", "unknown"),
        "films": safe_join(data.get("films", [])),
        "gender": data.get("gender", "unknown"),
        "hair_color": data.get("hair_color", "unknown"),
        "height": data.get("height", "unknown"),
        "homeworld": data.get("homeworld", "unknown"),
        "mass": data.get("mass", "unknown"),
        "name": data.get("name", "unknown"),
        "skin_color": data.get("skin_color", "unknown"),
        "species": safe_join(data.get("species", [])),
        "starships": safe_join(data.get("starships", [])),
        "vehicles": safe_join(data.get("vehicles", [])),
    }

async def fetch_starship_data(session: aiohttp.ClientSession, starship_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о звездолёте"""
    url = f"{BASE_URL}starships/{starship_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    return {
        "id": starship_id,
        "name": data.get("name", "unknown"),
        "model": data.get("model", "unknown"),
        "manufacturer": data.get("manufacturer", "unknown"),
        "cost_in_credits": data.get("cost_in_credits", "unknown"),
        "length": data.get("length", "unknown"),
        "crew": data.get("crew", "unknown"),
        "passengers": data.get("passengers", "unknown"),
        "cargo_capacity": data.get("cargo_capacity", "unknown"),
        "consumables": data.get("consumables", "unknown"),
        "hyperdrive_rating": data.get("hyperdrive_rating", "unknown"),
        "starship_class": data.get("starship_class", "unknown"),
        "films": safe_join(data.get("films", [])),
    }

async def fetch_vehicle_data(session: aiohttp.ClientSession, vehicle_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о транспортном средстве"""
    url = f"{BASE_URL}vehicles/{vehicle_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    return {
        "id": vehicle_id,
        "name": data.get("name", "unknown"),
        "model": data.get("model", "unknown"),
        "manufacturer": data.get("manufacturer", "unknown"),
        "cost_in_credits": data.get("cost_in_credits", "unknown"),
        "length": data.get("length", "unknown"),
        "crew": data.get("crew", "unknown"),
        "passengers": data.get("passengers", "unknown"),
        "cargo_capacity": data.get("cargo_capacity", "unknown"),
        "consumables": data.get("consumables", "unknown"),
        "vehicle_class": data.get("vehicle_class", "unknown"),
        "films": safe_join(data.get("films", [])),
    }

async def fetch_planet_data(session: aiohttp.ClientSession, planet_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о планете"""
    url = f"{BASE_URL}planets/{planet_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    return {
        "id": planet_id,
        "name": data.get("name", "unknown"),
        "diameter": data.get("diameter", "unknown"),
        "rotation_period": data.get("rotation_period", "unknown"),
        "orbital_period": data.get("orbital_period", "unknown"),
        "gravity": data.get("gravity", "unknown"),
        "population": data.get("population", "unknown"),
        "climate": data.get("climate", "unknown"),
        "terrain": data.get("terrain", "unknown"),
        "surface_water": data.get("surface_water", "unknown"),
    }