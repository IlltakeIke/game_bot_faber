import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    ContextTypes,
)
from states import MAINMENU, RATE
from bd import get_knb_rate, get_bnc_rate, get_cnz_rate, procent

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update – это полная информация о том, что произошло
    # update.effective_user - полная инфа о пользователе
    # update.effective_message - полная инфа о сообщении
    # update.effective_chat - полная инфа о диалоге
    # context.user_data['chislo'] = 1234
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Привет, {update.effective_user.username}!\n/knb - Камень ножницы бумага\n/bnc - быки и коровы\n/cnz - крестики нолики\n/rate - стата"
    )
    
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT id, name FROM users WHERE id = {update.effective_user.id}')
    user = cur.fetchone() # (24123421,'vova') | None
    if user is None:
        cur.execute(f'INSERT INTO users (id, name) VALUES({update.effective_user.id}, "{update.effective_user.username}")')
        conn.commit()
    conn.close()


    return MAINMENU

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton('Рейтинг KNB', callback_data='knb_data')
        ],
        [
            InlineKeyboardButton('Рейтинг BNC', callback_data='bnc_data')
        ],
        [
            InlineKeyboardButton('Рейтинг CNZ', callback_data='cnz_data')
        ]
        ]
    markup = InlineKeyboardMarkup(keyboard)
    knb_data = procent(update.effective_user.id)
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT cnz_all_hods, cnz_wins, bnc_record, bnc_wins FROM users WHERE id = {update.effective_user.id}')
    user = cur.fetchone()
    conn.commit()
    conn.close()
    cnz_data = user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"OWN stata: \n КНБ: \n Процент побед : {knb_data[0]} \n Кол-во побед : {knb_data[1]} \n Кол-во ничей : {knb_data[2]} \n Кол-во поражений : {knb_data[3]} \n \n БНК:\n Рекорд: {cnz_data[2]}\n Всего игр: {cnz_data[3]} \n \n КНЗ: \n Всего ходов: {cnz_data[0]} \n Всего игр: {cnz_data[1]}.",
        reply_markup=markup
    )
    return RATE

async def rate_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'knb_data':
        keyboard = [
        [
            InlineKeyboardButton('Рейтинг OWN', callback_data='own_data')
        ],
        [
            InlineKeyboardButton('Рейтинг BNC', callback_data='bnc_data')
        ],
        [
            InlineKeyboardButton('Рейтинг CNZ', callback_data='cnz_data')
        ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        rate = get_knb_rate()
        answer = 'Топ мира по К-Н-Б:\n'
        for n, person in enumerate(rate): 
            answer += f'{n+1}. {person[0]} — {person[1]}% \n'
        await query.edit_message_text(answer, reply_markup=markup)
    elif query.data == 'bnc_data':
        keyboard = [
        [
            InlineKeyboardButton('Рейтинг KNB', callback_data='knb_data')
        ],
        [
            InlineKeyboardButton('Рейтинг OWN', callback_data='own_data')
        ],
        [
            InlineKeyboardButton('Рейтинг CNZ', callback_data='cnz_data')
        ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        rate = get_bnc_rate()
        answer = 'Топ мира по Б-Н-К:\n'
        for n, person in enumerate(rate): 
            answer += f'{n+1}. {person[0]} — {person[1]} (попыток рекорд) || ({person[2]} игр) \n'
            if person[2] >= 3: 
                answer[:-2] += 'Достижение: Терпеливый'
            elif person[2] >= 5: 
               answer[:-2] += 'Достижение: Безумие'
        await query.edit_message_text(answer, reply_markup=markup)

    elif query.data == 'cnz_data':
        keyboard = [
        [
            InlineKeyboardButton('Рейтинг KNB', callback_data='knb_data')
        ],
        [
            InlineKeyboardButton('Рейтинг OWN', callback_data='own_data')
        ],
        [
            InlineKeyboardButton('Рейтинг BNC', callback_data='bnc_data')
        ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        rate = get_cnz_rate()
        answer = 'Топ мира по К-Н-Л:\n'
        for n, person in enumerate(rate): 
            answer += f'{n+1}. {person[0]} — {person[1]} ходов за жизнь. || ({person[2]} - игр) \n'
        await query.edit_message_text(answer, reply_markup=markup)
      
    elif query.data == 'own_data':
        keyboard = [
        [
            InlineKeyboardButton('Рейтинг KNB', callback_data='knb_data')
        ],
        [
            InlineKeyboardButton('Рейтинг BNC', callback_data='bnc_data')
        ],
        [
            InlineKeyboardButton('Рейтинг CNZ', callback_data='cnz_data')
        ],
        ]
        answer = 'OWN stata'
        
    markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text('КНБ', reply_markup=markup)

    return RATE
    