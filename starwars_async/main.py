# Точка входа
import logging
import asyncio
import traceback
from starwars_async.loader import load_all_characters

# Настройка логирования с сохранением в файл
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Имя файла для сохранения логов
    filemode="a",        # Режим записи: "a" (append) или "w" (overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    try:
        logging.info("Starting to load all characters...")
        # Загружаем всех персонажей
        await load_all_characters()
        logging.info("All characters have been successfully loaded.")
    except Exception as e:
        error_traceback = traceback.format_exc()
        logging.error("An error occurred: %s\n%s", e, error_traceback)


if __name__ == "__main__":
    asyncio.run(main())