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
async def segredo(ctx):
    await ctx.send('Bot segredinho. Shhhhh! -_-')

@client.command()
async def ajuda(ctx):
    await ctx.send('**Olá! Eu sou o Random. Vou te explicar o que sou e como você pode me usar.**\n\nVeja bem, eu sou um bot que gera itens aleatórios para você usar em suas aventuras de RPG. Para isso, basta digitar o comando **!item** e eu vou te dar um item aleatório. Simples assim! Espero que você goste e se divirta com os itens que eu vou te dar. Boa sorte!\n\nQuer uma curiosidade aleatória? Use o comando **!curiosidade** e eu vou te contar algo que você talvez não saiba. Divirta-se!')

@client.command()
async def comandos(ctx):
    await ctx.send('**Olá! Eu sou o Random.** Aqui está minha lista de comandos:\n\n**!ola** - Me cumprimenta.\n**!ajuda** ou **!help** - Explica o que eu sou e como você pode me usar.\n**!comandos** - Mostra a lista de comandos disponíveis.\n**!item** - Gera um item aleatório para você.\n**!curiosidade** - Conta uma curiosidade aleatória para você.\n\n**Espero que você se divirta com meus comandos!**')

@client.command()
async def item(ctx):
    user_id = str(ctx.author.id)
    if check_limit(user_id, "items"):
        item = return_gp()
        await ctx.send(f'**Ding ding ding! Você ganhou o item a seguir:**\n\n**->** {item}')
    else:
        await ctx.send('Você já pegou muitos itens hoje. Volte amanhã!')

@client.command()
async def curiosidade(ctx):
    user_id = str(ctx.author.id)
    if check_limit(user_id, "curiosities"):
        curiosidade = return_sp()
        await ctx.send(f'**Está na hora da cursiosidade aleatória! Será que você já sabia?**\n\n-> {curiosidade}')
    else:
        await ctx.send('Você já sabe coisas demais. Volte amanhã!')


client.run(mykey)