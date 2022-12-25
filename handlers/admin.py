import db_myql as db
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
import keyboards as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loggin_func import loggin_to_file
from config import API_TOKEN



class Admin:
    def __init__(self, message: types.Message):
        message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре',
                       reply_markup=kb_admin)
    async def export_file(message: types.Message):
        db.export_file()
        await bot.send_message(message.from_user.id, "Выгружено в файл file.csv")
        # await message.reply("Выгружено в файл file.csv")

    @dp.message_handler(lambda message: message.text == "Заблокировать пользователя")
    async def block_user(message: types.Message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Назад"))
        await message.answer('Введите name пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже',
                             reply_markup=keyboard)
        await Test.blacklist.set()

    @dp.message_handler(state=Test.blacklist)
    async def proce(message: types.Message, state: FSMContext):
        if message.text == 'Назад':
            await message.answer('Отмена! Возвращаю назад.', reply_markup=kb)
            await state.finish()
        else:
            answer_block = message.text
            if db.select_user(answer_block) is None:
                await bot.send_message(message.from_user.id, "Нет такого пользователя")
                await state.finish()
            else:
                db.block_user(answer_block)
                await bot.send_message(message.from_user.id, answer_block + " заблокирован")
                await state.finish()

    @dp.message_handler(lambda message: message.text == "Выгрузка пользователей с их балансом")
    async def export_file(message: types.Message):
        db.export_file()
        await bot.send_message(message.from_user.id, "Выгружено в файл file.csv")
        # await message.reply("Выгружено в файл file.csv")

    @dp.message_handler(lambda message: message.text == "Изменить баланс пользователя")
    async def change_balance1(message: types.Message):
        await bot.send_message(message.from_user.id, "Введите пользователя")
        await Test.Q3.set()

    @dp.message_handler(state=Test.Q3)
    async def change_balance2(message: types.Message, state: FSMContext):
        answer3 = message.text
        await state.update_data(answer3=answer3)
        await bot.send_message(message.from_user.id, "Введите сумму, на которую вы хотите изменить баланс")
        await Test.Q4.set()

    @dp.message_handler(state=Test.Q4)
    async def change_balance3(message: types.Message, state: FSMContext):
        data = await state.get_data()
        answer3 = data.get("answer3")
        answer4 = message.text
        if db.select_user(answer3) is None:
            await bot.send_message(message.from_user.id, "Нет такого пользователя")
        else:
            db.update_users(answer3, answer4)

            await bot.send_message(message.from_user.id, "Баланс изменен")
        await state.finish()

