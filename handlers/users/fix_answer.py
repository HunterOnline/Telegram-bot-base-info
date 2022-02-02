import difflib
import json
import logging

from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from data.config import ADMINS

from keyboards.inline.fix_buttons import fix_keyboard, fix_callback, resolution_fix
from loader import dp, bot, db
from states import FixMessage
from states.fix_state import Del
from utils.misc import rate_limit


@rate_limit(5, "Количество значений в Базе 🗄")
@dp.message_handler(text="Количество значений в Базе 🗄")
async def func_count(message: types.Message, ):

    await message.answer(f'Всего значений в БД: {db.count_question_answer()[0][0]}')
    logging.info(message.from_user.full_name + " -> pressed [Количество значений в Базе 🗄]")


@dp.message_handler(text="Внести поправки 🛠")
async def function_fix(message: types.Message, ):
    with open("data/photo/photo_INFO.jpg", 'rb') as fail:
        await message.answer_photo(photo=fail, caption='Скопируй и пришли <u>вопрос</u> как на картинке 👆')
    await FixMessage.EnterQuestion.set()
    logging.info(message.from_user.full_name + " -> pressed [Внести поправки 🛠]")


@rate_limit(5, "Внести поправки 🛠")
@dp.message_handler(state=FixMessage.EnterQuestion)
async def enter_question(message: types.Message, state: FSMContext):
    await state.update_data(text_question=message.html_text, mention=message.from_user.get_mention())
    await message.answer('Вы собираетесь отправить текст <u>вопроса</u> на проверку', reply_markup=fix_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='back'), state=FixMessage.EnterQuestion)
