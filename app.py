import asyncio

from aiogram import executor

from utils.set_bot_commands import set_default_commands
from loader import dp, db, db_user  # pg_db, pg_db_users

import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify, on_startup_menu


async def on_startup(dispatcher):
    try:

        db.create_table_question_answer()
    except Exception as e:
        print(e)
    try:
        db_user.create_user_table()

    except Exception as e:
        print(e)

    db.unload_data()
    await on_startup_notify(dispatcher)
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
