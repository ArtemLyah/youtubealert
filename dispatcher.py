from aiogram import Bot, Dispatcher, executor
import config

bot = Bot(config.TOCKEN)
dp = Dispatcher(bot, executor.asyncio.get_event_loop())