import discord
from discord.ext import commands
from mykey import mykey
from functions import *

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# Verify if bot is working
@client.event
async def on_ready():
    print('Bot is working.')


# Sending hello
@client.command(name='ola')
async def ola(ctx):
    await ctx.send('Olá, caro cliente! Estou pronto para uso. Caso queira entender meu funcionamento, utilize o comando "!ajuda".')


# Sending secret message
@client.command()
async def segredo(ctx):
    await ctx.send('Bot segredinho. Shhhhh! -_-')


# help command
@client.command(name='ajuda', aliases=['help'])
async def ajuda(ctx):
    await ctx.send('**Olá! Eu sou o Random. Vou te explicar o que sou e como você pode me usar.**\n\nVeja bem, eu sou um bot que gera itens aleatórios para você usar em suas aventuras de RPG. Para isso, basta digitar o comando **!item** e eu vou te dar um item aleatório.\n\nSeus itens serão guardados na sua mochila automaticamente (você pode guardar até 10 itens e pode acessar a sua mochila através do comando **!abrirmochila**, depois disso, você terá que **!descartar** ou trocar itens com outros jogadores).\n\nEspero que você goste e se divirta com os itens que eu vou te dar. Boa sorte!\n\nQuer uma curiosidade aleatória? Use o comando **!curiosidade** e eu vou te contar algo que você talvez não saiba. Divirta-se!\n\n*Para ver todos os meus comandos disponíveis, utilize* **!comandos**.')


#command list
@client.command(name='comandos')
async def comandos(ctx):
    await ctx.send('**Olá! Eu sou o Random.** Aqui está minha lista de comandos:\n\n**!ola** - Me cumprimenta.\n**!ajuda** ou **!help** - Explica o que eu sou e como você pode me usar.\n**!comandos** - Mostra a lista de comandos disponíveis.\n**!item** - Gera um item aleatório para você.\n**!curiosidade** - Conta uma curiosidade aleatória para você.\n**!abrirmochila** - Lista os itens na mochila do usuário\n**!descartar [numero]** - Descarta um item da sua mochila de acordo com seu índice. Exemplo: !descartar 1\n\n**Espero que você se divirta com meus comandos!**')


# Open Bag
@client.command(name='abrirmochila')
async def abrirmochila(ctx):
    user_id = str(ctx.author.id)
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    if user_id in users:
        bag = users[user_id]["bag"]
        if len(bag) > 0:
            bag_str = 'Seus itens:\n\n'
            for item in bag:
                n = bag.index(item) + 1
                bag_str += f'**{n} ->** {item}\n'
            await ctx.send(bag_str)
        else:
            await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')
    else:
        await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')


# Remove Item
@client.command(name='descartar')
async def descartar(ctx, i: int):
    user_id = str(ctx.author.id)
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    if user_id in users:
        bag = users[user_id]["bag"]
        if len(bag) > 0:
            if i > 0 and i <= len(bag):
                item = bag[i - 1]
                bag.remove(item)
                users[user_id]["bag"] = bag
                with open('limits.json', 'w', encoding='utf-8') as file:
                    json.dump(users, file, indent=4, ensure_ascii=False)
                    file.close()
                await ctx.send(f'Você descartou o item **{item}**.')
            else:
                await ctx.send('Escolha um número válido para descartar.')
        else:
            await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')
    else:
        await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')


# Random Item
@client.command(name='item')
async def item(ctx):
    user_id = str(ctx.author.id)
    if check_limit(user_id, "items") == 1:
        item = return_gp()
        if add_item(user_id, item):
            await ctx.send(f'**Ding ding ding! Você ganhou o item a seguir:**\n\n**->** {item}\n\nUse o comando **!abrirmochila** para ver seus itens!')
        else:
            await ctx.send('Algo deu errado ao guardar seu item! Tente novamente.')
    elif check_limit(user_id, "items") == 0:
        await ctx.send('Você já pegou muitos itens hoje. Volte amanhã!')
    else:
        await ctx.send('Sua mochila está cheia! Descarte ou troque itens para pegar mais. **!ajuda** para mais informações.')


# Random Curiosity
@client.command(name='curiosidade')
async def curiosidade(ctx):
    user_id = str(ctx.author.id)
    if check_limit(user_id, "curiosities") == 1:
        curiosidade = return_sp()
        await ctx.send(f'**Está na hora da cursiosidade aleatória! Será que você já sabia?**\n\n-> {curiosidade}')
    else:
        await ctx.send('Você já sabe coisas demais. Volte amanhã!')


client.run(mykey)