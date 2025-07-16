import aiohttp
import asyncio
from typing import Optional, Dict, Any, List

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

                # Проверяем структуру ответа
                if not data or "result" not in data or "properties" not in data["result"]:
                    return None

                return data["result"]["properties"]

        except (aiohttp.ClientError, asyncio.TimeoutError):
            if attempt == max_retries - 1:
                return None
            await asyncio.sleep(1 * (attempt + 1))
    return None


def safe_join(items: List[Any], separator: str = ", ") -> str:
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
    """Загрузка данных о персонаже (обновленная версия)"""
    url = f"{BASE_URL}people/{character_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    # Получаем название родной планеты
    homeworld_name = None
    if data.get("homeworld"):
        planet_data = await fetch_with_retry(session, data["homeworld"])
        homeworld_name = planet_data.get("name") if planet_data else None

    # Получаем названия фильмов
    film_tasks = [fetch_with_retry(session, film_url) for film_url in data.get("films", [])]
    film_results = await asyncio.gather(*film_tasks, return_exceptions=True)
    films_names = [
        film.get("title") for film in film_results
        if not isinstance(film, Exception) and film
    ]

    # Получаем названия видов
    species_tasks = [fetch_with_retry(session, species_url) for species_url in data.get("species", [])]
    species_results = await asyncio.gather(*species_tasks, return_exceptions=True)
    species_names = [
        species.get("name") for species in species_results
        if not isinstance(species, Exception) and species
    ]

    # Получаем названия кораблей
    starship_tasks = [fetch_with_retry(session, starship_url) for starship_url in data.get("starships", [])]
    starship_results = await asyncio.gather(*starship_tasks, return_exceptions=True)
    starships_names = [
        starship.get("name") for starship in starship_results
        if not isinstance(starship, Exception) and starship
    ]

    # Получаем названия транспорта
    vehicle_tasks = [fetch_with_retry(session, vehicle_url) for vehicle_url in data.get("vehicles", [])]
    vehicle_results = await asyncio.gather(*vehicle_tasks, return_exceptions=True)
    vehicles_names = [
        vehicle.get("name") for vehicle in vehicle_results
        if not isinstance(vehicle, Exception) and vehicle
    ]

    return {
        "id": character_id,
        "birth_year": data.get("birth_year"),
        "eye_color": data.get("eye_color"),
        "films": safe_join(films_names),
        "gender": data.get("gender"),
        "hair_color": data.get("hair_color"),
        "height": data.get("height"),
        "homeworld": homeworld_name,
        "mass": data.get("mass"),
        "name": data.get("name"),
        "skin_color": data.get("skin_color"),
        "species": safe_join(species_names),
        "starships": safe_join(starships_names),
        "vehicles": safe_join(vehicles_names),
    }


async def fetch_starship_data(session: aiohttp.ClientSession, starship_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о звездолёте (обновленная версия)"""
    url = f"{BASE_URL}starships/{starship_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    # Получаем названия фильмов
    film_tasks = [fetch_with_retry(session, film_url) for film_url in data.get("films", [])]
    film_results = await asyncio.gather(*film_tasks, return_exceptions=True)
    films_names = [
        film.get("title") for film in film_results
        if not isinstance(film, Exception) and film
    ]

    # Получаем названия пилотов
    pilot_tasks = [fetch_with_retry(session, pilot_url) for pilot_url in data.get("pilots", [])]
    pilot_results = await asyncio.gather(*pilot_tasks, return_exceptions=True)
    pilots_names = [
        pilot.get("name") for pilot in pilot_results
        if not isinstance(pilot, Exception) and pilot
    ]

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
        "films": safe_join(films_names),
        "pilots": safe_join(pilots_names),
    }


async def fetch_vehicle_data(session: aiohttp.ClientSession, vehicle_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о транспорте (обновленная версия)"""
    url = f"{BASE_URL}vehicles/{vehicle_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    # Получаем названия фильмов
    film_tasks = [fetch_with_retry(session, film_url) for film_url in data.get("films", [])]
    film_results = await asyncio.gather(*film_tasks, return_exceptions=True)
    films_names = [
        film.get("title") for film in film_results
        if not isinstance(film, Exception) and film
    ]

    # Получаем названия пилотов
    pilot_tasks = [fetch_with_retry(session, pilot_url) for pilot_url in data.get("pilots", [])]
    pilot_results = await asyncio.gather(*pilot_tasks, return_exceptions=True)
    pilots_names = [
        pilot.get("name") for pilot in pilot_results
        if not isinstance(pilot, Exception) and pilot
    ]

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
        "films": safe_join(films_names),
        "pilots": safe_join(pilots_names),
    }


async def fetch_planet_data(session: aiohttp.ClientSession, planet_id: int) -> Optional[Dict[str, Any]]:
    """Загрузка данных о планете (обновленная версия)"""
    url = f"{BASE_URL}planets/{planet_id}"
    data = await fetch_with_retry(session, url)
    if not data:
        return None

    # Получаем названия жителей
    resident_tasks = [fetch_with_retry(session, resident_url) for resident_url in data.get("residents", [])]
    resident_results = await asyncio.gather(*resident_tasks, return_exceptions=True)
    residents_names = [
        resident.get("name") for resident in resident_results
        if not isinstance(resident, Exception) and resident
    ]

    # Получаем названия фильмов
    film_tasks = [fetch_with_retry(session, film_url) for film_url in data.get("films", [])]
    film_results = await asyncio.gather(*film_tasks, return_exceptions=True)
    films_names = [
        film.get("title") for film in film_results
        if not isinstance(film, Exception) and film
    ]

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
        "residents": safe_join(residents_names),
        "films": safe_join(films_names),
    }