import sqlite3
import json
from functions import *

conn = sqlite3.connect("randombase.db")
cursor = conn.cursor()


def return_free_item(user_id: int):
    query = f"SELECT * FROM users WHERE user_id = {user_id} AND items_free > 0"

    cursor.execute(query)
    user = cursor.fetchall()

    if len(user) > 0:
        if len(open_bag(user_id)) < 10:

            i = return_gp()

            n = user[0][2]-1

            query = '''
            UPDATE users SET items_free = ? WHERE user_id = ?
            '''

            cursor.execute(query, (n, user_id))
            conn.commit()

            query = f"SELECT * FROM items WHERE id = {i}"
            
            cursor.execute(query)
            item = cursor.fetchone()[1]

            return item
        else:
            return -1
    else:
        return 0


def return_free_curiosity(user_id: int):
    query = f"SELECT * FROM users WHERE user_id = {user_id} AND curiosities_free > 0"

    cursor.execute(query)
    user = cursor.fetchall()

    if len(user) > 0:
        i = return_sp()

        n = user[0][3]-1

        query = '''
        UPDATE users SET curiosities_free = ? WHERE user_id = ?
        '''

        cursor.execute(query, (n, user_id))
        conn.commit()

        query = f"SELECT * FROM curiosities WHERE id = {i}"
    
        cursor.execute(query)
        curiosity = cursor.fetchone()[1]

        return curiosity
    else:
        return ''


def add_user(user_id, date):
    query = f"INSERT INTO users (user_id, date, items_free, curiosities_free, credits, bag) VALUES (?, ?, ?, ?, ?, ?)"

    cursor.execute(query, (int(user_id), date, 2, 2, 0, '[]'))

    cursor.commit()


def add_item(item_name, user_id):
    bag = open_bag(user_id)

    if len(bag) < 10:
        bag.append(item_name)
        bag_update = json.dumps(bag)

        query = '''
        UPDATE users SET bag = ? WHERE user_id = ?
        '''

        cursor.execute(query, (bag_update, user_id))

        cursor.commit()

        return True
    else:
        return False


def remove_item(item_id, user_id):
    bag = open_bag(user_id)

    if len(bag) > 0:

        try:
            item = bag[item_id]
            del bag[item_id-1]
        except:
            return 'Escolha um número válido para descartar.'
        
        bag_update = json.dumps(bag)

        query = '''
        UPDATE users SET bag = ? WHERE user_id = ?
        '''

        cursor.execute(query, (bag_update, user_id))

        cursor.commit()

        return f'**Você descartou com sucesso o item: {item}**'
    else:
        return 'Sua mochila está vazia! Utilize o comando **!item** para ganhar um item novo!'


def open_bag(user_id):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"

    cursor.execute(query)
    try:
        bag = json.loads(cursor.fetchone()[-1])
    except:
        bag = []

    return bag


def jackpot(user_id):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"

    cursor.execute(query)
    user = cursor.fetchone()

    credits = user[0][4]+100

    query = f"UPDATE users WHERE items_free = ? WHERE user_id = ?"

    cursor.execute(query, (user_id, credits))
    conn.commit()

    return True