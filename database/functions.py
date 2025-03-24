from random import randint, choice
import uuid
import os
import shutil
import time


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


# Make backup
def verify_backup():
    try:
        if not os.path.exists("backup.db"):
            print("Backup não encontrado. Criando um novo backup...")
            shutil.copy("database/randombase.db", "backup.db")
            return

        last_modified_time = os.path.getmtime("backup.db")
        current_time = time.time()

        if (current_time - last_modified_time) > 6 * 3600:
            print("Backup desatualizado. Criando um novo backup...")
            shutil.copy("database/randombase.db", "backup.db")
        else:
            print("Backup está atualizado.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
