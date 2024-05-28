import asyncio

from vovacool_bot_1 import start as start_bot_1
from vovacool_bot_2 import start as start_bot_2

async def main_bot():
    await asyncio.gather(start_bot_2(), start_bot_1())

if __name__ == "__main__":
    asyncio.run(main_bot())
