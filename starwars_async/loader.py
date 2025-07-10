import aiohttp
import asyncio
from starwars_async.models import Character, Starship, Vehicle, Planet
from starwars_async.database import AsyncSessionLocal
from starwars_async.api_client import (
    fetch_character_data,
    fetch_starship_data,
    fetch_vehicle_data,
    fetch_planet_data,
    BASE_URL,
)


async def load_character_to_db(session, character_id):
    try:
        # Загружаем данные персонажа
        character_data = await fetch_character_data(session, character_id)
        if not character_data:
            return False

        async with AsyncSessionLocal() as db_session:
            new_character = Character(**character_data)
            db_session.add(new_character)
            await db_session.commit()
            return True
    except Exception:
        return False


async def load_starship_to_db(session, starship_id):
    try:
        # Загружаем данные звездолёта
        starship_data = await fetch_starship_data(session, starship_id)
        if not starship_data:
            return False

        async with AsyncSessionLocal() as db_session:
            new_starship = Starship(**starship_data)
            db_session.add(new_starship)
            await db_session.commit()
            return True
    except Exception:
        return False


async def load_vehicle_to_db(session, vehicle_id):
    try:
        # Загружаем данные транспортного средства
        vehicle_data = await fetch_vehicle_data(session, vehicle_id)
        if not vehicle_data:
            return False

        async with AsyncSessionLocal() as db_session:
            new_vehicle = Vehicle(**vehicle_data)
            db_session.add(new_vehicle)
            await db_session.commit()
            return True
    except Exception:
        return False


async def load_planet_to_db(session, planet_id):
    try:
        # Загружаем данные планеты
        planet_data = await fetch_planet_data(session, planet_id)
        if not planet_data:
            return False

        async with AsyncSessionLocal() as db_session:
            new_planet = Planet(**planet_data)
            db_session.add(new_planet)
            await db_session.commit()
            return True
    except Exception:
        return False


async def load_all_characters():
    timeout = aiohttp.ClientTimeout(total=60 * 5)  # 5 минут общий таймаут
    async with aiohttp.ClientSession(timeout=timeout) as session:
        people_url = f"{BASE_URL.strip()}people/"

        while people_url:
            try:
                async with session.get(people_url.strip()) as response:
                    if response.status != 200:
                        break

                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" not in content_type:
                        break

                    data = await response.json()
                    people_url = data.get("next")  # Переход к следующей странице

                    tasks = []
                    for person in data.get("results", []):
                        try:
                            person_url = person.get('url', '').strip()
                            if not person_url:
                                continue

                            person_id = int(person_url.strip("/").split("/")[-1])
                            tasks.append(load_character_to_db(session, person_id))
                        except (ValueError, IndexError):
                            pass

                    # Ограничиваем количество одновременных задач
                    batch_size = 10
                    for i in range(0, len(tasks), batch_size):
                        batch = tasks[i:i + batch_size]
                        await asyncio.gather(*batch)
                        await asyncio.sleep(1)  # Небольшая пауза между батчами

            except Exception:
                break


async def load_all_starships():
    timeout = aiohttp.ClientTimeout(total=60 * 5)  # 5 минут общий таймаут
    async with aiohttp.ClientSession(timeout=timeout) as session:
        starships_url = f"{BASE_URL.strip()}starships/"

        while starships_url:
            try:
                async with session.get(starships_url.strip()) as response:
                    if response.status != 200:
                        break

                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" not in content_type:
                        break

                    data = await response.json()
                    starships_url = data.get("next")  # Переход к следующей странице

                    tasks = []
                    for starship in data.get("results", []):
                        try:
                            starship_url = starship.get('url', '').strip()
                            if not starship_url:
                                continue

                            starship_id = int(starship_url.strip("/").split("/")[-1])
                            tasks.append(load_starship_to_db(session, starship_id))
                        except (ValueError, IndexError):
                            pass

                    # Ограничиваем количество одновременных задач
                    batch_size = 10
                    for i in range(0, len(tasks), batch_size):
                        batch = tasks[i:i + batch_size]
                        await asyncio.gather(*batch)
                        await asyncio.sleep(1)  # Небольшая пауза между батчами

            except Exception:
                break


async def load_all_vehicles():
    timeout = aiohttp.ClientTimeout(total=60 * 5)  # 5 минут общий таймаут
    async with aiohttp.ClientSession(timeout=timeout) as session:
        vehicles_url = f"{BASE_URL.strip()}vehicles/"

        while vehicles_url:
            try:
                async with session.get(vehicles_url.strip()) as response:
                    if response.status != 200:
                        break

                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" not in content_type:
                        break

                    data = await response.json()
                    vehicles_url = data.get("next")  # Переход к следующей странице

                    tasks = []
                    for vehicle in data.get("results", []):
                        try:
                            vehicle_url = vehicle.get('url', '').strip()
                            if not vehicle_url:
                                continue

                            vehicle_id = int(vehicle_url.strip("/").split("/")[-1])
                            tasks.append(load_vehicle_to_db(session, vehicle_id))
                        except (ValueError, IndexError):
                            pass

                    # Ограничиваем количество одновременных задач
                    batch_size = 10
                    for i in range(0, len(tasks), batch_size):
                        batch = tasks[i:i + batch_size]
                        await asyncio.gather(*batch)
                        await asyncio.sleep(1)  # Небольшая пауза между батчами

            except Exception:
                break


async def load_all_planets():
    timeout = aiohttp.ClientTimeout(total=60 * 5)  # 5 минут общий таймаут
    async with aiohttp.ClientSession(timeout=timeout) as session:
        planets_url = f"{BASE_URL.strip()}planets/"

        while planets_url:
            try:
                async with session.get(planets_url.strip()) as response:
                    if response.status != 200:
                        break

                    content_type = response.headers.get("Content-Type", "")
                    if "application/json" not in content_type:
                        break

                    data = await response.json()
                    planets_url = data.get("next")  # Переход к следующей странице

                    tasks = []
                    for planet in data.get("results", []):
                        try:
                            planet_url = planet.get('url', '').strip()
                            if not planet_url:
                                continue

                            planet_id = int(planet_url.strip("/").split("/")[-1])
                            tasks.append(load_planet_to_db(session, planet_id))
                        except (ValueError, IndexError):
                            pass

                    # Ограничиваем количество одновременных задач
                    batch_size = 10
                    for i in range(0, len(tasks), batch_size):
                        batch = tasks[i:i + batch_size]
                        await asyncio.gather(*batch)
                        await asyncio.sleep(1)  # Небольшая пауза между батчами

            except Exception:
                break