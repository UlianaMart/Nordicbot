import logging
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
ri = {}
riri = {}


def zd_check(date):
    day, month, year = map(int, date.split('.'))

    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"



async def start(update, context):
    user_id = update.message.from_user.id
    ri[user_id] = update.message.chat.first_name
    await update.message.reply_html(
        rf"Привет! Я бот с которым можно пообщаться и что-то про себя узнать, познакомимся?")
    await update.message.reply_html(
        rf"Я могу называть тебя {ri[user_id]}?")
    reply_keyboard = [['/yes', '/no']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        rf"или нет?",
        reply_markup=markup
    )


async def yes(update, context):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Круто, {ri[user_id]}")
    reply_keyboard = [['/zodiac_sign', '/test']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        rf"Теперь выбери, чем м займемся!",
        reply_markup=markup
    )


def check_answer(ans):
    return ans.lower().strip()  in ["да", "нет"]


async def no(update, context):
    await update.message.reply_text(f"Тогда напиши мне, пожалуйста, как к тебе обращаться?")


async def echo(update, context):
    s = update.message.text
    await update.message.reply_text(f"Хорошо, {s}")
    reply_keyboard = [['/zodiac_sign', '/test']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        rf"Теперь выбери, чем мы займемся!",
        reply_markup=markup
    )


async def zodiac_1(update, context):
    await update.message.reply_text(
        "Чтобы получить свой знак зодиака введи свою дату рождения в формате ДД.ММ.ГГГГ")
    return 1


async def zodiac_2(update, context):
    try:
        zs = zd_check(update.message.text)
        await update.message.reply_text(zs)
        return ConversationHandler.END
    except Exception:
        await update.message.reply_text("Вы ввели дату неправильно. Попробуйте снова. Или /stop для выхода")
        return 1


async def teststart(update, context):
    uid = update.message.from_user.id
    global riri
    if uid not in riri:
        riri[uid] = 0

    await update.message.reply_text(
        "Супер, сейчас узнаем кто ты \n"
        "Ты можете прервать тест, послав команду /stop \n"
        "Отвечай на вопросы да или нет \n"
        "1. Часто ли Вы испытываете тягу к новым впечатлениям, к тому чтобы отвлечься, испытать сильные ощущения?")
    return 1


async def a_response(update, context):
    print('hi')
    context.user_data[0] = update.message.text

    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 1
    await update.message.reply_text(
        f"2. Нравится ли вам работа, требующая быстрого действия?")
    return 2


async def b_response(update, context):
    context.user_data[1] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 2
    await update.message.reply_text(
        f"3. Обдумываете ли вы свои дела не спеша и предпочитаете подождать, прежде чем действовать?")
    return 3


async def c_response(update, context):
    context.user_data[2] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 3
    await update.message.reply_text(
        f"4. Считаете ли вы себя беззаботным человеком?")
    return 4


async def d_response(update, context):
    context.user_data[3] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 4
    await update.message.reply_text(
        f"5. Предпочитаете ли вы чтение книг встречам с людьми?")
    return 5


async def e_response(update, context):
    context.user_data[4] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 5
    await update.message.reply_text(
        f"6. Стараетесь ли вы ограничить круг своих знакомств небольшим числом самых близких людей?")
    return 6


async def f_response(update, context):
    context.user_data[5] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 6
    await update.message.reply_text(
        f"7. Любите ли вы часто бывать в компании?")
    return 7


async def g_response(update, context):
    context.user_data[6] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 7
    await update.message.reply_text(
        f"8. Любите ли вы часто бывать в компании?")
    return 8


async def h_response(update, context):
    context.user_data[7] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 8
    await update.message.reply_text(
        f"9. Чувствуете ли вы себя неспокойно, находясь в большой компании?")
    return 9


async def i_response(update, context):
    context.user_data[8] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 9
    await update.message.reply_text(
        f"10. Сумели бы вы внести оживление в скучную компанию?")
    return 10


async def j_response(update, context):
    context.user_data[9] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 10
    await update.message.reply_text(
        f"11. Могли бы вы сказать, что вы уверенный в себе человек?")
    return 11


async def k_response(update, context):
    context.user_data[10] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 11
    await update.message.reply_text(
        f"12. Что вы предпочитаете, если хотите что-либо узнать: найти это в книге или спросить у друзей?")
    return 12


async def m_response(update, context):
    context.user_data[11] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 12
    await update.message.reply_text(
        f"13. Огорчились бы вы, если бы не смогли долго видеться с друзьями?")
    return 13


