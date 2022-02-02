from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

fix_callback = CallbackData("fix_mess", "action")

fix_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data=fix_callback.new(action='send')),
            InlineKeyboardButton(text="Редактировать", callback_data=fix_callback.new(action='back')),
        ],
        [
            InlineKeyboardButton(text="Выйти", callback_data=fix_callback.new(action='cancel'))
        ]

    ]
)
resolution_fix = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Обновить/добавить", callback_data=fix_callback.new(action='add')),
            InlineKeyboardButton(text="Отменить", callback_data=fix_callback.new(action='cancellation')),
        ]
        ]
)


post_buttons =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отправить", callback_data=fix_callback.new(action='post')),
         InlineKeyboardButton(text="Збросить", callback_data=fix_callback.new(action='del_post'))
         ]
    ])