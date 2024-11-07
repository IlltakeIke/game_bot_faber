import sqlite3

def create_table():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                                                id INTEGER PRIMARY KEY,
                                                name TEXT,
                                                cnz_wins INTEGER,
                                                cnz_ties INTEGER,
                                                bnc_record INTEGER,
                                                bnc_wins INTEGER,
                                                cnz_all_hods INTEGER
                                                    )''')
                                                    
    conn.commit()
    conn.close()


def update_knb(result, user_id):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    if result == 'win': 
        cur.execute(f'SELECT knb_wins FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET knb_wins = {user[0]+1} WHERE id = {user_id}')
    elif result == 'tie': 
        cur.execute(f'SELECT knb_ties FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET knb_ties = {user[0]+1} WHERE id = {user_id}')
    else: 
        cur.execute(f'SELECT cnz_losses FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET knb_losses = {user[0]+1} WHERE id = {user_id}')
    conn.commit()
    conn.close()

def update_bnc(result, efforts, user_id):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    if result == 'win': 
        cur.execute(f'SELECT wins FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET wins = {user[0]+1} WHERE id = {user_id}')
    
    cur.execute(f'SELECT bnc_record FROM users WHERE id = {user_id}')
    user = cur.fetchone() #в юзере картеж(0,)
    if user[0] > efforts:
        cur.execute(f'UPDATE users SET bnc_record = efforts WHERE id = {user_id}')
    conn.commit()
    conn.close()

def update_cnz(result, moves, user_id):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT cnz_all_hods FROM users WHERE id = {user_id}')
    user = cur.fetchone() #в юзере картеж(0,)
    cur.execute(f'UPDATE users SET cnz_all_hods = {user[0]+moves} WHERE id = {user_id}')
    if result == 'win': 
        cur.execute(f'SELECT cnz_wins FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET cnz_wins = {user[0]+1} WHERE id = {user_id}')
    elif result == 'tie': 
        cur.execute(f'SELECT cnz_ties FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET cnz_ties = {user[0]+1} WHERE id = {user_id}')
    conn.commit()
    conn.close()

