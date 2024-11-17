import random
from bd import update_knb, procent
from telegram import Update, ReplyKeyboardMarkup

from telegram.ext import (
    ContextTypes,
)
from states import KNB


async def start_knb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #games = procent(update.effective_chat.id)
    keyboard = [["ножницы", "бумага", "камень"]]
    # print(context.user_data['chislo'])
    markup = ReplyKeyboardMarkup(keyboard)
    # if flag == 1: 
    #     text = 'Чтобы выбрать другую игру отправьте /start' 
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру камень ножницы бумага. \n Выбери кем ты будешь ходить на клавиатуре снизу. ", #+ text
        reply_markup=markup,
    )
    # if games % 5 == 0: 
    #     flag = 1
    #     return KNB, text
    return KNB

async def knb_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    various = ["ножницы", "бумага", "камень"]
    answer = random.choice(various)
    mes = update.effective_message.text.lower()

    if answer == "ножницы" and mes == "камень":
        ans = "Ты победил, показав камень"
        update_knb('win' ,update.effective_user.id)
    elif answer == "камень" and mes == "бумага":
        ans = "Ты победил, показав бумагу"
        update_knb('win' ,update.effective_user.id)
    elif answer == "бумага" and mes == "ножницы":
        ans = "Ты победил, показав ножницы"
        update_knb('win' ,update.effective_user.id)
    elif answer == mes:
        ans = f"Ничья, оба показали {answer}"
        update_knb('tie' ,update.effective_user.id)
    else:
        ans = f"Ты проиграл показав {mes}"
        update_knb('lose' ,update.effective_user.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"{mes} VS {answer}\n{ans}"
    )
    return await start_knb(update, context)
