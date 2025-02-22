from random import randint, choice
from datetime import datetime
import uuid

# return id unico
def gerar_id_unico():
    lista = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    return f"{choice(lista)}{str(uuid.uuid4().int)[:5]}"


# Return random item
def return_gp():
    gp = randint(1, 1000)

    return gp


# Return random curiosity
def return_sp():
    sp = randint(1, 100)

    return sp
