from random import randint
from datetime import datetime
import json

# Return random item
def return_gp():
    gp = randint(1, 1000)

    with open('d1000.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = lines[gp].strip("\n")
        file.close()
    return item


# Return random curiosity
def return_sp():
    sp = randint(1, 100)

    with open('d100.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        curiosity = lines[sp].strip("\n")
        file.close()
    return curiosity
            

def swap_items(user_id_1: str, item1: int, user_id_2: str, item2: int):
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    item_1 = users[user_id_1]["bag"][item1]

    users[user_id_1]["bag"][item1] = users[user_id_2]["bag"][item2]
    users[user_id_2]["bag"][item2] = item_1

    with open('limits.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)
        file.close()

    return True
