import json
import logging

from aiogram import types

from loader import dp, db
import difflib

from utils.misc import rate_limit

"""Хендлер описание для юзера"""


@rate_limit(5, "Как вносить поправки 📃")
@dp.message_handler(text="Как вносить поправки 📃")
async def show_info(message: types.Message, ):
    with open("data/photo/photo_INFO.jpg", 'rb') as fail:
        await message.answer("Как получить ответ, смотри на картинку 👇")
        await message.answer_photo(photo=fail, caption=f"Копируй и пришли мне вопрос"
                                                       f" как на картинке! ☝")
        await message.answer("Бот не имеет всех ответов на вопросы,\n"
                             "поэтому в Ebash_Bot есть функцыя для добавления\n"
                             "в базу вопросов с ответами та обновления ответа если ответ\n"
                             "не правельный.\n"
                             "Если Ты знаешь правильный ответ пользуйся данной фитчей!!!\n"
                             "- Жми кнопку 👉 \"Внести поправки 🛠\"\n"
                             "- копируй и отправляй вопрос\n"
                             "- жми кнопку отпрвить\n"
                             "- копируй и отправляй ответ(фото тоже можно)\n"
                             "- жми кнопку отпрвить")
        logging.info(message.from_user.full_name + " -> pressed [Как вносить поправки 📃]")


"""Хендлер для ключа с типом значения string and list"""


@dp.inline_handler(types.InlineQuery)
async def inline_handler(query: types.InlineQuery):

    keys = difflib.get_close_matches(str(query.query).lower(), db.buf_data.keys(), 10, cutoff=0.15)
    articles = [types.InlineQueryResultArticle(id=str(i), title=key, description=db.buf_data[key],
                                               input_message_content=types.InputTextMessageContent(
                                                   message_text=str(key))) for i, key in enumerate(keys, start=1)
                ]
    await query.answer(articles, cache_time=30, is_personal=True)
    logging.info(query.from_user.full_name + ' -> inline Search')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def answer(message: types.Message):

    try:
        keys = difflib.get_close_matches(str(message.text).lower(), db.buf_data.keys(), 1, cutoff=0.95)[
            0]  # сравненин строки с ключом по набольшему совпадию
        if 'data' in db.buf_data[keys]:
            photos = json.loads(db.buf_data[keys])
            await message.answer('Варианты ответа:')
            for photo in photos:
                with open(photo, 'rb') as fail:
                    await message.answer_photo(photo=fail)

        else:

            await message.answer(db.buf_data[keys])
        logging.info(message.from_user.full_name + ' -> got an answer')
    except IndexError:
        await message.answer('Я еще не знаю ответ на этот вопрос 😔')
        logging.info(message.from_user.full_name + ' for question: ' + message.text + ' -> no answer')
