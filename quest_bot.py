from aiogram import Bot, Dispatcher, executor, types
import logging
import os

logging.basicConfig(level=logging.INFO)

# Получаем токен из переменной окружения
API_TOKEN = os.getenv("7612341931:AAGmwYNJtrdgB9BBEQY13miUCW-888lbTe4")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Список загадок и ответов
QUESTS = [
    {"question": "Я мягкая и пушистая. Спишь ты на мне. Где я?", "answer": "подушка"},
    {"question": "Утром я показываю твоё лицо. Где я?", "answer": "зеркало"},
    {"question": "Там хранятся вкусняшки и холод. Где я?", "answer": "холодильник"},
    {"question": "Я разогреваю еду, но не микроволновка. Где я?", "answer": "духовка"},
    {"question": "Там живут книги. Где я?", "answer": "книжная полка"},
]

# Словарь, чтобы отслеживать прогресс каждого пользователя
user_progress = {}

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    user_id = message.from_user.id
    user_progress[user_id] = 0
    await message.answer("🎉 Привет! Это квест по дому 🎁\nОтгадай, где спрятан подарок!\n\nВот первая загадка:")
    await message.answer(QUESTS[0]['question'])

# Обработка всех текстовых сообщений (ответов)
@dp.message_handler()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    progress = user_progress.get(user_id, 0)

    # Если квест пройден — поздравляем
    if progress >= len(QUESTS):
        await message.answer("🎉 Ты уже прошла весь квест! Поищи подарок там, где живут книги 😉")
        return

    correct_answer = QUESTS[progress]['answer'].lower()
    user_reply = message.text.strip().lower()

    if user_reply == correct_answer:
        progress += 1
        user_progress[user_id] = progress
        if progress < len(QUESTS):
            await message.answer("✅ Верно! Следующая загадка:")
            await message.answer(QUESTS[progress]['question'])
        else:
            await message.answer("🏁 Квест завершён! Подарок ждёт тебя на книжной полке 📚")
    else:
        await message.answer("❌ Хм... не совсем. Попробуй ещё раз!")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
