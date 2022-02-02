from aiogram import types

from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/info - Как получить ответ",
            "/fix -  Внести поправки(добавить/изменить вопрос/ответ)",
            "/count - Счетчик значений БД"
            )
    
    await message.answer("\n".join(text))



