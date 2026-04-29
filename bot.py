import asyncio
import logging
import os
import random
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageButton, MessageCreated, Command, BotStarted
from maxapi.types import ButtonsPayload, Attachment
from maxapi.types import LinkButton, MessageCallback, CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.enums.intent import Intent

def get_info_keyboard():
    """Возвращает клавиатуру с тремя кнопками для раздела Информатика"""
    kb = InlineKeyboardBuilder()
    kb.row(MessageButton(text='Я пропустил лекцию :('))
    kb.row(MessageButton(text='Сдать ДЗ'))
    kb.row(MessageButton(text='Какой у меня вариант?'))
    return kb.as_markup()

def get_topics_keyboard():
    """Клавиатура с 6 темами лекций"""
    kb = InlineKeyboardBuilder()
    kb.row(MessageButton(text='Тема 1. Системы счисления'))
    kb.row(MessageButton(text='Тема 2. Алгебра логики'))
    kb.row(MessageButton(text='Тема 3. Интернет'))
    kb.row(MessageButton(text='Тема 4. Защита информации'))
    kb.row(MessageButton(text='Тема 5. Текстовый процессор'))
    kb.row(MessageButton(text='Тема 6. Компьютерная графика'))
    return kb.as_markup()

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Переменная окружения TOKEN не задана!")
    exit(1)

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.bot_started()
async def bot_started(event: BotStarted):
    # Создаём клавиатуру
    kb = InlineKeyboardBuilder()
    # Каждая кнопка добавляется в свой отдельный ряд
    kb.row(MessageButton(text='Информатика'))
    kb.row(MessageButton(text='Иностранный язык'))
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='👋 Привет! Ты что-то пропустил? Выбери дисциплину:',
        attachments=[kb.as_markup()]
    )

@dp.message_created(Command('start'))
async def start_message(event: MessageCreated):
    await event.message.answer(f"Обработка команды start")

@dp.message_created(Command('id'))
async def hello(event: MessageCreated):
    await event.message.answer(f'''Привет, {event.from_user.first_name}!
Твой ID в мессенджере: {event.from_user.user_id}''')

@dp.message_created(Command('test'))
async def test_message(event: MessageCreated):
    reply_kb = InlineKeyboardBuilder()
    reply_kb.row(MessageButton(text='Да'), MessageButton(text='Нет'))
    await bot.send_message(user_id=event.from_user.user_id, text='Текстовое сообщение с кнопками',
                       attachments=[reply_kb.as_markup()])

@dp.message_created(F.message.body.text)
async def handle_all_text(event: MessageCreated):
    text = event.message.body.text

    # Проверяем, не выбрана ли тема лекции
    if text.startswith("Тема "):  # Все кнопки тем начинаются со слова "Тема"
        # Пока что просто ссылка-заглушка
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Вот ссылка на материалы"  # Потом заменишь на реальную ссылку или словарь
        )
        return
    # Если нажата кнопка "Информатика"
    if text == "Информатика":
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Выбери нужную кнопку:",
            attachments=[get_info_keyboard()]
        )
    elif text == "Я пропустил лекцию :(":
        # Показываем выбор тем
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Выбери лекцию, которую ты пропустил:",
            attachments=[get_topics_keyboard()]
        )
    elif text in ("Сдать ДЗ", "Какой у меня вариант?"):
        if text == "Сдать ДЗ":
            response = "Загрузи задание в раздел 'Домашнее задание' в личном кабинете."
        else:  # "Какой у меня вариант?"
            variant_number = random.randint(1, 10)
            response = f"Ваш вариант: {variant_number}"
        await bot.send_message(user_id=event.from_user.user_id, text=response)
    # Обработка кнопок "Да"/"Нет" из /test и любых других текстов
    else:
        await bot.send_message(user_id=event.from_user.user_id, text=f'Вы выбрали "{text}"')
    
async def main():
   await bot.delete_webhook()
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
