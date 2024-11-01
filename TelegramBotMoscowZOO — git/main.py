# main.py:
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
import logging
from Questions import start_quiz, get_result, reset_quiz
from Body import send_question, send_result, send_welcome_image
from Token import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    await send_welcome_image(bot, message.chat.id)  # Приветственное изображение
    await message.reply("А чтобы было интереснее, предлагаем Вам познакомиться с нашими обитателями "
                        "\nи определить на кого Вы больше всего похожи!🦁 \n\nНачнем тест?")
    reset_quiz(message.from_user.id)
    await send_question(bot, message.chat.id, 0)

@router.callback_query(lambda c: c.data.startswith('answer'))
async def handle_answer(callback_query: types.CallbackQuery):
    answer_index = int(callback_query.data.split('_')[1])
    question_index = int(callback_query.data.split('_')[2])
    if not start_quiz(callback_query.from_user.id, question_index, answer_index):
        result = get_result(callback_query.from_user.id)
        await send_result(bot, callback_query.from_user.id, result)
    else:
        await send_question(bot, callback_query.from_user.id, question_index + 1)
    await bot.answer_callback_query(callback_query.id)

@router.callback_query(lambda c: c.data == "retry")
async def retry_quiz(callback_query: types.CallbackQuery):
    reset_quiz(callback_query.from_user.id)
    await send_question(bot, callback_query.from_user.id, 0)
    await bot.answer_callback_query(callback_query.id)

@router.callback_query(lambda c: c.data == "privacy")
async def privacy_policy(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Ваши данные защищены и используются только для викторины.")
    await bot.answer_callback_query(callback_query.id)

@router.callback_query(lambda c: c.data == "contact")
async def contact(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Контактный телефон: +7(123)456-78-90, "
                                        "Email: https://moscowzoo.ru/about/guardianship")
    await bot.answer_callback_query(callback_query.id)

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
