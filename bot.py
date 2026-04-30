import asyncio
import logging
import os
import random
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageButton, MessageCreated, Command, BotStarted
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# ======================== НАСТРОЙКА ========================
logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Переменная окружения TOKEN не задана!")
    exit(1)

bot = Bot(TOKEN)
dp = Dispatcher()

# Множество для хранения уникальных ID пользователей
unique_users = set()

ADMIN_ID = os.environ.get('ADMIN_ID')
if not ADMIN_ID:
    logging.critical("Переменная окружения ADMIN_ID не задана!")
    exit(1)
try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    logging.critical("ADMIN_ID должен быть числом!")
    exit(1)


# ======================== ФУНКЦИИ КЛАВИАТУР ========================
def get_info_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(MessageButton(text='Я пропустил лекцию :('))
    kb.row(MessageButton(text='Сдать ДЗ'))
    kb.row(MessageButton(text='Какой у меня вариант?'))
    return kb.as_markup()

def get_topics_keyboard():
    kb = InlineKeyboardBuilder()
    topics = [
        'Тема 1. Системы счисления',
        'Тема 2. Алгебра логики',
        'Тема 3. Интернет',
        'Тема 4. Защита информации',
        'Тема 5. Текстовый процессор',
        'Тема 6. Компьютерная графика'
    ]
    for topic in topics:
        kb.row(MessageButton(text=topic))
    return kb.as_markup()

TOPICS_MESSAGES = {
    "Тема 1. Системы счисления": "Тема 1. Системы счисления. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/APQE4mDwBTSbkA",
    "Тема 2. Алгебра логики": "Тема 2. Алгебра логики. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/BPjzUvFeiSOvVw",
    "Тема 3. Интернет": "Тема 3. Интернет. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/w_85PUK6rneizQ",
    "Тема 4. Защита информации": "Тема 4. Защита информации. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/JycaZ67-mUxadQ",
    "Тема 5. Текстовый процессор": "Тема 5. Текстовый процессор. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/aiykc237nTqJBg",
    "Тема 6. Компьютерная графика": "Тема 6. Компьютерная графика. Задание: Напиши конспект Лекции в тетрадь, выполни все задания лекции. Тетрадь с Лекцией и выполненными заданиями сдай учителю. И не забудь про ДЗ! Ссылка на материалы: https://disk.yandex.ru/d/qKQ3ZFQHg59wGQ",
}

# ======================== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ========================
async def track_user(user_id):
    """Добавляет пользователя в множество уникальных"""
    unique_users.add(user_id)

# ======================== ОБРАБОТЧИКИ ========================
@dp.bot_started()
async def bot_started(event: BotStarted):
    await track_user(event.chat_id)  # добавляем пользователя
    kb = InlineKeyboardBuilder()
    kb.row(MessageButton(text='Информатика'))
    kb.row(MessageButton(text='Иностранный язык'))
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='👋 Привет! Ты что-то пропустил? Выбери дисциплину:',
        attachments=[kb.as_markup()]
    )

@dp.message_created(Command('start'))
async def start_message(event: MessageCreated):
    await track_user(event.from_user.user_id)
    await event.message.answer("Обработка команды start")

@dp.message_created(Command('id'))
async def cmd_id(event: MessageCreated):
    await track_user(event.from_user.user_id)
    user_id = event.from_user.user_id
    name = event.from_user.first_name
    await event.message.answer(f"Привет, {name}!\nТвой ID: {user_id}")

@dp.message_created(Command('test'))
async def test_message(event: MessageCreated):
    await track_user(event.from_user.user_id)
    reply_kb = InlineKeyboardBuilder()
    reply_kb.row(MessageButton(text='Да'), MessageButton(text='Нет'))
    await bot.send_message(
        user_id=event.from_user.user_id,
        text='Текстовое сообщение с кнопками',
        attachments=[reply_kb.as_markup()]
    )

# ---------- КОМАНДА /stats (только для админа) ----------
@dp.message_created(Command('stats'))
async def show_stats(event: MessageCreated):
    await track_user(event.from_user.user_id)  # админа тоже считаем

    # Проверяем, что команду отправил администратор
    if event.from_user.user_id != ADMIN_ID:
        await event.message.answer("⛔ У вас нет доступа к этой команде.")
        return

    total = len(unique_users)
    await event.message.answer(f"📊 Статистика:\nВсего уникальных пользователей: {total}")

# ---------- Обработка всех текстовых сообщений (кнопки, темы и т.д.) ----------
@dp.message_created(F.message.body.text)
async def handle_all_text(event: MessageCreated):
    # Добавляем пользователя в статистику при любом его действии
    await track_user(event.from_user.user_id)

    text = event.message.body.text

    # Обработка выбора темы лекции (6 тем)
    if text.startswith("Тема "):
        message = TOPICS_MESSAGES.get(text, "Информация по этой теме временно отсутствует")
        await bot.send_message(user_id=event.from_user.user_id, text=message)
        return

    # Кнопка "Информатика"
    if text == "Информатика":
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Выбери нужную кнопку:",
            attachments=[get_info_keyboard()]
        )
    # Кнопка "Я пропустил лекцию :("
    elif text == "Я пропустил лекцию :(":
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Выбери лекцию, которую ты пропустил:",
            attachments=[get_topics_keyboard()]
        )
    # Кнопки "Сдать ДЗ" и "Какой у меня вариант?"
    elif text in ("Сдать ДЗ", "Какой у меня вариант?"):
        if text == "Сдать ДЗ":
            response = "Загрузи задание в раздел 'Домашнее задание' в личном кабинете."
        else:
            variant_number = random.randint(1, 10)
            response = f"Ваш вариант: {variant_number}"
        await bot.send_message(user_id=event.from_user.user_id, text=response)
    # Кнопки "Да"/"Нет" и всё остальное
    else:
        await bot.send_message(user_id=event.from_user.user_id, text=f'Вы выбрали "{text}"')

# ======================== ЗАПУСК ========================
async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
