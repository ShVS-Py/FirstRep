from aiogram import Bot, types
from Questions import questions, get_result

async def send_welcome_image(bot: Bot, chat_id: int):
    await bot.send_photo(chat_id,
                         photo="https://filearchive.cnews.ru/img/book/2022/04/13/moskovskij_zoopark.png",
                         caption="Добро пожаловать в МОСКОВСКИЙ ЗООПАРК! \n\nХотим рассказать Вам о программе «Клуб друзей зоопарка»\n\n"
                                 "Участие в программе «Клуб друзей зоопарка» — это помощь в содержании наших обитателей, \n"
                                 "а также ваш личный вклад в дело сохранения биоразнообразия Земли и развитие нашего зоопарка."
                                 "\n\nОсновная задача Московского зоопарка с самого начала его существования это — сохранение биоразнообразия планеты. \n\n"
                                 "Когда вы берете под опеку животное, вы помогаете нам в этом благородном деле.")

async def send_question(bot: Bot, chat_id: int, question_index: int):
    question = questions[question_index]
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=answer, callback_data=f"answer_{i}_{question_index}")]
        for i, answer in enumerate(question["answers"])
    ])
    await bot.send_message(chat_id, question["question"], reply_markup=markup)

async def send_result(bot: Bot, chat_id: int, result_data):
    animal, description, image_url = result_data
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Попробовать ещё раз?", callback_data="retry")],
        [types.InlineKeyboardButton(text="Политика конфиденциальности", callback_data="privacy")],
        [types.InlineKeyboardButton(text="Контакты", callback_data="contact")]
    ])
    await bot.send_photo(chat_id, photo=image_url, caption=f"Результат: {animal}\n\n{description}", reply_markup=markup)
