import logging
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.inline.fix_buttons import post_buttons, fix_callback
from loader import dp, db_user, bot
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("count_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    await message.answer(f'Всего значений в БД User: {db_user.count_user()[0][0]}')


@dp.message_handler(Command("del_user"), user_id=ADMINS, )
async def del_user(message: types.Message, state: FSMContext):
    await message.answer('пришли id пользователя для удаления с БД Users :')
    await state.set_state('Del_user')


@dp.message_handler(state='Del_user')
async def delete_user(message: types.Message, state: FSMContext):
    data = message.html_text
    try:
        user = db_user.select_user_parm(int(data))
        db_user.delete_user(int(data))
        await message.answer(f'Пользователь {str(user[0][2])}:\nУспешно удален с БД')
    except ValueError as v:
        logging.info(f"{v}")
        await message.answer("Некорректное значения!")

    await state.finish()


@dp.message_handler(Command("arr_user"), user_id=ADMINS)
async def func_user_count(message: types.Message, ):
    user = [f"{str(i[0])}. {i[2]}" for i in  db_user.select_all_sets()]
    await message.answer("\n".join(user))


"""           Post Command            """


@dp.message_handler(Command("post"), user_id=ADMINS)
async def post_fo_users(message: types.Message, state: FSMContext):
    await message.answer("Ведите текст поста")
    await state.set_state("text_post")


@dp.message_handler(state="text_post")
async def create_post(message: types.Message, state: FSMContext):
    await state.update_data(text_post=message.html_text)
    await message.answer(f'Вы собираетесь отправить текст:\n{message.text}', reply_markup=post_buttons)


@dp.callback_query_handler(fix_callback.filter(action='del_post'), state="text_post")
async def dell_post_users(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Данные зброшены", show_alert=True)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(fix_callback.filter(action='post'), state="text_post")
async def send_post_users(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text_post = data.get('text_post')

    await call.message.delete()

    user = [int(i[1]) for i in db_user.select_all_sets()]

    for us in user:
        try:

            await dp.bot.send_message(chat_id=us, text=text_post)
        except Exception as err:
            print(err)
    await state.finish()
