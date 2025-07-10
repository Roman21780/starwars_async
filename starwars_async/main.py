import asyncio
import logging
from starwars_async.loader import (
    load_all_characters,
    load_all_starships,
    load_all_vehicles,
    load_all_planets,
)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Имя файла для сохранения логов
    filemode="a",        # Режим записи: "a" (append) или "w" (overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

async def main():
    try:
        logging.info("Starting to load all characters...")
        await load_all_characters()
        logging.info("All characters have been successfully loaded.")

        logging.info("Starting to load all starships...")
        await load_all_starships()
        logging.info("All starships have been successfully loaded.")

        logging.info("Starting to load all vehicles...")
        await load_all_vehicles()
        logging.info("All vehicles have been successfully loaded.")

        logging.info("Starting to load all planets...")
        await load_all_planets()
        logging.info("All planets have been successfully loaded.")
    except asyncio.CancelledError:
        logging.info("Script was cancelled by user")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        logging.info("Script finished")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Script interrupted by user")