async def back_question(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Еще раз скопируй и пришли <u>вопрос</u>:')


@dp.callback_query_handler(fix_callback.filter(action='send'), state=FixMessage.EnterQuestion)
async def send_question(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Теперь скопируй/пришли <u>ответ</u> на вопрос:')
    await FixMessage.next()





@dp.message_handler(state=FixMessage.EnterAnswer)
async def enter_answer(message: types.Message, state: FSMContext):
    await state.update_data(text_answer=message.html_text, mention=message.from_user.get_mention())
    await message.answer('Вы собираетесь отправить текст <u>ответа</u> на проверку', reply_markup=fix_keyboard)


@dp.message_handler(state=FixMessage.EnterAnswer, content_types=types.ContentType.PHOTO)
async def enter_answer(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo_answer=photo, mention=message.from_user.get_mention())
    await message.answer('Вы собираетесь отправить фото <u>ответа</u> на проверку', reply_markup=fix_keyboard)


@dp.callback_query_handler(fix_callback.filter(action='back'), state=FixMessage.EnterAnswer)
async def back_answer(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Еще раз скопируй и пришли <u>ответ</u>:')


@dp.callback_query_handler(fix_callback.filter(action='send'), state=FixMessage.EnterAnswer)
async def send_inquiry(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text_question = data.get('text_question')
        text_question = str(text_question).rstrip(":?")
        text_answer = data.get('text_answer')
        photo_answer = data.get('photo_answer')
        mention = data.get('mention')

    if text_answer is None:
        await call.message.answer(f'Данные приняты и отправлены на модерацыю: \n\n'
                                  f'вопрос: {text_question}\n\n'
                                  f'ответ 👇')
        await call.message.answer_photo(photo_answer)
    else:
        await call.message.answer(f'Данные приняты и отправлены на модерацыю: \n\n'
                                  f'вопрос: {text_question}\n\n'
                                  f'ответ: {text_answer}\n\n')

    await call.message.delete()
    user_id = call.from_user.id
    await bot.send_message(chat_id=ADMINS[0], text=f'Пользователь {mention} хочет внести поправки:')

    if text_answer is None:
        await bot.send_photo(chat_id=ADMINS[0], photo=photo_answer, caption=f'Вопрос:{text_question}&\n{user_id}',
                             reply_markup=resolution_fix)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f'{text_question}&\n{text_answer}&\n{user_id}',
                               parse_mode='HTML', reply_markup=resolution_fix, )
    await state.reset_state()


@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterQuestion)
@dp.callback_query_handler(fix_callback.filter(action='cancel'), state=FixMessage.EnterAnswer)
async def cancel_state(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

    await call.answer("Данные зброшены", show_alert=True)


@dp.callback_query_handler(fix_callback.filter(action='add'), user_id=ADMINS)
async def add_meaning(call: types.CallbackQuery):
    data = dict(db.select_all_sets())

    if call.message.text is None:

        """Download photo"""

        path_to_download = Path().joinpath('data', 'photo', 'add_new')
        path_to_download.mkdir(parents=True, exist_ok=True)
        path_to_download = path_to_download.joinpath(
            f"{call.message.photo[-1].file_unique_id}.jpg")  # call.message.photo[-1].file_unique_id call.message.caption[7:18] - вариант имени файла
        await call.message.photo[-1].download(destination=path_to_download)

        """Отбираем текст вопроса"""

        buf = call.message.caption
        buf = buf.split('&')
        chat_id = buf[1]
        buf = buf[0][7:]
        buf = str(buf).lower().rstrip('?')
        answer_json = json.dumps([f"{path_to_download}"])
        """Добавляем/Обновляем значения БД"""
        try:
            keys = difflib.get_close_matches(buf, data, 1, cutoff=0.98)[0]
            if 'data' in data[keys]:
                path = data[keys]
                path_to_photo = json.loads(path)
                file_path = Path(path_to_photo[0])
                file_path.unlink()
            db.update_question_answer(question=keys, answer=answer_json)
        except IndexError:
            db.add_question_answer(buf, answer=answer_json)
        await bot.send_message(chat_id=int(chat_id), text='Ваш запрос добавлен в БД')
        """Добавляем/Обновляем значения БД если ответ текст"""
    else:
        buf = call.message.text
        buf = buf.split('&')

        try:
            keys = difflib.get_close_matches(str(buf[0]).lower(), dict(data), 1, cutoff=0.98)[0]
            db.update_question_answer(question=keys, answer=str(buf[1]).lstrip('\n'))
        except IndexError:
            db.add_question_answer(question=str(buf[0]).lower(), answer=str(buf[1]).lstrip('\n'))
            await bot.send_message(chat_id=int(buf[2]), text='Ваш запрос добавлен в БД')

    db.unload_data()
    await call.answer('Вы добавили/изменили значения БД', show_alert=True)

    await call.message.delete()


@dp.callback_query_handler(fix_callback.filter(action='cancellation'), user_id=ADMINS)
async def cancell_fanck(call: types.CallbackQuery):
    if call.message.text is None:
        buf = call.message.caption
    else:
        buf = call.message.text
    buf = buf.split('&')
    await bot.send_message(chat_id=int(buf[-1]), text='Ваш запрос в БД отклонен')
    await call.message.delete()
    await call.answer('Запрос отклонён', show_alert=True)


@dp.message_handler(Command("delete"), user_id=ADMINS)
async def function_delete(message: types.Message, ):
    await message.answer('Скопируй/пришли вопрос для удаления с БД :')
    await Del.DelQuestionAnswer.set()


@dp.message_handler(state=Del.DelQuestionAnswer)
async def delete_question(message: types.Message, state: FSMContext):
    data = str(message.html_text).lower()
    main_data = dict(db.select_all_sets())
    try:
        keys = difflib.get_close_matches(data, main_data, 1, cutoff=0.98)[0]
        if 'data' in main_data[keys]:
            path = main_data[keys]
            path_to_photo = json.loads(path)
            file_path = Path(path_to_photo[0])
            file_path.unlink()
        db.delete_question_answer(keys)

        db.unload_data()
        await message.answer("Внесенные значение удалено с БД")
    except IndexError:
        await message.answer("Такого значения нет в БД")
    await state.finish()
