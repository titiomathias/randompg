from random import randint
from datetime import datetime
import json

# Return random item
def return_gp():
    gp = randint(1, 1001)

    with open('d1000.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = lines[gp].strip("\n")
        file.close()
    return item


# Return random curiosity (still in development)
def return_sp():
    sp = randint(1, 100)

    with open('d100.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        curiosity = lines[sp].strip("\n")
        file.close()
    return curiosity


# Still in development
def check_limit(user_id, command_name):
    today = datetime.now().date()

    users = json.load(open('limits.json', 'r', encoding='utf-8'))

    if user_id not in users:
        users[user_id] = {
            "date": today,
            "counts": {
                "items": 0,
                "curiosities": 0
            },
            "items": [],
            "curiosities": []
        }

    print(users[user_id])


check_limit("user1", "item")