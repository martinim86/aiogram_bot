from datetime import datetime
from aiogram.utils.callback_data import CallbackData
from state_func import Test
from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import dp, bot
from keyboards import keyboard_create_plus, keyboard_plus
from db.db_myql import Database
db = Database()
class Client:
    async def start_client(message: types.Message):
        if db.select_user(message.from_user.first_name) is None:
            await message.answer("Привет " + str(message.from_user.first_name) +
                                     "\nЯ - бот для создания пользователя и пополнения баланса"
                                     "\nНажмите на кнопку, чтобы создать пользователя и пополнить баланс",
                                     reply_markup=keyboard_create_plus)

        else:
            await message.answer("Привет " +str(message.from_user.first_name) +
                                     "\nЯ - бот для пополнения баланса"
                                     "\nНажмите на кнопку, чтобы пополнить баланс",
                                     reply_markup=keyboard_plus)
    @dp.callback_query_handler(text="button1")
    async def process_hi2_command(message: types.Message):
        await bot.send_message(message.from_user.id, "Введите сумму, на которую вы хотите пополнить баланс")
        await Test.Q2.set()

    vote_cb = CallbackData('vote', 'action', 'amount')
    @dp.message_handler(state=Test.Q2)
    async def answer_q2(message: types.Message, state: FSMContext):
        vote_cb = CallbackData('vote', 'action', 'amount')
        answer2 = message.text
        if db.select_user(message.from_user.first_name) is None:
            db.create_user(message.from_user.first_name, answer2)
        else:
            db.update_users(message.from_user.first_name, answer2)
            try:
                db.insert_payment(message.from_user.first_name, answer2, datetime.now())
                amount = 1
            except ValueError:
                print("Oops!  That was no valid pay")


        buttons = [
            types.InlineKeyboardButton(text="Проверить оплату", callback_data=vote_cb.new(action='up', amount=amount)),
            types.InlineKeyboardButton(text="Ссылка на оплату", url = "https://qiwi.com/"),

        ]
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*buttons)
        await message.answer( str(message.from_user.first_name) +
                             "\nВаш счет создан",
                             reply_markup=keyboard)

        # Вариант 1
        await state.finish()


    @dp.callback_query_handler(vote_cb.filter(action='up'))
    async def process_hi2_command1(message: types.CallbackQuery, callback_data: dict):
        amount = int(callback_data['amount'])
        if amount == 1:
            await message.answer("Оплата прошла")

    @dp.callback_query_handler(text="is_pay_true")
    async def process_hi2_command(message: types.Message):
        await message.answer("Платеж прошел")

