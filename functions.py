from random import randint
from datetime import datetime
import json

# Return random item
def return_gp():
    gp = randint(0, 999)

    with open('d1000.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        item = lines[gp].strip("\n")
        file.close()
    return item


# Return random curiosity
def return_sp():
    sp = randint(0, 99)

    with open('d100.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        curiosity = lines[sp].strip("\n")
        file.close()
    return curiosity


# Add item to user's bag
def add_item(user_id, item):
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    if user_id in users:
        users[user_id]["bag"].append(item)

        with open('limits.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4, ensure_ascii=False)
            file.close()

        return True
    else:
        return False

# Define limits for users
def check_limit(user_id, command_name):
    today = datetime.now().strftime("%d/%m/%Y")

    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
        
        for user in users:
            if users[user]["date"] != today:
                users[user]["date"] = today
                users[user]["counts"]["items"] = 0
                users[user]["counts"]["curiosities"] = 0
            else:
                continue
    except Exception as e:
        print(e)

    if user_id not in users:

        users[user_id] = {
            "date": today,
            "counts": {
                "items": 0,
                "curiosities": 0
            },
            "bag": []
        }

        users[user_id]["counts"][command_name] += 1

        with open('limits.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4, ensure_ascii=False)
            file.close()

        return 1
    else:
        if users[user_id]["counts"][command_name] < 2:

            if command_name == "items":
                if len(users[user_id]["bag"]) < 10:
                    users[user_id]["counts"]["items"] += 1
                else:
                    return -1
            else:
                users[user_id]["counts"]["curiosities"] += 1

            with open('limits.json', 'w', encoding='utf-8') as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
                file.close()
            
            return 1
        else:
            return 0
