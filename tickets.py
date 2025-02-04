import discord
import json
import os
from discord.ext import commands
from datetime import datetime

TICKETS_FILE = "ticket.json"

# Função para carregar tickets do arquivo JSON
def load_tickets():
    if os.path.exists(TICKETS_FILE):
        with open(TICKETS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Função para salvar tickets no arquivo JSON
def save_tickets(tickets):
    with open(TICKETS_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4, ensure_ascii=False)


