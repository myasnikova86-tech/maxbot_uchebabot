import asyncio
import logging
import os

from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command, CallbackQuery
from maxapi.types import CallbackButton, ButtonsPayload, Attachment
from maxapi.enums.intent import Intent

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Переменная окружения TOKEN не задана!")
    exit(1)

bot = Bot(TOKEN)
dp = Dispatcher()

def get_hello_keyboard() -> Attachment:
    """Клавиатура с одной кнопкой 'Сказать Привет!'"""
    btn = CallbackButton(
        text="Сказать Привет!",
        payload="say_hello",
        intent=Intent.DEFAULT
    )
    return Attachment(type="inline_keyboard", payload=ButtonsPayload(buttons=[[btn]]))

@dp.message_created(Command('start'))
async def start_command(event: MessageCreated):
    await event.message.answer(
        "Привет! Нажми кнопку!",
        attachment=get_hello_keyboard()
    )

# --- ПРАВИЛЬНЫЙ ОБРАБОТЧИК ДЛЯ КНОПОК ---
# В maxapi callback-запросы приходят как отдельный тип события CallbackQuery
@dp.callback_query(lambda c: c.data == "say_hello")  # или просто @dp.callback_query()
async def handle_hello_button(callback: CallbackQuery):
    """Срабатывает при нажатии кнопки с payload 'say_hello'"""
    logging.info(f"Пользователь {callback.from_user.id} нажал кнопку")
    # Отвечаем на callback (закрывает "часики" на кнопке)
    await callback.answer("И тебе привет!")
    # Можно также отправить сообщение в чат:
    # await callback.message.answer("И тебе привет!")

async def main():
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
