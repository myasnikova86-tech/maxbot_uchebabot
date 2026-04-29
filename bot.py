import asyncio
import logging
import os

from maxapi import Bot, Dispatcher
from maxapi.types import MessageCreated, Command
from maxapi import InlineKeyboardBuilder

# Настройка логирования для отслеживания работы в логах Bothost
logging.basicConfig(level=logging.INFO)

# --- БЕЗОПАСНОЕ ПОЛУЧЕНИЕ ТОКЕНА ИЗ ОКРУЖЕНИЯ (ОБЯЗАТЕЛЬНОЕ УСЛОВИЕ) ---
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.critical("Критическая ошибка: переменная окружения 'TOKEN' не найдена.")
    exit("Не удалось запустить бота. Проверьте настройки окружения на Bothost.")
# ---

# Инициализация бота и диспетчера
bot = Bot(TOKEN)
dp = Dispatcher()

# Формируем клавиатуру с кнопкой "Сказать Привет!"
# Библиотека maxapi использует Inline клавиатуры для callback-кнопок.
keyboard_builder = InlineKeyboardBuilder()
button_say_hello = keyboard_builder.button(
    text='Сказать Привет!',
    callback_data='say_hello' # Идентификатор для обработчика
)
keyboard_builder.add(button_say_hello)

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@dp.message_created(Command('start'))
async def handle_start_command(event: MessageCreated):
    """
    Отправляет приветственное сообщение и показывает кнопку.
    """
    logging.info(f"Пользователь {event.message.chat_id} отправил команду /start.")
    await event.message.answer(
        "Привет! Нажми кнопку!",
        inline_keyboard=keyboard_builder.as_markup()  # Прикрепляем клавиатуру к сообщению
    )

# --- ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ "Сказать Привет!" ---
@dp.message_created(F.callback.data == 'say_hello')
async def handle_say_hello_callback(event: MessageCreated):
    """
    Этот обработчик сработает, когда MAX пришлет сообщение о callback-запросе
    от кнопки с `callback_data='say_hello'`.
    """
    logging.info(f"Пользователь {event.message.chat_id} нажал кнопку 'Сказать Привет!'.")
    # `event.message.answer` отправит ответное сообщение в тот же чат
    await event.message.answer("И тебе привет!")

# --- ТОЧКА ЗАПУСКА БОТА (САМАЯ ВАЖНАЯ ЧАСТЬ) ---
async def main():
    """
    Главная асинхронная функция, которая запускает long polling бота.
    """
    logging.info("Бот начинает работу...")
    # Очистка вебхуков - важный шаг для стабильной работы через polling
    await bot.delete_webhook()
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Запускаем асинхронную main-функцию
    asyncio.run(main())
