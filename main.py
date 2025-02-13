import discord
from discord.ext import commands
from mykey import mykey
from functions import *
from tickets import *
from database import crud


intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# Verify if bot is working
@client.event
async def on_ready():
    print('Bot is working.')


# Sending hello
@client.command(name='ola', aliases=['hello'])
async def ola(ctx):
    await ctx.send('Olá, caro cliente! Estou pronto para uso. Caso queira entender meu funcionamento, utilize o comando "!ajuda".')


# Sending secret message
@client.command(name='segredo', aliases=['segredinho', 'secret'])
async def segredo(ctx):
    await ctx.send('Bot segredinho. Shhhhh! -_-')


# help command
@client.command(name='ajuda', aliases=['help'])
async def ajuda(ctx):
    await ctx.send('**Olá! Eu sou o Random. Vou te explicar o que sou e como você pode me usar.**\n\nVeja bem, eu sou um bot que gera itens aleatórios para você usar em suas aventuras de RPG. Para isso, basta digitar o comando **!item** e eu vou te dar um item aleatório.\n\nSeus itens serão guardados na sua mochila automaticamente (você pode guardar até 10 itens e pode acessar a sua mochila através do comando **!abrirmochila**, depois disso, você terá que **!descartar** ou **!trocar** itens com outros jogadores).\n\nEspero que você goste e se divirta com os itens que eu vou te dar. Boa sorte!\n\n*Para ver todos os meus comandos disponíveis, utilize* **!comandos**.')


#command list
@client.command(name='comandos', aliases=['commands'])
async def comandos(ctx):
    await ctx.send('**Olá! Eu sou o Random.** Aqui está minha lista de comandos:\n\n**!ola** - Me cumprimenta.\n**!ajuda** ou **!help** - Explica o que eu sou e como você pode me usar.\n**!comandos** - Mostra a lista de comandos disponíveis.\n**!item** - Gera um item aleatório para você.\n**!mochila** - Lista os itens na mochila do usuário\n**!descartar [numero]** - Descarta um item da sua mochila de acordo com seu índice. Exemplo: !descartar 1\n**!troca [numero] @usuario [numero]** - Troca um item de sua mochila com o de outro usuário. Exemplo: !troca 1 @fulano 2 (esse comando solicita uma troca do seu item número 1 pelo item número 2 do usuário mencionado)\n\n**Espero que você se divirta com meus comandos!**')


# Open Bag
@client.command(name='abrirmochila', aliases=['mochila', 'bag', 'openbag'])
async def abrirmochila(ctx):

    user_id = ctx.author.id
    
    bag = crud.open_bag(user_id)

    if len(bag) > 0:
        bag_str = 'Seus itens:\n\n'
        for item in bag:
            n = bag.index(item) + 1
            bag_str += f'**{n} ->** {item}\n'
        await ctx.send(bag_str)
    else:
        await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')


# Remove Item
@client.command(name='descartar', aliases=['remover', 'lixeira', 'jogarfora'])
async def descartar(ctx, i: int):
    user_id = ctx.author.id

    message = crud.remove_item(i, user_id)

    await ctx.send(message)


# Random Item
@client.command(name='item')
async def item(ctx):
    user_id = ctx.author.id

    item = crud.return_free_item(user_id)

    if item == 0:
        await ctx.send('Você já pegou muitos itens hoje. Volte amanhã!')
    elif item == -1:
        await ctx.send('Sua mochila está cheia! Descarte ou troque itens para pegar mais. **!ajuda** para mais informações.')
    else:
        if "Jackpot!" in item:
            crud.jackpot(user_id)
            await ctx.send(f'**💰 Ding ding ding! TEMOS UM VENCEDOR!?:**\n\n**->** {item}\n\nCréditos permitem que você tire vários itens sem a limitação de dois itens por dia!')
        else:
            if crud.add_item(item, user_id):
                await ctx.send(f'**Ding ding ding! Você ganhou o item a seguir:**\n\n**->** {item}\n\nUse o comando **!abrirmochila** para ver seus itens!{message_vip}')
            else:
                await ctx.send('Algo deu errado ao guardar seu item! Tente novamente.')



# Random Curiosity
@client.command(name='curiosidade')
async def curiosidade(ctx):
    user_id = str(ctx.author.id)
    if check_limit(user_id, "curiosities") == 0:
        curiosidade = return_sp()
        await ctx.send(f'**Está na hora da cursiosidade aleatória! Será que você já sabia?**\n\n-> {curiosidade}')
    else:
        await ctx.send('Você já sabe coisas demais. Volte amanhã!')


