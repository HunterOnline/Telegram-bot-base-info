from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Как вносить поправки 📃")],

        [KeyboardButton(text="Внести поправки 🛠")],

        [KeyboardButton(text="Количество значений в Базе 🗄")],

    ], resize_keyboard=True,


    )
