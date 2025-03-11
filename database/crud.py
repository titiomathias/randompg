import sqlite3
import json
from .functions import *
from datetime import datetime

path = "database/randombase.db"

conn = sqlite3.connect(path)
cursor = conn.cursor()

from datetime import datetime

def return_free_item(user_id: int):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"

    cursor.execute(query)
    user = cursor.fetchall()

    if len(user) > 0:
        data_atual = datetime.now().date()
        
        try:
            data = datetime.strptime(user[0][1], '%d/%m/%Y').date()
        except ValueError as e:
            print(f"Erro ao converter data: {e}")
            return -1

        diferenca_dias = (data_atual - data).days

        if diferenca_dias > 0:
            update_query = '''
            UPDATE users 
            SET date = ?, credits = credits + ?, curiosities_free = 2 
            WHERE user_id = ?
            '''
            cursor.execute(update_query, (data_atual.strftime('%d/%m/%Y'), diferenca_dias, user_id))
            conn.commit()

            return return_free_item(user_id)

        if user[0][3] > 0:
            bag = open_bag(user_id)
            if len(bag[0]) < bag[1]:
                i = return_gp()

                n = user[0][3] - 1

                query = '''
                UPDATE users SET credits = ? WHERE user_id = ?
                '''
                cursor.execute(query, (n, user_id))
                conn.commit()

                query = f"SELECT * FROM items WHERE id = {i}"
                cursor.execute(query)
                item = cursor.fetchone()[1]

                if "Jackpot" in item:
                    jackpot(user_id)
                else:
                    add_item(item, user_id)

                return item
            else:
                return -1
        else:
            return 0
    else:
        # Adiciona o usuário com a data no formato ISO
        add_user(user_id, datetime.now().strftime('%d/%m/%Y'))
        return return_free_item(user_id)


def return_free_curiosity(user_id: int):
    query = f"SELECT * FROM users WHERE user_id = {user_id} AND curiosities_free > 0"

    cursor.execute(query)
    user = cursor.fetchall()

    if len(user) > 0:
        i = return_sp()

        n = user[0][2]-1

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
    query = f"INSERT INTO users (user_id, date, curiosities_free, credits, bag) VALUES (?, ?, ?, ?, ?)"

    cursor.execute(query, (int(user_id), date, 2, 2, json.dumps({'items': [], 'slots': 10}, ensure_ascii=False)))

    conn.commit()


