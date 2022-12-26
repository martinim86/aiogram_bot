from aiogram import executor
from aiogram import types
from create_bot import dp
from handlers.class_admin import Admin
from handlers.class_client import Client
async def on_startup(_):
    print('Бот вышел в онлайн')


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await Client.start_client(message)
@dp.message_handler(commands=['admin'])
async def process_start_command(message: types.Message):
    await Admin.start_admin(message) 


# client.registre_handlers_client(dp)
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
