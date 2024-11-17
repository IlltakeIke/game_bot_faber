import random
from telegram import Update#, ReplyKeyboardMarkup
from bd import update_bnc

from telegram.ext import (
    ContextTypes,
    # ApplicationBuilder,
    # CommandHandler,
    # MessageHandler,
    # filters,
    # ConversationHandler,
)
from states import BNC 
from start import start 


def guess_number() -> list[int]:
    """Эта функция возвращает список с цифрами загаданного числа"""
    rand = random.randint(1000, 9999)
    result = check_num(rand)
    if not result:
        return guess_number()
    else:
        print(result)
        return result

def check_num(num):
    num = str(num)
    for i in range(len(num) - 1):
        for j in range(i + 1, len(num)):
            if num[i] == num[j]:
                return None
    return list(map(int, num))

def take_input():
    num = int(input("Введите число "))
    result = check_num(num)
    if not result:
        return take_input()
    else:
        return result

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


async def start_bnc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру быки и коровы. Попробуй ниже угадать 4-х значное число \n(Быки - угаданная цифра и её место)\n(Корова - угаданная цифра, но не на своем месте) ",
    )
    result = guess_number()
    context.user_data["gsp"] = result
    return BNC


async def bnc_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.effective_message.text
    result = check_num(answer)
    efforts = 0
    if not result:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="wrong")
        return BNC
    c, b = count_bulls_and_cows(context.user_data["gsp"], result)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"cows = {c} and bulls = {b}"
    )
    efforts += 1
    if b == 4:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.effective_user.first_name}, you won!",
        )
        update_bnc('win', efforts, update.effective_chat.id)
        return await start(update, context)