def add_item(item_name, user_id):
    bag_data = open_bag(user_id)
    bag = bag_data[0]

    if len(bag) < bag_data[1]:
        bag.append(item_name)

        bag_data = {
            'items': bag,
            'slots': bag_data[1]
        }

        try:
            bag_update = json.dumps(bag_data, ensure_ascii=False)

            query = '''
            UPDATE users SET bag = ? WHERE user_id = ?
            '''

            cursor.execute(query, (bag_update, user_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating database: {e}\n")
            return False
    else:
        print("Bag is full, cannot add item.\n")
        return False


def remove_item(item_id, user_id):
    bag_data = open_bag(user_id)
    bag = bag_data[0]

    if len(bag) > 0:
        try:
            item = bag[item_id - 1]
            bag.remove(item)
        except:
            return 'Escolha um número válido para descartar.'
        
        bag_data = {
            'items': bag,
            'slots': bag_data[1]
        }

        bag_update = json.dumps(bag_data, ensure_ascii=False)

        query = '''
        UPDATE users SET bag = ? WHERE user_id = ?
        '''

        cursor.execute(query, (bag_update, user_id))

        conn.commit()

        return f'**Você descartou com sucesso o item: {item}**'
    else:
        return 'Sua mochila está vazia! Utilize o comando `!item` para ganhar um item novo!'


def open_bag(user_id):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()

    if not user:
        add_user(user_id, datetime.now().strftime("%d/%m/%Y"))
        return open_bag(user_id)
    
    try:
        bag_data = json.loads(user[-1])
        bag = bag_data['items']
        slots = bag_data['slots']
    except:
        bag = []

    return bag, slots


def jackpot(user_id):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"

    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        query = f"UPDATE users WHERE credits = credits + 100 WHERE user_id = ?"

        cursor.execute(query, (user_id,))
        conn.commit()

        return True
    else:
        add_user(user_id, str(datetime.now().strftime("%d/%m/%Y")))
        return jackpot(user_id)


def create_ticket(user_id: int, type: int, item: str, purpose: str, user_id_request: int):
    try:
        query = f"INSERT INTO tickets (date, user_id, item, purpose, user_id_request, result, status) VALUES (?, ?, ?, ?, ?, ?, ?)"

        cursor.execute(query, (str(datetime.now().strftime("%d/%m/%Y")), user_id, item, purpose, user_id_request, '', 1))

        conn.commit()

        return cursor.lastrowid
    except Exception as e:
        print(e)
        return None
    

def fetch_ticket(ticket_id: int):
    query = f"SELECT * FROM tickets WHERE id = {ticket_id}"
    cursor.execute(query)
    return cursor.fetchone()


def fetch_aposta(aposta_id: int):
    query = f"SELECT * FROM apostas WHERE id = {aposta_id}"
    cursor.execute(query)
    return cursor.fetchone()


def fetch_sell_buy(business_id: int):
    query = f"SELECT * FROM sell_buy WHERE id = {business_id}"
    cursor.execute(query)
    return cursor.fetchone()


def update_sell_buy_status(business_id: int, status: int, result: str):
    query = f"UPDATE sell_buy SET status = {status}, result = '{result}' WHERE id = {business_id}"
    cursor.execute(query)
    conn.commit()


def update_ticket_status(ticket_id: int, status: int, result: str):
    if status == 0:
        # Se o status for 0, deleta o ticket
        delete_query = f"DELETE FROM tickets WHERE id = {ticket_id}"
        cursor.execute(delete_query)
    else:
        # Caso contrário, atualiza o status e o result
        update_query = f"UPDATE tickets SET status = {status}, result = '{result}' WHERE id = {ticket_id}"
        cursor.execute(update_query)

    # Commit para salvar as alterações no banco de dados
    conn.commit()


def update_aposta_status(aposta_id: int, status: int, result: str):
    try:
        if status == 0:
            delete_query = f"DELETE FROM apostas WHERE id = {aposta_id}"
            cursor.execute(delete_query)
        else:
            update_query = f"UPDATE apostas SET status = {status}, result = '{result}' WHERE id = {aposta_id}"
            cursor.execute(update_query)

        conn.commit()

        return True
    except Exception as e:
        print("Erro ao atualiar status de aposta:", e)
        return False


def close_ticket(user_id_command: int, ticket_id: int, result: str):
    results = ["aceito", "recuso", "cancelar"]

    if result not in results:
        return '❌ Comando inválido! Utilize `!aceito`, `!recuso` ou `!cancelar`.'

    ticket = fetch_ticket(ticket_id)
    if not ticket:
        return '❌ Ticket não encontrado ou já finalizado.'

    if result == "cancelar":
        if ticket[2] == user_id_command:
            update_ticket_status(ticket_id, 0, 'Cancelado')
            return '✅ Troca cancelada com sucesso!'
        else:
            return '❌ Você não pode cancelar uma troca que não foi solicitada por você.'

    elif result == "aceito":
        if ticket[5] == user_id_command:
            troca = swap_items(ticket[2], ticket[5], ticket[3], ticket[4])
            
            if "not found" in troca:
                return '❌ O item de algum dos envolvidos não foi encontrado ou não está mais em seu inventário.'
            elif "fail" in troca:
                return '❌ Ocorreu um erro ao realizar a troca.'
            else:
                update_ticket_status(ticket_id, 0, 'Aceito')
                return [ticket[2], ticket[5], ticket[3], ticket[4]]
        else:
            return '❌ Você não pode aceitar uma troca que não está envolvido!'

    elif result == "recuso":
        if ticket[5] == user_id_command:
            update_ticket_status(ticket_id, 0, 'Recusado')
            return '✅ Troca recusada com sucesso!'
        else:
            return '❌ Você não pode recusar uma troca que não está envolvido.'
    

def swap_items(user_id: int, user_id_request: int, item1: str, item2: str):
    bag_user_id, user_id_slots = open_bag(user_id)
    if not bag_user_id or not user_id_slots:
        return "fail: bag do user_id não encontrada"

    bag_user_id_request, bag_user_id_request_slots = open_bag(user_id_request)
    if not bag_user_id_request or not bag_user_id_request_slots:
        return "fail: bag do user_id_request não encontrada"

    if item1 not in bag_user_id:
        return "item1 not found"
    if item2 not in bag_user_id_request:
        return "item2 not found"

    index_1 = bag_user_id.index(item1)
    index_2 = bag_user_id_request.index(item2)

    bag_user_id[index_1] = item2
    bag_user_id_request[index_2] = item1

    bag_data_user_id = {
        'items': bag_user_id,
        'slots': user_id_slots
    }

    bag_data_user_id_request = {
        'items': bag_user_id_request,
        'slots': bag_user_id_request_slots
    }

    try:
        bag_data_user_id_json = json.dumps(bag_data_user_id, ensure_ascii=False)
        bag_data_user_id_request_json = json.dumps(bag_data_user_id_request, ensure_ascii=False)
    except json.JSONEncodeError as e:
        print(f"Erro ao serializar dados JSON: {e}")
        return "fail"

    try:
        query = f"UPDATE users SET bag = ? WHERE user_id = {user_id}"
        cursor.execute(query, (bag_data_user_id_json,))
        conn.commit()

        query = f"UPDATE users SET bag = ? WHERE user_id = {user_id_request}"
        cursor.execute(query, (bag_data_user_id_request_json,))
        conn.commit()

        return "success"
    except sqlite3.Error as e:
        print(f"Erro ao executar query no banco de dados: {e}")
        return "fail"
    

def buy_slots(user_id, n):
    query = f"SELECT * FROM users WHERE user_id = {user_id}"

    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        bag_data = json.loads(user[-1])
        bag = bag_data['items']
        slots = bag_data['slots']

        if user[3] >= n*2:
            credits = user[3]
        else: 
            return False
        
        slots += n
        credits -= n*2

        bag_data = {
            'items': bag,
            'slots': slots
        }

        bag_update = json.dumps(bag_data, ensure_ascii=False)

        query = f"UPDATE users SET bag = ?, credits = ? WHERE user_id = {user_id}"

        cursor.execute(query, (bag_update, credits))
        conn.commit()

        return True
    else:
        return False
    

def sell_buy_item(user_id, user_id_request, item, value, type):
    ""


def do_sell_buy(user_id, user_id_request, item, value):
    ""

    

def close_sell_buy(user_id, business_id, result):
    ""


def check_credits(user_id):
    query = "SELECT date, credits FROM users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if user:
        data_atual = datetime.now().date()
        
        try:
            data = datetime.strptime(user[0], '%d/%m/%Y').date()
        except ValueError as e:
            print(f"Erro ao converter data: {e}")
            return -1

        diferenca_dias = (data_atual - data).days

        if diferenca_dias > 0:
            update_query = '''
            UPDATE users 
            SET date = ?, credits = credits + ?, curiosities_free = 2 
            WHERE user_id = ?
            '''
            cursor.execute(update_query, (data_atual.strftime('%d/%m/%Y'), diferenca_dias, user_id))
            conn.commit()

            cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
            updated_user = cursor.fetchone()
            return updated_user[0]
        else:
            return user[1]
    else:
        # Adiciona o usuário se não existir
        add_user(user_id, datetime.now().strftime('%d/%m/%Y'))
        return check_credits(user_id)
    
    
def abriraposta(user_id, valor, user_id_request):
    try:
        query = f"INSERT INTO apostas (date, user_id, value, user_id_request, result, status) VALUES (?, ?, ?, ?, ?, ?)"

        cursor.execute(query, (str(datetime.now().strftime("%d/%m/%Y")), user_id, valor, user_id_request, '', 1))

        conn.commit()

        return cursor.lastrowid
    except Exception as e:
        print(e)
        return None


def close_aposta(user_id_command: int, aposta_id: int, result: str):
    results = ["pagar", "correr", "desistir"]

    if result not in results:
        return '❌ Comando inválido! Utilize `!pagar`, `!correr` ou `!desistir`.'

    aposta = fetch_aposta(aposta_id)
    
    if not aposta:
        return '❌ ID de aposta não encontrado ou já finalizado.'
    
    if result == "desistir":
        if aposta[2] == user_id_command:
            update_aposta_status(aposta_id, 0, 'Cancelado')
            return '✅ Você desistiu da aposta!'
        else:
            return '❌ Você não desistir de uma aposta por outra pessoa!'

    elif result == "pagar":
        if aposta[4] == user_id_command:
            if aposta[6] == 2:
                return '❌ A aposta já está em andamento e não é possível pagá-la novamente!'
    
            resultado = update_aposta_status(aposta_id, 2, 'Andamento')
            if resultado:
                return (aposta[2], aposta[4], aposta[3])
            else:
                return '❌ Um erro inesperado ocorreu e não foi possível aceitar a aposta.'
        else:
            return '❌ Você não pode pagar uma aposta por outro usuário.'

    elif result == "correr":
        if aposta[4] == user_id_command:
            if aposta[6] == 2:
                return '❌ A aposta já está em andamento e não é mais possível correr!'

            update_aposta_status(aposta_id, 0, 'Recusado')
            return '✅ Você correu. A aposta foi recusada.'
        else:
            return '❌ Você não pode correr de uma aposta por outro usuário.'
    

def update_saldo_aposta(winner, loser, value):
    try:
        query_increment = "UPDATE users SET credits = credits + ? WHERE user_id = ?"
        query_decrement = "UPDATE users SET credits = credits - ? WHERE user_id = ?"
        
        cursor.execute(query_increment, (value, winner))
        conn.commit()

        cursor.execute(query_decrement, (value, loser))
        conn.commit()

        return True
    except Exception as e:
        print("Erro ao atualizar saldo do vencedor e perdedor: ", e)
        return False



def roleta(aposta_id):
    n = randint(1, 36)

    vermelhos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    
    if n in vermelhos:
        cor = "vermelho"
        emoji = "🔴"
    else:
        cor = "preto"
        emoji = "⚫"

    aposta = fetch_aposta(aposta_id)

    query = "SELECT value, user_id, user_id_request, user_id_color FROM apostas WHERE id = ?"
    cursor.execute(query, (aposta_id,))
    resultado = cursor.fetchone()

    valor = resultado[0]
    user_id = resultado[1]
    user_id_request = resultado[2]
    user_id_color = resultado[3]

    if user_id_color == cor:
        update_saldo_aposta(user_id, user_id_request, valor)
        vencedor = user_id
        perdedor = user_id_request
    else:
        update_saldo_aposta(user_id_request, user_id, valor)
        vencedor = user_id_request
        perdedor = user_id

    update_aposta_status(aposta_id, 0, "Encerrado")

    return {"vencedor": vencedor, "perdedor": perdedor, "valor": valor, "emoji": emoji, "numero": n, "cor": cor}


def setcolor(color, aposta_id, type):
    if type == 1:
        user = "user_id_color"
        user2 = "user_id_request_color"
    else:
        user = "user_id_request_color"
        user2 = "user_id_color"

    if color == "vermelho":
        color2 = "preto"
    else:
        color2 = "vermelho"

    query = f"UPDATE apostas SET {user} = ?, {user2} = ?  WHERE id = ?"
    cursor.execute(query, (color, color2, aposta_id))
    conn.commit()

    return roleta(aposta_id)


def rank():
    try:
        query = f"SELECT user_id, credits FROM users ORDER BY credits DESC LIMIT 10"
        cursor.execute(query)
        rank = cursor.fetchall()
        print(rank)
        return rank
    except Exception as e:
        print("Um erro inesperado ocorreu ao tentar rankear. Erro: ", e)
        return


# Adm function
def deposit(user_id, n):
    query = f"UPDATE users SET credits = credits + {n} WHERE user_id = {user_id}"
    cursor.execute(query)
    conn.commit()

    return True    
