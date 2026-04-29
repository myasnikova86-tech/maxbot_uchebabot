import asyncio
import logging
import os
from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command, BotStarted, CallbackButton, ButtonsPayload, Attachment
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
    await event.message.answer("Обработка команды start")

@dp.message_created(Command('test'))
async def test_message(event: MessageCreated):
    # Создаём кнопки через CallbackButton
    btn_yes = CallbackButton(text="Да", payload="yes")
    btn_no = CallbackButton(text="Нет", payload="no")
    keyboard = ButtonsPayload(buttons=[[btn_yes, btn_no]])
    attachment = Attachment(type="inline_keyboard", payload=keyboard)
    
    await event.message.answer(
        "Текстовое сообщение с кнопками",
        attachment=attachment
    )

# Обработчик нажатий на кнопки
@dp.message_created()
async def handle_callbacks(event: MessageCreated):
    # Проверяем, есть ли callback у сообщения
    callback = getattr(event.message, 'callback', None)
    if callback and callback.data in ("yes", "no"):
        text = "Да" if callback.data == "yes" else "Нет"
        await event.message.answer(f'Вы выбрали "{text}"')
    # Если это обычное текстовое сообщение (не команда и не кнопка)
    elif event.message.body and not event.message.body.startswith('/'):
        # Дополнительная логика для любых текстовых сообщений
        await event.message.answer(f'Вы написали: "{event.message.body}"')

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
