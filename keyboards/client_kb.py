from aiogram import types


button_create_plus = [types.InlineKeyboardButton(text="Создать счет и Пополнить баланс", callback_data='button1'),]
keyboard_create_plus = types.InlineKeyboardMarkup(row_width=1)
keyboard_create_plus.add(*button_create_plus)

button_plus = [types.InlineKeyboardButton(text="Пополнить баланс", callback_data='button1'),]
keyboard_plus = types.InlineKeyboardMarkup(row_width=1)
keyboard_plus.add(*button_plus)

