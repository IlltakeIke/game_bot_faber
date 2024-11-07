from telegram import Update, ReplyKeyboardMarkup
from bd import update_cnz

from telegram.ext import (
    ContextTypes,
    # ApplicationBuilder,
    # CommandHandler,
    # MessageHandler,
    # filters,
    # ConversationHandler,
)
from states import CNZ  # MAINMENU, KNB, BNC,
from start import start
from telegram.constants import ParseMode


def check_win_cnz(context: ContextTypes.DEFAULT_TYPE):
    ls = context.user_data["board"]

    if context.user_data["hod"] == 9:
        return "tie"

    elif ls[0] == ls[1] == ls[2]:
        return ls[0]
    elif ls[3] == ls[4] == ls[5]:
        return ls[3]
    elif ls[6] == ls[7] == ls[8]:
        return ls[6]

    elif ls[0] == ls[3] == ls[6]:
        return ls[6]
    elif ls[1] == ls[4] == ls[7]:
        return ls[1]
    elif ls[2] == ls[5] == ls[8]:
        return ls[2]

    elif ls[0] == ls[4] == ls[8]:
        return ls[4]
    elif ls[2] == ls[4] == ls[6]:
        return ls[6]
    else:
        return None


async def start_cnz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ты попал в игру крестики нолики. \n Ниже выбери клетку для хода.",
    )
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    context.user_data["board"] = board
    context.user_data["hod"] = 1

    keyboard = [
        context.user_data["board"][0:3],
        context.user_data["board"][3:6],
        context.user_data["board"][6:9],
    ]
    markup = ReplyKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=create_board(context),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )

    return CNZ


async def cnz_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = int(update.effective_message.text) - 1
    if message > 8 or message < 0:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Клетки №{message+1} не существует, напиши цифру от 1 до 9",
        )
        return CNZ

    if context.user_data["board"][message] in "OX":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="клетка занята"
        )
        return CNZ

    if context.user_data["hod"] % 2 == 0:
        context.user_data["board"][message] = "O"

    elif context.user_data["hod"] % 2 == 1:
        context.user_data["board"][message] = "X"

    keyboard = [
        context.user_data["board"][0:3],
        context.user_data["board"][3:6],
        context.user_data["board"][6:9],
    ]
    markup = ReplyKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=create_board(context),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    context.user_data["hod"] += 1
    
    is_win_or_tie = check_win_cnz(context)

    if is_win_or_tie == 'win':
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{is_win_or_tie} - победитель"
        )
        update_cnz('win',context.user_data["hod"], update.effective_chat.id)
        return await start(update, context)
    elif is_win_or_tie == "tie":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"{is_win_or_tie} - ничья"
        )
        update_cnz('win',context.user_data["hod"], update.effective_chat.id)
        return await start(update, context)
    return CNZ


def create_board(context: ContextTypes.DEFAULT_TYPE):
    global ls
    ls = context.user_data["board"]
    text = f"""`-------------
| {ls[0]} | {ls[1]} | {ls[2]} |
-------------
| {ls[3]} | {ls[4]} | {ls[5]} |
-------------
| {ls[6]} | {ls[7]} | {ls[8]} |
-------------`"""
    return text
