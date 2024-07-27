import asyncio
from functions import create_table, bot, dp

# Starting the polling process for new updates
async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
 asyncio.run(main())