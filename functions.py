from random import randint

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