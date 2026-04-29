import os
import logging
import aiomax

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logging.error("Переменная окружения TOKEN не найдена!")
    exit(1)

bot = aiomax.Bot(TOKEN)

@bot.on_command('start')
async def start_command(ctx: aiomax.CommandContext):
    kb = aiomax.buttons.KeyboardBuilder()
    btn = aiomax.buttons.CallbackButton('Сказать Привет!', 'say_hello')
    kb.add(btn)
    await ctx.reply("Привет! Нажми кнопку!", keyboard=kb)

@bot.on_button_callback(lambda data: data.payload == 'say_hello')
async def say_hello_callback(cb: aiomax.Callback):
    await cb.answer("И тебе привет!")

if __name__ == '__main__':
    bot.run()
