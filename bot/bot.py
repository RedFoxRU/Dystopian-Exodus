from aiogram import Bot, Dispatcher, types

from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, PWD
from loguru import logger
from service.stack import Stack


stack = Stack()

logger.add(PWD+'/logs/debug.log', format="{time} {level} {message}", level="DEBUG", rotation="10 KB", compression='zip')

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(storage=storage)

async def set_commands():
    commands = [
        types.BotCommand(command="/start", description="Вывести приветствие/начать игру"),
        types.BotCommand(command="/create", description="Создать игру"),
    ]
    await bot.set_my_commands(commands)
