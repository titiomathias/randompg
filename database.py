import sqlite3
import json

conn = sqlite3.connect("randombase.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    date TEXT,
    items_free INTEGER,
    curiosities_free INTEGER,
    credits INTEGER,
    bag TEXT
)
'''
)

cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
'''
)

cursor.execute('''
CREATE TABLE IF NOT EXISTS curiosities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
'''
)

cursor.execute('''
CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    user_id INTEGER,
    item TEXT,
    purpose TEXT,
    user_id_request INTEGER,
    result TEXT,
    status INTEGER
)
'''
)

with open('d1000.csv', 'r', encoding='utf-8') as file:
    lines = [line.strip() for line in file]

with open('d100.csv', 'r', encoding='utf-8') as file:
    curiosities = [line.strip() for line in file]

for l in lines:
    cursor.execute('''
    INSERT INTO items (name) VALUES (?)
    ''', (l,))

for c in curiosities:
    cursor.execute('''
    INSERT INTO curiosities (content) VALUES (?)
    ''', (c,))

with open('limits.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)
    file.close()

for user_id, info in dados.items():
    date = info['date']
    items_free = info["counts"]["items"]
    curiosities_free = info["counts"]["curiosities"]
    try:
        credits = info["counts"]["items_vip"]
    except:
        credits = 0
    bag = json.dumps(info["bag"], ensure_ascii=False)

    cursor.execute('''
    INSERT INTO users (user_id, date, items_free, curiosities_free, credits, bag) VALUES (?, ?, ?, ?, ?, ?)
    ''', (int(user_id), date, items_free, curiosities_free, credits, bag))



conn.commit()


conn.close()