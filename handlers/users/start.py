import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.menu_buttons import menu
from loader import dp, db_user, bot  # pg_db_users


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.get_mention()
    user_id = message.from_user.id
    await bot.send_message(text=f"Привет, {message.from_user.full_name}!", chat_id=user_id, reply_markup=menu)
    user = [i[1] for i in db_user.select_all_sets()]
    if user_id in user:
        logging.info(f"{message.from_user.full_name} -> уже есть БД_S")
    else:
        try:
            db_user.add_user(user_id, name)
            logging.info(f"{message.from_user.full_name} -> записани в БД")

        except Exception as e:
            print(e)
