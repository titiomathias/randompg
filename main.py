import discord
from discord.ext import commands
from mykey import mykey
from functions import *

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Bot is working.')

@client.command()
async def ola(ctx):
    await ctx.send('Olá, caro cliente! Estou pronto para uso. Caso queira entender meu funcionamento, utilize o comando "!ajuda".')

@client.command()
async def ajuda(ctx):
    await ctx.send('**Vou te explicar o que sou e como você pode me usar.**\n\nVeja bem, eu sou um bot que gera itens aleatórios para você usar em suas aventuras de RPG. Para isso, basta digitar o comando **!item** e eu vou te dar um item aleatório. Simples assim! Espero que você goste e se divirta com os itens que eu vou te dar. Boa sorte!\n\nQuer uma curiosidade aleatória? O comando !curiosidade está sendo desenvolvido para gerar curiosidades aleatórias para você!')

@client.command()
async def item(ctx):
    item = return_gp()
    await ctx.send(f'**Ding ding ding! Você ganhou o item a seguir:**\n\n**->** {item}')

#@client.command() Still in development
#async def curiosidade(ctx):
#    curiosidade = return_sp()
#    await ctx.send(f'Está na hora da cursiosidade aleatória! Será que você já sabia?\n\n-> {curiosidade}')


client.run(mykey)