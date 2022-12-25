import db_myql as db
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loggin_func import loggin_to_file
from config import API_TOKEN
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())