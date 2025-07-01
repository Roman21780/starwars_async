# Точка входа
from starwars_async.loader import load_all_characters
import asyncio

if __name__ == '__main__':
    asyncio.run(load_all_characters())
