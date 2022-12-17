import db_myql as db
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
import keyboards as kb
from mysql.connector import connect
import mysql.connector
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loggin_func import loggin_to_file

DB_HOST = 'localhost'
DB_USER = 'summy'
DATABASE_NAME = 'bot'
DB_PASSWORD = 'summy'
DB_PORT = '3306'
TEST_DATABASE_NAME = 'mydb'

mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DATABASE_NAME
)
mycursor = mydb.cursor()


API_TOKEN = '5909535015:AAFB676Jm6icCfOnLmJ32ss2fUwkKbt2M5A' # Токен
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    blacklist = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.first_name == 'D':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.InlineKeyboardButton(text="Выгрузка пользователей с их балансом", callback_data='button1'))
        keyboard.add(types.InlineKeyboardButton(text="Выгрузка логов"))
        keyboard.add(types.InlineKeyboardButton(text="Изменить баланс пользователя"))
        keyboard.add(types.InlineKeyboardButton(text="Заблокировать пользователя"))
        await message.answer('Добро пожаловать в Админ-Панель! Выберите действие на клавиатуре', reply_markup=keyboard)
    else:
        if db.select_user(message.from_user.first_name) is None:
            buttons = [
                types.InlineKeyboardButton(text="Создать счет и Пополнить баланс", callback_data='button1'),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message.answer("Привет " + str(message.from_user.first_name) +
                                 "\nЯ - бот для создания пользователя и пополнения баланса"
                                 "\nНажмите на кнопку, чтобы создать пользователя и пополнить баланс",
                                 reply_markup=keyboard)

        else:
            buttons = [
                types.InlineKeyboardButton(text="Пополнить баланс", callback_data='button1'),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message.answer("Привет " +str(message.from_user.first_name) +
                                 "\nЯ - бот для пополнения баланса"
                                 "\nНажмите на кнопку, чтобы пополнить баланс",
                                 reply_markup=keyboard)
#adminka
@dp.message_handler(lambda message: message.text == "Выгрузка логов")
async def loggin_export(message: types.Message):
    loggin_to_file()
    await message.answer('Выгружено в файл')


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
    answer3 = data .get("answer3")
    answer4 = message.text
    if db.select_user(answer3) is None:
        await bot.send_message(message.from_user.id, "Нет такого пользователя")
    else:
        db.update_users(answer3, answer4)

        await bot.send_message(message.from_user.id, "Баланс изменен")
    await state.finish()



#users
@dp.callback_query_handler(text="button1")
async def process_hi2_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите сумму, на которую вы хотите пополнить баланс")
    await Test.Q2.set()

@dp.message_handler(state=Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer2 = message.text
    if db.select_user(message.from_user.first_name) is None:
        db.create_user(message.from_user.first_name, answer2)
    else:
        db.update_users(message.from_user.first_name, answer2)
        db.insert_payment(message.from_user.first_name, answer2, datetime.now())
        await state.update_data(answer6="Ok")
        data = await state.get_data()
        print(data. get("answer6"))


    buttons = [
        types.InlineKeyboardButton(text="Проверить оплату", callback_data='check_pay'),
        types.InlineKeyboardButton(text="Прошел ли платеж", callback_data='is_pay_true'),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer( str(message.from_user.first_name) +
                         "\nВаш счет создан",
                         reply_markup=keyboard)

    # Вариант 1
    await state.finish()


@dp.callback_query_handler(text="check_pay")
async def process_hi2_command(message: types.Message):
    await message.answer("Оплата прошла")
@dp.callback_query_handler(text="is_pay_true")
async def process_hi2_command(message: types.Message):
    await message.answer("Платеж прошел")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)