from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
b1 = KeyboardButton(text="Выгрузка пользователей с их балансом")
b2 = KeyboardButton(text="Выгрузка логов")
b3 = KeyboardButton(text="Изменить баланс пользователя")
b4 = KeyboardButton(text="Заблокировать пользователя")
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(b1).add(b2).add(b3).add(b4)
