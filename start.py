import sqlite3
from telegram import Update#, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from states import MAINMENU

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
    
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT id, name FROM users WHERE id = {update.effective_user.id}')
    user = cur.fetchone() # (24123421,'vova') | None
    if user is None:
        cur.execute(f'INSERT INTO users VALUES({update.effective_user.id}, "{update.effective_user.username}", 0, 0, 1000, 0, 0)')
        conn.commit()
    conn.close()

    return MAINMENU


# быки и коровы для пользователей узнать рекорд

# команда /rate, которая одним сообщением будет выводить всю стату
# в нем 4 блока: его стата по всем играм, топ мира по кнб, топ мира по бнк, топ мира по кнл 

# сумарное количество ходов в кнл 

# придумать игру

# гит 