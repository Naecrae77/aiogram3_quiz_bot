import asyncio
from functions import bot, dp
from create_table import create_table

# Starting the polling process for new updates
async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
 asyncio.run(main())

#NaecraeCode
