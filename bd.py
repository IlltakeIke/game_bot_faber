import sqlite3

def create_table():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                                                id INTEGER PRIMARY KEY,
                                                name TEXT,
                                                knb_wins INTEGER DEFAULT 0, 
                                                knb_ties INTEGER DEFAULT 0, 
                                                knb_losses INTEGER DEFAULT 0,
                                                knb_wprocent INTEGER DEFAULT 0,  
                                                cnz_wins INTEGER DEFAULT 0,
                                                cnz_ties INTEGER DEFAULT 0,
                                                cnz_all_hods INTEGER DEFAULT 0,
                                                bnc_record INTEGER DEFAULT 1000,
                                                bnc_wins INTEGER DEFAULT 0
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
        cur.execute(f'SELECT knb_losses FROM users WHERE id = {user_id}')
        user = cur.fetchone() #в юзере картеж(0,)
        cur.execute(f'UPDATE users SET knb_losses = {user[0]+1} WHERE id = {user_id}')
    conn.commit()
    conn.close()

def procent(user_id):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT knb_wins, knb_ties, knb_ties FROM users WHERE id = {user_id}')
    user = cur.fetchone() #в юзере картеж(0,)
    all_games = user[0] + user[1] + user[2]
    wprocent = user[0] / all_games * 100  
    conn.commit()
    conn.close()
    return [wprocent, user[0], user[1], user[2]]


def get_knb_rate():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute('SELECT name, knb_wins, knb_ties, knb_ties FROM users')
    users = cur.fetchall()
    wins_procent = []
    for user in users:
        all_games = user[1] + user[2] + user[3]
        wprocent = user[1] / all_games * 100
        wins_procent.append([user[0], wprocent])
    wins_procent.sort(key=lambda x: x[1], reverse=True)
    return wins_procent[:10]

def get_bnc_rate():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute('SELECT name, bnc_wins, bnc_record FROM users')
    users = cur.fetchall()
    bnc_top = []
    bnc_plays = []
    for user in users:
        bnc_top.append([user[0], user[2]])
        bnc_plays.append([user[0], user[1]])
    bnc_top(key=lambda x: x[1], reverse=True)
    bnc_plays(key=lambda x: x[1], reverse=True)        
    return bnc_top[:10], bnc_plays[:10]

def get_cnz_rate():
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute('SELECT name, cnz_all_hods, cnz_wins, cnz_ties FROM users')
    users = cur.fetchall()
    hod_top = []
    all_games = []
    for user in users:
        hod_top.append([user[0], user[1]])
        all_games.append([user[2] + user[3]])
    hod_top.sort(key=lambda x: x[1], reverse=True)
    all_games.sort(key=lambda x: x[0], reverse=True)
    return hod_top[:10], all_games[:10]

def update_bnc(result, efforts, user_id):
    conn = sqlite3.connect("game_bot.db")
    cur = conn.cursor()
    cur.execute(f'SELECT bnc_wins, bnc_record FROM users WHERE id = {user_id}')
    user = cur.fetchone() #в юзере картеж(0,)
    cur.execute(f'UPDATE users SET bnc_wins = {user[0]+1} WHERE id = {user_id}')
    if user[1] > efforts:
        cur.execute(f'UPDATE users SET bnc_record = {efforts} WHERE id = {user_id}')
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
