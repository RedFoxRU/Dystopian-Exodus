import asyncio
from bot import dp,bot, logger, set_commands
import models


import handlers



async def main():
    models.createDatabase()
    logger.info('DATABASE created')
    await set_commands()
    logger.info('commands registred')

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    dp.include_routers(handlers.client.router, handlers.keyboard.router)
    await dp.start_polling(bot)
    logger.info('Bot Started')

if __name__ == '__main__':
    asyncio.run(main())