async def n_response(update, context):
    context.user_data[12] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 13
    await update.message.reply_text(
        f"14. Верно ли что вы так любите поговорить, что не упускаете любого удобного случая побеседовать с новым человеком?")
    return 14


async def o_response(update, context):
    context.user_data[13] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 14
    await update.message.reply_text(
        f"15. Нравится ли вам работа, требующая сосредоточения?")
    return 15


async def p_response(update, context):
    context.user_data[14] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 15
    await update.message.reply_text(
        f"16. Слывете ли вы за человека веселого и живого?")
    return 16


async def q_response(update, context):
    context.user_data[15] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 16
    await update.message.reply_text(
        f"17. Способны ли вы иногда дать волю своим чувств и беззаботно развлечься с веселой компанией?")
    return 17


async def r_response(update, context):
    context.user_data[16] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 17
    await update.message.reply_text(
        f"18. Когда на вас кричат, отвечаете ли тем же?")
    return 18


async def s_response(update, context):
    context.user_data[17] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 18
    await update.message.reply_text(
        f"19. Бывает ли вам неприятно находиться в компании, где все подшучивают друг над другом?")
    return 19


async def t_response(update, context):
    context.user_data[18] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 19
    await update.message.reply_text(
        f"20. Часто ли действуете необдуманно, под влиянием момента?")
    return 20


async def v_response(update, context):
    context.user_data[19] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 20
    await update.message.reply_text(
        f"21. Верно ли, что вы неторопливы в движениях и несколько медлительны?")
    return 21


async def w_response(update, context):
    context.user_data[20] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 21
    await update.message.reply_text(
        f"22. Верно ли, что 'на спор' вы способны решиться на все?")
    return 22


async def x_response(update, context):
    context.user_data[21] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 22
    await update.message.reply_text(
        f"23. Трудно ли вам получить настоящее удовольствие от мероприятий, в которых участвует много народу?")
    return 23


async def y_response(update, context):
    context.user_data[22] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 23
    await update.message.reply_text(
        f"24. Быстро ли вы обычно действуете и говорите, не затрачиваете ли много времени на обдумывание?")
    return 24


async def se_response(update, context):
    context.user_data[23] = update.message.text
    uid = update.message.from_user.id
    ans = update.message.text
    if check_answer(ans):
        if ans.lower() == "да":
            riri[uid] += 1
    else:
        await update.message.reply_text("я вас не понимаю")
        return 24
    await update.message.reply_text("Считаю результат")
    await update.message.reply_text(f"Вы {'интроверт' if riri[uid] <= 12 else 'экстроверт'}. Ваши баллы: {riri[uid]}")
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


def main():
    application = Application.builder().token('6938421012:AAGo5bk_xi1fR0PoZpup93CSsu9KUEpxxeU').build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('test', teststart)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, a_response)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, b_response)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, c_response)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, d_response)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, e_response)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_response)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, g_response)],
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, h_response)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, i_response)],
            10: [MessageHandler(filters.TEXT & ~filters.COMMAND, j_response)],
            11: [MessageHandler(filters.TEXT & ~filters.COMMAND, k_response)],
            12: [MessageHandler(filters.TEXT & ~filters.COMMAND, m_response)],
            13: [MessageHandler(filters.TEXT & ~filters.COMMAND, n_response)],
            14: [MessageHandler(filters.TEXT & ~filters.COMMAND, o_response)],
            15: [MessageHandler(filters.TEXT & ~filters.COMMAND, p_response)],
            16: [MessageHandler(filters.TEXT & ~filters.COMMAND, q_response)],
            17: [MessageHandler(filters.TEXT & ~filters.COMMAND, r_response)],
            18: [MessageHandler(filters.TEXT & ~filters.COMMAND, s_response)],
            19: [MessageHandler(filters.TEXT & ~filters.COMMAND, t_response)],
            20: [MessageHandler(filters.TEXT & ~filters.COMMAND, v_response)],
            21: [MessageHandler(filters.TEXT & ~filters.COMMAND, w_response)],
            22: [MessageHandler(filters.TEXT & ~filters.COMMAND, x_response)],
            23: [MessageHandler(filters.TEXT & ~filters.COMMAND, y_response)],
            24: [MessageHandler(filters.TEXT & ~filters.COMMAND, se_response)]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )
    cv2 = ConversationHandler(
        entry_points=[CommandHandler("zodiac_sign", zodiac_1)],
        states={
            1:[MessageHandler(filters.TEXT & ~filters.COMMAND, zodiac_2)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(cv2)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("yes", yes))
    application.add_handler(CommandHandler("no", no))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == '__main__':
    main()
