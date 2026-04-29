import asyncio
import logging
import os

from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command
from maxapi.types import CallbackButton, ButtonsPayload, Attachment
from maxapi.enums.intent import Intent

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# --- Получение токена из переменной окружения ---
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Переменная окружения TOKEN не задана!")
    exit(1)

# Инициализация бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher()

# --- Функция, создающая клавиатуру с одной кнопкой "Сказать Привет!" ---
def get_hello_keyboard() -> Attachment:
    """Возвращает Attachment с inline-кнопкой 'Сказать Привет!'."""
    # Создаём кнопку с payload 'say_hello'
    btn_hello = CallbackButton(
        text="Сказать Привет!",
        payload="say_hello",
        intent=Intent.DEFAULT    # обычный интент, можно и DEFAULT
    )
    # Группируем: один ряд, одна кнопка
    buttons_payload = ButtonsPayload(buttons=[[btn_hello]])
    # Возвращаем Attachment типа inline_keyboard
    return Attachment(type="inline_keyboard", payload=buttons_payload)

# --- Обработчик команды /start ---
@dp.message_created(Command('start'))
async def start_command(event: MessageCreated):
    """Отправляет приветствие и клавиатуру с одной кнопкой."""
    logging.info(f"Пользователь {event.message.chat_id} отправил /start")
    keyboard = get_hello_keyboard()
    await event.message.answer(
        "Привет! Нажми кнопку!",
        attachment=keyboard      # прикрепляем клавиатуру
    )

# --- Обработчик нажатия на кнопку (по payload) ---
@dp.message_created(lambda msg: msg.callback is not None and msg.callback.payload == "say_hello")
async def hello_button_callback(event: MessageCreated):
    """
    Срабатывает, когда пользователь нажимает на кнопку с payload 'say_hello'.
    """
    logging.info(f"Пользователь {event.message.chat_id} нажал кнопку 'Сказать Привет!'")
    # Отвечаем в тот же чат
    await event.message.answer("И тебе привет!")

# --- Запуск бота ---
async def main():
    logging.info("Запуск бота (polling)...")
    await bot.delete_webhook()   # очищаем вебхук на всякий случай
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
