import asyncio
import logging
import os
from maxapi import Bot, Dispatcher, F
from maxapi.types import MessageButton, MessageCreated, Command, BotStarted
from maxapi.types import ButtonsPayload, Attachment
from maxapi.types import LinkButton, MessageCallback, CallbackButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder
from maxapi.enums.intent import Intent

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Переменная окружения TOKEN не задана!")
    exit(1)

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.bot_started()
async def bot_started(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='Ты начал диалог с ботом'
    )

@dp.message_created(Command('start'))
async def start_message(event: MessageCreated):
    await event.message.answer(f "Обработка команды start")

@dp.message_created(Command('id'))
async def hello(event: MessageCreated):
    await event.message.answer(f'''Привет, {event.from_user.first_name}!
Твой ID в мессенджере: {event.from_user.user_id}''')

@dp.message_created(Command('test'))
async def test_message(event: MessageCreated):
    reply_kb = InlineKeyboardBuilder()
    reply_kb.row(MessageButton(text='Да'), MessageButton(text='Нет'))
    await bot.send_message(chat_id=event.from_chat.chat_id, text='Текстовое сообщение с кнопками',
                       attachments=[reply_kb.as_markup()])

@dp.message_created(F.message.body.text)
async def text_handler(event: MessageCreated):
    await bot.send_mesage(user_id=event.from_chat.chat_id, text = f 'Вы выбрали "{event.message.body.text}" ' 
    )
async def main():
   await bot.delete_webhook()
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
