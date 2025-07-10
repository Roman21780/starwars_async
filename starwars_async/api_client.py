import aiohttp
import asyncio
from typing import Optional, Dict, Any

# Конфигурация
BASE_URL = "https://www.swapi.tech/api/ "
REQUEST_TIMEOUT = 30  # секунд
MAX_RETRIES = 3
CONCURRENT_REQUESTS_LIMIT = 5  # Ограничение на количество одновременных запросов

# Семафор для ограничения количества одновременных запросов
request_semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS_LIMIT)


async def fetch_data(session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
    """
    Общая функция для получения данных из API.
    """
    for attempt in range(MAX_RETRIES):
        try:
            async with request_semaphore, session.get(url.strip(), timeout=REQUEST_TIMEOUT) as response:
                if response.status == 429:  # Rate limiting
                    wait_time = 5 * (attempt + 1)  # Экспоненциальная задержка
                    await asyncio.sleep(wait_time)
                    continue

                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    return {}

                response.raise_for_status()
                data = await response.json()

                # Проверяем структуру ответа
                if "result" not in data or "properties" not in data["result"]:
                    return {}

                return data["result"]["properties"]

        except (aiohttp.ClientError, aiohttp.ClientResponseError, asyncio.TimeoutError):
            if attempt == MAX_RETRIES - 1:
                raise
            await asyncio.sleep(1 * (attempt + 1))

    raise Exception(f"All {MAX_RETRIES} attempts failed for {url}")


def safe_join(items: list) -> str:
    """
    Безопасное объединение списка строк с фильтрацией None и пустых значений.
    """
    if not items:
        return "unknown"

    # Фильтруем None и пустые значения
    filtered = [str(item).strip() for item in items if item is not None and str(item).strip()]
    return ", ".join(filtered) if filtered else "unknown"


async def fetch_character_data(session, character_id: int) -> Optional[Dict[str, Any]]:
    """
    Загрузка данных о персонаже.
    """
    try:
        character_url = f"{BASE_URL.strip()}people/{character_id}"
        async with session.get(character_url) as response:
            if response.status == 200:
                data = await response.json()
                properties = data.get("result", {}).get("properties", {})

                # Фильтруем только нужные поля
                filtered_data = {
                    "id": int(character_id),
                    "birth_year": properties.get("birth_year", "unknown"),
                    "eye_color": properties.get("eye_color", "unknown"),
                    "films": safe_join(properties.get("films", [])),
                    "gender": properties.get("gender", "unknown"),
                    "hair_color": properties.get("hair_color", "unknown"),
                    "height": properties.get("height", "unknown"),
                    "homeworld": properties.get("homeworld", "unknown"),
                    "mass": properties.get("mass", "unknown"),
                    "name": properties.get("name", "unknown"),
                    "skin_color": properties.get("skin_color", "unknown"),
                    "species": safe_join(properties.get("species", [])),
                    "starships": safe_join(properties.get("starships", [])),
                    "vehicles": safe_join(properties.get("vehicles", [])),
                }
                return filtered_data
            else:
                return None
    except Exception:
        return None


async def fetch_starship_data(session, starship_id: int) -> Optional[Dict[str, Any]]:
    """
    Загрузка данных о звездолёте.
    """
    try:
        starship_url = f"{BASE_URL.strip()}starships/{starship_id}"
        async with session.get(starship_url) as response:
            if response.status == 200:
                data = await response.json()
                properties = data.get("result", {}).get("properties", {})

                # Фильтруем только нужные поля
                filtered_data = {
                    "id": starship_id,
                    "name": properties.get("name", "unknown"),
                    "model": properties.get("model", "unknown"),
                    "manufacturer": properties.get("manufacturer", "unknown"),
                    "cost_in_credits": properties.get("cost_in_credits", "unknown"),
                    "length": properties.get("length", "unknown"),
                    "crew": properties.get("crew", "unknown"),
                    "passengers": properties.get("passengers", "unknown"),
                    "cargo_capacity": properties.get("cargo_capacity", "unknown"),
                    "consumables": properties.get("consumables", "unknown"),
                    "hyperdrive_rating": properties.get("hyperdrive_rating", "unknown"),
                    "starship_class": properties.get("starship_class", "unknown"),
                    "films": safe_join(properties.get("films", [])),
                }
                return filtered_data
            else:
                return None
    except Exception:
        return None


async def fetch_vehicle_data(session, vehicle_id: int) -> Optional[Dict[str, Any]]:
    """
    Загрузка данных о транспортном средстве.
    """
    try:
        vehicle_url = f"{BASE_URL.strip()}vehicles/{vehicle_id}"
        async with session.get(vehicle_url) as response:
            if response.status == 200:
                data = await response.json()
                properties = data.get("result", {}).get("properties", {})

                # Фильтруем только нужные поля
                filtered_data = {
                    "id": vehicle_id,
                    "name": properties.get("name", "unknown"),
                    "model": properties.get("model", "unknown"),
                    "manufacturer": properties.get("manufacturer", "unknown"),
                    "cost_in_credits": properties.get("cost_in_credits", "unknown"),
                    "length": properties.get("length", "unknown"),
                    "crew": properties.get("crew", "unknown"),
                    "passengers": properties.get("passengers", "unknown"),
                    "cargo_capacity": properties.get("cargo_capacity", "unknown"),
                    "consumables": properties.get("consumables", "unknown"),
                    "vehicle_class": properties.get("vehicle_class", "unknown"),
                    "films": safe_join(properties.get("films", [])),
                }
                return filtered_data
            else:
                return None
    except Exception:
        return None


async def fetch_planet_data(session, planet_id: int) -> Optional[Dict[str, Any]]:
    """
    Загрузка данных о планете.
    """
    try:
        planet_url = f"{BASE_URL.strip()}planets/{planet_id}"
        async with session.get(planet_url) as response:
            if response.status == 200:
                data = await response.json()
                properties = data.get("result", {}).get("properties", {})

                # Фильтруем только нужные поля
                filtered_data = {
                    "id": planet_id,
                    "name": properties.get("name", "unknown"),
                    "diameter": properties.get("diameter", "unknown"),
                    "rotation_period": properties.get("rotation_period", "unknown"),
                    "orbital_period": properties.get("orbital_period", "unknown"),
                    "gravity": properties.get("gravity", "unknown"),
                    "population": properties.get("population", "unknown"),
                    "climate": properties.get("climate", "unknown"),
                    "terrain": properties.get("terrain", "unknown"),
                    "surface_water": properties.get("surface_water", "unknown"),
                }
                return filtered_data
            else:
                return None
    except Exception:
        return None