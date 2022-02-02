import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config

from utils.db_api.BD_user import UserDatabase
from utils.db_api.DB import Database
# from utils.db_api.main_pg_db import DatabaseMainPG
# from utils.db_api.users_pg_bd import DatabaseUsersPG

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
db_user = UserDatabase()
db_low = Database()







