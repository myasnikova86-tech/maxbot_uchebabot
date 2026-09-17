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

# === НОВОЕ ===
# Словарь: кто сейчас пишет вопрос учителю
# {user_id: True/False}
user_waiting_question = {}


# ======================== ФУНКЦИИ КЛАВИАТУР ========================
def get_info_keyboard():
    kb = InlineKeyboardBuilder()
    kb.row(MessageButton(text='Я пропустил лекцию :('))
    kb.row(MessageButton(text='Сдать ДЗ'))
    kb.row(MessageButton(text='Какой у меня вариант?'))
    kb.row(MessageButton(text='✉️ Задать вопрос учителю'))  # === НОВОЕ ===
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
    await track_user(event.chat_id)
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
    await track_user(event.from_user.user_id)

    if event.from_user.user_id != ADMIN_ID:
        await event.message.answer("⛔ У вас нет доступа к этой команде.")
        return

    total = len(unique_users)
    await event.message.answer(f"📊 Статистика:\nВсего уникальных пользователей: {total}")

# === НОВОЕ ===
# ---------- КОМАНДА /reply (только для админа) ----------
# Использование: /reply <user_id> <текст ответа>
@dp.message_created(Command('reply'))
async def cmd_reply(event: MessageCreated):
    # Только админ может отвечать
    if event.from_user.user_id != ADMIN_ID:
        return

    text = event.message.body.text
    parts = text.split(maxsplit=2)

    if len(parts) < 3:
        await event.message.answer(
            "Использование: /reply <user_id> <текст ответа>\n"
            "Например: /reply 987654321 Посмотри лекцию на стр. 12"
        )
        return

    try:
        target_id = int(parts[1])
        answer_text = parts[2]
    except ValueError:
        await event.message.answer("❌ user_id должен быть числом.")
        return

    try:
        await bot.send_message(
            user_id=target_id,
            text=f"📬 Ответ учителя:\n\n{answer_text}"
        )
        await event.message.answer(f"✅ Ответ отправлен пользователю {target_id}.")
    except Exception as e:
        await event.message.answer(f"❌ Не удалось отправить ответ: {e}")

# ---------- Обработка всех текстовых сообщений (кнопки, темы и т.д.) ----------
@dp.message_created(F.message.body.text)
async def handle_all_text(event: MessageCreated):
    await track_user(event.from_user.user_id)

    text = event.message.body.text
    user_id = event.from_user.user_id

    # === НОВОЕ ===
    # Если пользователь сейчас пишет вопрос учителю — перехватываем сообщение
    if user_waiting_question.get(user_id):
        user_waiting_question[user_id] = False  # выключаем режим

        # Пересылаем вопрос админу
        try:
            await bot.send_message(
                user_id=ADMIN_ID,
                text=(
                    f"📩 Вопрос от {event.from_user.first_name} "
                    f"(ID: {user_id}):\n\n{text}\n\n"
                    f"Чтобы ответить, отправь:\n/reply {user_id} <твой ответ>"
                )
            )
            # Подтверждаем пользователю
            await bot.send_message(
                user_id=user_id,
                text="✅ Твой вопрос отправлен учителю. Ответ придёт сюда же."
            )
        except Exception as e:
            logging.error(f"Ошибка при пересылке вопроса: {e}")
            await bot.send_message(
                user_id=user_id,
                text="⚠️ Не удалось отправить вопрос. Попробуй позже."
            )
        return  # ВАЖНО: выходим, чтобы не обрабатывать текст как кнопку

    # Обработка выбора темы лекции (6 тем)
    if text.startswith("Тема "):
        message = TOPICS_MESSAGES.get(text, "Информация по этой теме временно отсутствует")
        await bot.send_message(user_id=user_id, text=message)
        return

    # Кнопка "Информатика"
    if text == "Информатика":
        await bot.send_message(
            user_id=user_id,
            text="Выбери нужную кнопку:",
            attachments=[get_info_keyboard()]
        )
    # Кнопка "Я пропустил лекцию :("
    elif text == "Я пропустил лекцию :(":
        await bot.send_message(
            user_id=user_id,
            text="Выбери лекцию, которую ты пропустил:",
            attachments=[get_topics_keyboard()]
        )
    # === НОВОЕ ===
    # Кнопка "Задать вопрос учителю"
    elif text == "✉️ Задать вопрос учителю":
        user_waiting_question[user_id] = True
        await bot.send_message(
            user_id=user_id,
            text="✍️ Напиши свой вопрос одним сообщением, и я передам его учителю."
        )
    # Кнопки "Сдать ДЗ" и "Какой у меня вариант?"
    elif text in ("Сдать ДЗ", "Какой у меня вариант?"):
        if text == "Сдать ДЗ":
            response = "Загрузи задание в раздел 'Домашнее задание' в личном кабинете."
        else:
            variant_number = random.randint(1, 10)
            response = f"Ваш вариант: {variant_number}"
        await bot.send_message(user_id=user_id, text=response)
    # Кнопки "Да"/"Нет" и всё остальное
    else:
        await bot.send_message(user_id=user_id, text=f'Вы выбрали "{text}"')

# ======================== ЗАПУСК ========================
async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
