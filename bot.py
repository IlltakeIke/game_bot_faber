import logging
import random
from telegram import Update, ReplyKeyboardMarkup 
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

MAINMENU, KNB, BNC, CNZ = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update – это полная информация о том, что произошло
    # update.effective_user - полная инфа о пользователе
    # update.effective_message - полная инфа о сообщении
    # update.effective_chat - полная инфа о диалоге
    # context.user_data['chislo'] = 1234
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.username}!\n/knb - Камень ножницы бумага\n/bnc - быки и коровы\n/cnz - крестики нолики"
    )
    return MAINMENU


async def start_knb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["ножницы", "бумага", "камень"]]
    # print(context.user_data['chislo'])
    markup = ReplyKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру камень ножницы бумага. \n Выбери кем ты будешь ходить на клавиатуре снизу.", reply_markup=markup
    )
    return KNB

async def start_bnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру быки и коровы. Попробуй ниже угадать 4-х значное число"
    )

    return BNC

async def knb_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    various = ["ножницы", "бумага", "камень"]   
    answer = random.choice(various)
    mes = update.effective_message.text.lower()

    if answer == "ножницы" and mes == "камень":
        ans = "Ты победил, показав камень"
    elif answer == "камень" and mes == "бумага":
        ans = "Ты победил, показав бумагу"
    elif answer == "бумага" and mes == "ножницы":
        ans = "Ты победил, показав ножницы"
    elif answer == mes:
        ans = f"Ничья, оба показали {answer}"
    else:
        ans = f"Ты проиграл показав {mes}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"{mes} VS {answer}\n{ans}"
    )
    return await start_knb(update, context)

async def bnc_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import random
    def guess_number():
        rand = random.randint(1000,9999)
        result = check_num(rand)
        if not result:
            return guess_number()
        else: 
            return result

    def check_num(num):
        num = str(num)
        for i in range(len(num)-1):
            for j in range(i+1,len(num)):
                if num[i] == num[j]:
                    return None
        return list(map(int, num))

    def take_input():
        num = int(input("Введите число "))
        result = check_num(num)
        if not result:
            return take_input()
        else:
            return  result
        
    def count_bulls_and_cows(g_sp, u_sp):
        b = 0
        c = 0
        for i in range(len(g_sp)):
            if g_sp[i] == u_sp[i]:
                b += 1

        for i in range(len(g_sp)):
            for j in range(len(u_sp)):
                if g_sp[i] == u_sp[j]:
                    c += 1
                
        c = c - b
        return c, b
    
    guess = guess_number()
    b = 0
    while b != 4: 
        user = take_input()
        c, b = count_bulls_and_cows(guess,user)
        print(f'Коров: {c}\n Быков: {b}')

    print("Victory")



async def start_cnz(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await context.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру крестики нолики. \n Ниже выбери клетку для хода.",
    )
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    context.user_data['board'] = board

    return CNZ

def create_board(context: ContextTypes.DEFAULT_TYPE):
    ls = context.user_data['board']
    text=f"""-------------
| {ls[0]} | {ls[1]} | {ls[2]} |
-------------
| {ls[3]} | {ls[4]} | {ls[5]} |
-------------
| {ls[6]} | {ls[7]} | {ls[8]} |
-------------"""
    return text


async def cnz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=create_board(context)
    )   
    return CNZ
        



if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token("7940846926:AAGBjqcxvR2xlEzINHTduFGmVJv98wvY3vE")
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states = {
            MAINMENU: [CommandHandler("knb", start_knb), CommandHandler("bnc", start_bnc), CommandHandler("cnz", start_cnz)],  
            KNB: [MessageHandler(filters.TEXT & ~filters.COMMAND, knb_game)],
            BNC: [MessageHandler(filters.TEXT & ~filters.COMMAND, bnc_game)],
            CNZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, cnz_game)]
        },
        fallbacks= [CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)

    application.run_polling()
