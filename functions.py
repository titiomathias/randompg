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

# Return random curiosity
def return_sp():
    sp = randint(1, 101)

    with open('d100.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        curiosity = lines[sp].strip("\n")
        file.close()
    return curiosity


# Still in development
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
            }
        }

        users[user_id]["counts"][command_name] += 1

        with open('limits.json', 'w', encoding='utf-8') as file:
            json.dump(users, file, indent=4, ensure_ascii=False)
            file.close()

        return True
    else:
        if users[user_id]["counts"][command_name] < 2:
            users[user_id]["counts"][command_name] += 1

            with open('limits.json', 'w', encoding='utf-8') as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
                file.close()
            
            return True
        else:
            return False
