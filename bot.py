import asyncio
import logging
import os
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
    
    # Если нажата кнопка "Информатика"
    if text == "Информатика":
        # Отправляем новое сообщение с тремя кнопками
        await bot.send_message(
            user_id=event.from_user.user_id,
            text="Выбери нужную кнопку:",
            attachments=[get_info_keyboard()]
        )
    # Если нажата одна из новых кнопок (Информатика)
    elif text in ("Я пропустил лекцию :(", "Сдать ДЗ", "Какой у меня вариант?"):
        if text == "Я пропустил лекцию :(":
            response = "Обратись к одногруппникам за конспектом 😢"
        elif text == "Сдать ДЗ":
            response = "Загрузи задание в раздел 'Домашнее задание' в личном кабинете."
        else:  # "Какой у меня вариант?"
            response = "Твой вариант указан в файле 'Варианты' в общем чате."
        await bot.send_message(user_id=event.from_user.user_id, text=response)
    # Обработка кнопок "Да"/"Нет" из /test и любых других текстов
    else:
        await bot.send_message(user_id=event.from_user.user_id, text=f'Вы выбрали "{text}"')
    
async def main():
   await bot.delete_webhook()
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
