# Точка входа
import logging
import asyncio
from starwars_async.loader import load_all_characters

# Настройка логирования с сохранением в файл
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",  # Имя файла для сохранения логов
    filemode="w",        # Режим записи: "a" (append) или "w" (overwrite)
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def main():
    try:
        # Загружаем всех персонажей
        await load_all_characters()
    except Exception as e:
        logging.error("An error occurred: %s", e)


if __name__ == "__main__":
    asyncio.run(main())