# Exchange items
@client.command(name="troca", aliases=["trocar"])
async def troca(ctx, item1: int, usuario: discord.Member, item2: int):
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    solicitante = ctx.author
    mencionado = usuario
    solicitante_id = str(solicitante.id)
    mencionado_id = str(mencionado.id)

    nameitem1 = name_item_user(solicitante_id, item1)
    nameitem2 = name_item_user(mencionado_id, item2)

    if nameitem1 not in users[solicitante_id]["bag"]:
        await ctx.send(f"❌ {solicitante.mention}, você não possui o item `{item1}`.")
        return

    if nameitem2 not in users[mencionado_id]["bag"]:
        await ctx.send(f"❌ {mencionado.mention}, ele não possui o item `{item2}`.")
        return
    

    # Creating a exchange ticket

    ticket_id = str(len(load_tickets()) + 1)

    ticket = {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "type": 0, 
        "user_id": solicitante_id,
        "item": nameitem1,
        "purpose": nameitem2,
        "user_id_request": mencionado_id,
        "result": "",
        "status": 1  # Status 1: Open - Status 0: Closed
    }

    tickets = load_tickets()
    tickets[ticket_id] = ticket
    save_tickets(tickets)

    name_item1 = name_item_user(str(solicitante.id), item1)
    name_item2 = name_item_user(str(mencionado.id), item2)

    mensagem = (
        f"🔄 {mencionado.mention}, {solicitante.mention} quer trocar um item com você! `ID de troca: {ticket_id}`\n"
        f"📌 Ele quer trocar o item `{nameitem1}` pelo seu item `{nameitem2}`.\n"
        f"✉ Para aceitar, digite `!aceito {ticket_id}` ou `!recuso {ticket_id}`.\n"
        f"❌ Se mudou de ideia e quer cancelar a troca, digite `!cancelar {ticket_id}`."
    )

    await ctx.send(mensagem)


@client.command(name="cancelar", aliases=["cancela", "cancelartroca"])
async def cancelar(ctx, ticket_id: str):
    tickets = load_tickets()

    ticket = tickets[ticket_id]

    if str(ctx.author.id) != ticket["user_id"]:
        await ctx.send("🚫 Você não pode cancelar esta troca, pois não é o solicitante.")
        return
    
    if ticket["status"] == 1 and ticket["result"] == "":    
        ticket["result"] = "Cancelado"
        ticket["status"] = 0
        save_tickets(tickets)

        mensagem = (
            f" {ctx.author.mention} cancelou a troca!\n"
        )
    else:
        mensagem = (
            f"❌ {ctx.author.mention} a troca em questão já foi finalizada!\n"
        )

    await ctx.send(mensagem)


@client.command(name="aceito")
async def aceito(ctx, ticket_id: str):
    try:
        users = json.load(open('limits.json', 'r', encoding='utf-8'))
    except Exception as e:
        print(e)

    tickets = load_tickets()

    if ticket_id not in tickets:
        await ctx.send("❌ Ticket não encontrado.")
        return

    ticket = tickets[ticket_id]

    if str(ctx.author.id) != ticket["user_id_request"]:
        await ctx.send("🚫 Você não pode aceitar esta troca, pois não é o destinatário.")
        return

    item1 = ticket["item"]
    solicitante_id = ticket["user_id"]
    mencionado_id = ticket["user_id_request"] 
    item2 = ticket["purpose"]

    if item1 not in users[solicitante_id]["bag"]:
        await ctx.send(f"❌ O item `{item1}` não está mais no inventário de {ctx.author.mention}. Troca cancelada.")
        return
    
    if item2 not in users[mencionado_id]["bag"]:
        await ctx.send(f"❌ O item `{item2}` não está mais no inventário de {ctx.author.mention}. Troca cancelada.")
        return
    
    index_item1 = users[solicitante_id]["bag"].index(item1)
    index_item2 = users[mencionado_id]["bag"].index(item2)
    
    swap_items(solicitante_id, index_item1, mencionado_id, index_item2)

    ticket["result"] = "Aceito"
    ticket["status"] = 0
    save_tickets(tickets)

    solicitante = await client.fetch_user(int(solicitante_id))
    mencionado = ctx.author

    mensagem = (
        f"✅ {mencionado.mention} aceitou a troca!\n"
        f"🔄 {solicitante.mention}, sua troca do item `{ticket['item']}` pelo `{ticket['purpose']}` foi aceita!"
    )

    await ctx.send(mensagem)


@client.command(name="recuso")
async def recuso(ctx, ticket_id: str):
    tickets = load_tickets()

    if ticket_id not in tickets:
        await ctx.send("❌ Ticket não encontrado.")
        return

    ticket = tickets[ticket_id]

    # Verificar se o usuário tem permissão para recusar a troca
    if str(ctx.author.id) != ticket["user_id_request"]:
        await ctx.send("🚫 Você não pode recusar esta troca, pois não é o destinatário.")
        return

    # Atualizar status do ticket
    ticket["result"] = "Recusado"
    ticket["status"] = 0  # Ticket fechado
    save_tickets(tickets)

    # Notificar os envolvidos
    solicitante = await client.fetch_user(int(ticket["user_id"]))
    mencionado = ctx.author

    mensagem = (
        f"❌ {mencionado.mention} recusou a troca.\n"
        f"🔄 {solicitante.mention}, sua solicitação para trocar `{ticket['item']}` pelo `{ticket['purpose']}` foi recusada."
    )

    await ctx.send(mensagem)

client.run(mykey)