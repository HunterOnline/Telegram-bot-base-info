import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboards.default.menu_buttons import menu
from loader import db_user, dp


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:

            await dp.bot.send_message(admin, "#@Ebash_new_bot....loaded")

        except Exception as err:

            logging.exception(err)


async def on_startup_menu():
    for users in db_user.select_all_sets():

        try:

            await dp.bot.send_message(text='#@Ebash_new_bot....loaded...menu', chat_id=users[1], reply_markup=menu)

        except Exception as err:

            logging.exception(err)
