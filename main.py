import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    global s
    first_name = update.message.chat.first_name
    s = first_name
    await update.message.reply_html(
        rf"Привет! Я бот с которым можно пообщаться и что-то про себя узнать, познакомимся?")
    await update.message.reply_html(
        rf"Я могу называть тебя {s}?")
    reply_keyboard = [['/yes', '/no']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        rf"или нет?",
        reply_markup=markup
    )


async def yes(update, context):
    global s
    await update.message.reply_text(f"Круто, {s}")
    reply_keyboard = [['/talk', '/test'], ['/zodiac_sign']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        rf"Теперь выбери, чем м займемся!",
        reply_markup=markup
    )


async def no(update, context):
    global s
    await update.message.reply_text(f"Тогда напиши мне, пожалуйста, как к тебе обращаться?")
    s = 9124

async def echo(update, context):
    global s
    if s == 9124:
        s = update.message.text
        await update.message.reply_text(f"Хорошо, {s}")
        reply_keyboard = [['/talk', '/test'], ['/zodiac_sign']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            rf"Теперь выбери, чем мы займемся!",
            reply_markup=markup
        )

async def test(update, context):
    await update.message.reply_text(f"Супер, сейчас узнаем кто ты")

async def talk(update, context):
    await update.message.reply_text(f"Давай поболтаем!")

async def zodiak(update, context):
    await update.message.reply_text(f"Напиши дату своего рождения")
def main():
    application = Application.builder().token('6938421012:AAGo5bk_xi1fR0PoZpup93CSsu9KUEpxxeU').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("yes", yes))
    application.add_handler(CommandHandler("no", no))
    application.add_handler(CommandHandler("test", test))
    application.add_handler(CommandHandler("talk", talk))
    application.add_handler(CommandHandler("zodiac_sign", zodiak))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()

if __name__ == '__main__':
    main()