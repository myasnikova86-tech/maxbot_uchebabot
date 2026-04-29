import asyncio
import logging
import os
from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command, BotStarted, CallbackQuery
from maxapi.types import CallbackButton, ButtonsPayload, Attachment
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
    await event.message.answer(f"Обработка команды start")

async def main():
   await bot.delete_webhook()
   await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
