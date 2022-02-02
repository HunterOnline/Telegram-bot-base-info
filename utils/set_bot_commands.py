
from aiogram import types





async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("delete", "Удалить значения(Admin)"),
        types.BotCommand("arr_user", "Массив юзеров(Admin)"),
        types.BotCommand("count_user", "Счетчик юзеров (Admin)"),
        types.BotCommand("del_user", "Удалить пользователя(Admin)"),
        types.BotCommand("post", "Зделать россылку(Admin)")


    ])
