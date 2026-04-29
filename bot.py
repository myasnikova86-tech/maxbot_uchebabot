import os
import logging
import aiomax

# --- НАСТРОЙКА ЛОГГИРОВАНИЯ И ТОКЕНА ---
logging.basicConfig(level=logging.INFO)

# Переменная TOKEN должна быть задана в окружении (например, в настройках Bothost)
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.error("❌ Ошибка: переменная окружения TOKEN не найдена!")
    exit(1)

# Создаём экземпляр бота с включённой поддержкой Markdown-разметки
bot = aiomax.Bot(TOKEN, default_format="markdown")

# --- СОЗДАНИЕ КЛАВИАТУРЫ С ОДНОЙ КНОПКОЙ ---
# Создаём строителя клавиатуры
kb = aiomax.buttons.KeyboardBuilder()
# Добавляем одну кнопку. 'Сказать Привет!' — это видимый текст на кнопке,
# а 'say_hello' — её идентификатор (callback_data), по которому мы поймём, что нажали именно её.
button = aiomax.buttons.CallbackButton('Сказать Привет!', 'say_hello')
kb.add(button)

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
# Когда пользователь отправляет команду /start
@bot.on_command('start')
async def start_command(ctx: aiomax.CommandContext):
    await ctx.reply(
        "Привет! Нажми кнопку!",
        keyboard=kb  # Прикрепляем клавиатуру к сообщению
    )

# --- ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ ---
# Когда пользователь нажимает на любую inline-кнопку, проверяем её идентификатор
@bot.on_button_callback('say_hello')  # Сработает только для кнопки с id 'say_hello'
async def on_say_hello_callback(callback: aiomax.Callback):
    # Отвечаем в тот же чат, откуда пришло нажатие
    await callback.answer("И тебе привет!")

# --- (НЕОБЯЗАТЕЛЬНО) ПРИВЕТСТВИЕ ПРИ ПЕРВОМ ЗАПУСКЕ БОТА ---
# Этот блок сработает, когда пользователь явно нажмёт "Начать" в интерфейсе мессенджера
@bot.on_bot_start()
async def bot_started(pd: aiomax.BotStartPayload):
    await pd.send("Привет! Напиши мне /start", keyboard=kb)

# --- ЗАПУСК БОТА ---
if __name__ == "__main__":
    logging.info("🚀 Бот запускается...")
    bot.run()
