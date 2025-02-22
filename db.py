import sqlite3
import json

conn = sqlite3.connect("database/randombase.db")

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    date TEXT,
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

cursor.execute('''
CREATE TABLE IF NOT EXISTS sell_buy (
    id TEXT PRIMARY KEY,
    date TEXT,
    type INTEGER,
    user_id INTEGER,
    item TEXT,
    value FLOAT,
    user_id_request INTEGER,
    result TEXT,
    status INTEGER
)
'''
)

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    target TEXT,
    number INTEGER,
    function TEXT
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
    curiosities_free = 2
    try:
        credits = info["counts"]["items_vip"]
    except:
        credits = 5
    bag = {
        "items": info["bag"],
        "slots": 10
    }
    bag = json.dumps(bag, ensure_ascii=False)

    cursor.execute('''
    INSERT INTO users (user_id, date, curiosities_free, credits, bag) VALUES (?, ?, ?, ?, ?)
    ''', (int(user_id), date, curiosities_free, credits, bag))



conn.commit()

conn.close()