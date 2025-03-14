import discord
from discord.ext import commands
from mykey import mykey
from database import crud

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)


# Verify if bot is working
@client.event
async def on_ready():
    print('Bot is working. Last update -> 24/02/2025 - 11:11')


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
    await ctx.send('**Olá! Eu sou o Random. Vou te explicar o que sou e como você pode me usar.**\n\nVeja bem, eu sou um bot que gera itens aleatórios para você usar em suas aventuras de RPG. Para isso, basta digitar o comando **!item** e eu vou te dar um item aleatório.\n\nSeus itens serão guardados na sua mochila automaticamente (você pode guardar até 10 itens e pode acessar a sua mochila através do comando **!mochila**, depois disso, você terá que **!descartar**, **!trocar** ou **!melhorarmochila**).\n\nEspero que você goste e se divirta com os itens que eu vou te dar. Boa sorte!\n\n*Para ver todos os meus comandos disponíveis, utilize* **!comandos**.')


#command list
@client.command(name='comandos', aliases=['commands'])
async def comandos(ctx):
    await ctx.send('**Olá! Eu sou o Random.** Aqui está minha lista de comandos:\n\n**!ola** - Me cumprimenta.\n**!ajuda** ou **!help** - Explica o que eu sou e como você pode me usar.\n**!comandos** - Mostra a lista de comandos disponíveis.\n**!item** - Gera um item aleatório para você.\n**!mochila** - Lista os itens na mochila do usuário\n**!descartar [numero]** - Descarta um item da sua mochila de acordo com seu índice. Exemplo: !descartar 1\n**!creditos** - Mostra os créditos do usuário e uma descrição de sua mecânica.\n**!rank** - Mostra o rank dos 10 usuários com mais créditos.\n\n**!troca [numero] @usuario [numero]** - Troca um item de sua mochila com o de outro usuário. Exemplo: !troca 1 @fulano 2 -> Esse comando solicita uma troca do seu item número 1 pelo item número 2 do usuário mencionado.\n\n**!melhorarmochila [n]** - Aumentar a sua mochila em um número de espaços fornecidos, gastando 2 créditos por espaço. Exemplo: !melhorarmochila 2 -> Aumanta 2 espaços da mochila por 4 créditos.\n\n**!apostar [creditos] @usuario** -  Aposta um número de créditos na roleta com outro usuário.\n\n**Espero que você se divirta com meus comandos!**')


# Open Bag
@client.command(name='abrirmochila', aliases=['mochila', 'bag', 'openbag'])
async def abrirmochila(ctx):

    user_id = ctx.author.id
    
    bag, slots = crud.open_bag(user_id)

    if len(bag) > 0:
        bag_str = f'**Espaços utilizados:** {len(bag)}/{slots}.\n\n**Seus itens:**\n\n'
        n = 1
        for item in bag:
            bag_str += f'**{n} ->** {item}\n'
            n+=1
        await ctx.send(bag_str)
    else:
        await ctx.send('Sua mochila está vazia! Use o comando **!item** para pegar itens.')


# Remove Item
@client.command(name='descartar', aliases=['remover', 'lixeira', 'jogarfora', 'Descartar'])
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
        await ctx.send('Você está sem créditos para sortear mais itens! Volte amanhã!')
    elif item == -1:
        await ctx.send('Sua mochila está cheia! Descarte ou troque itens para pegar mais. Use o comando `!ajuda` para mais informações.')
    else:
        if "Jackpot" in item:
            await ctx.send(f'**💰 Ding ding ding! TEMOS UM VENCEDOR!?:**\n\n**->** {item}\n\n')
        else:
            await ctx.send(f'**Ding ding ding! Você ganhou o item a seguir:**\n\n**->** {item}\n\nUse o comando **!abrirmochila** para ver seus itens')


# Random Curiosity
@client.command(name='curiosidade')
async def curiosidade(ctx):
    user_id = ctx.author.id

    curiosidade = crud.return_free_curiosity(user_id)

    if curiosidade == '' :
        await ctx.send('Você já sabe coisas demais. Volte amanhã!')
    else:
        await ctx.send(f'**Está na hora da cursiosidade aleatória! Será que você já sabia?**\n\n-> {curiosidade}')
    
        


# Exchange items
@client.command(name='troca', aliases=['trocar', 'exchange'])
async def troca(ctx, item1: int, usuario: discord.Member, item2: int):
    solicitante = ctx.author
    mencionado = usuario
    solicitante_id = solicitante.id
    mencionado_id = mencionado.id

    if solicitante_id == mencionado_id:
        await ctx.send("❌ Você não pode trocar itens com você mesmo.")
        return

    try:
        nameitem1 = crud.open_bag(solicitante_id)[0][item1 - 1]
        nameitem2 = crud.open_bag(mencionado_id)[0][item2 - 1]
        ticket_id = crud.create_ticket(solicitante_id, 1, nameitem1, nameitem2, mencionado_id)
    except Exception as e:
        print(e)
        await ctx.send("❌ Não foi possível solicitar a troca no momento.")
    else:
        mensagem = (
            f"🔄 {mencionado.mention}, {solicitante.mention} quer trocar um item com você! `ID de troca: {ticket_id}`\n"
            f"📌 Ele quer trocar o item `{nameitem1}` pelo seu item `{nameitem2}`.\n"
            f"✉ Para aceitar, digite `!aceito {ticket_id}` ou `!recuso {ticket_id}`.\n"
            f"❌ Se mudou de ideia e quer cancelar a troca, digite `!cancelar {ticket_id}`."
        )

        await ctx.send(mensagem)


@client.command(name="cancelar", aliases=["cancela", "cancelartroca"])
async def cancelar(ctx, ticket_id: int):
    mensagem = crud.close_ticket(ctx.author.id, ticket_id, "cancelar")
    await ctx.send(mensagem)


@client.command(name="aceito")
async def aceito(ctx, ticket_id: int):
    dados = crud.close_ticket(ctx.author.id, ticket_id, "aceito")

    if "❌" in dados:
        await ctx.send(dados)
        return
    else:
        solicitante_id = dados[0]
        mencionado_id = dados[1]
        item1 = dados[2]
        item2 = dados[3]

        solicitante = await client.fetch_user(solicitante_id)
        mencionado = await client.fetch_user(mencionado_id)

        mensagem = (
            f"✅ {mencionado.mention} aceitou a troca!\n"
            f"🔄 {solicitante.mention}, sua troca do item `{item1}` pelo `{item2}` foi aceita!"
        )

        await ctx.send(mensagem)


@client.command(name="recuso")
async def recuso(ctx, ticket_id: int):
    dados = crud.close_ticket(ctx.author.id, ticket_id, "aceito")

    if "❌" in dados:
        await ctx.send(dados)
        return
    else:
        solicitante_id = dados[0]
        mencionado_id = dados[1]
        item1 = dados[2]
        item2 = dados[3]

        solicitante = await client.fetch_user(solicitante_id)
        mencionado = await client.fetch_user(mencionado_id)

        mensagem = (
            f"❌ {mencionado.mention} recusou a troca.\n"
            f"🔄 {solicitante.mention}, sua solicitação para trocar `{item1}` pelo `{item2}` foi recusada."
        )

        await ctx.send(mensagem)


@client.command(name="melhorarmochila", aliases=["melhorarbag", "aumentarmochila", "aumentarbag", "buyslots", "comprarslots", "comprarespaço", "comprarespaços"])
async def melhorarmochila(ctx, n: int = 1):
    user_id = ctx.author.id

    if n<=0:
        await ctx.send("**O mínimo de slots a serem incrementados é 1!**")
    else:
        message = crud.buy_slots(user_id, n)

        if message:
            await ctx.send("**Sua mochila foi melhorada! Agora você pode guardar mais itens.**")
        else:
            await ctx.send("**Você não tem créditos o suficiente para melhorar sua mochila!**")


@client.command(name="creditos", aliases=["credits", "saldo", "créditos", "credito", "crédito"])
async def creditos(ctx):
    user_id = ctx.author.id

    credits = crud.check_credits(user_id)

    await ctx.send(f"**💰 Confira seus créditos agora:**\n\n**->** 🪙 **Créditos**: {credits}\n\nTodos os dias, todos os jogadores ganham +1 crédito.\nCréditos são cumulativos e podem ser comprados ou adquiridos em negociações.\n\nAbra o menu `!ajuda` para mais informações.")


@client.command(name="aposta", aliases=["apostar", "gambly", "fazeraposta"])
async def aposta(ctx, creditos: int, usuario: discord.Member):
    user_id = ctx.author.id
    user_id_request = usuario.id

    if creditos <= 0:
        await ctx.send(f"**❌ O valor mínimo de aposta é de 1 crédito!**")
    else:
        if crud.check_credits(user_id) >= creditos and crud.check_credits(user_id_request) >= creditos:
            aposta_id = crud.abriraposta(user_id, creditos, user_id_request)

            mensagem = (
                f"**💰 {usuario.mention}, {ctx.author.mention} quer apostar {creditos} créditos com você!** `ID da aposta: {aposta_id}`\n"
                f"🪙 Para aceitar, digite `!pagar {aposta_id}` ou `!correr {aposta_id}`.\n"
                f"❌ Se mudou de ideia e quer cancelar a aposta, digite `!desistir {aposta_id}`."
            )

            await ctx.send(mensagem)
        else:
            await ctx.send(f"**Um ou mais usuários envolvidos não tem créditos suficientes para cobrir a aposta!**")


@client.command(nome="pagar", aliases=["pago", "cubro", "cobrir"])
async def pagar(ctx, aposta_id: int):
    retorno = crud.close_aposta(ctx.author.id, aposta_id, "pagar")

    if '❌' in retorno:
        await ctx.send(retorno)
    else:
        user = retorno[0]
        user_request = retorno[1]

        solicitante = await client.fetch_user(user)
        mencionado = await client.fetch_user(user_request)

        mensagem = f"🪙 {mencionado.mention} pagou a aposta!\n"

        await ctx.send(mensagem)

        roleta = (
            f"**🎰 Hora de Roletar! - ID da aposta: {aposta_id} 🎰**\n\n"
            f"**->**{solicitante.mention} e {mencionado.mention}, utilizem o comando `!cor (cor escolhida) (ID da aposta)` para escolher a cor que deseja! Exemplo: `!cor vermelho {aposta_id}`.\n\n"
            f"**Cores**:\n"
            f"**->** 🔴 Vermelho\n**->** ⚫ Preto\n\n"
            f"Não se preocupe, **a sorte sempre estará ao seu favor** 🤑."
        )

        await ctx.send(roleta)
        

@client.command(nome="correr", aliases=["fold"])
async def correr(ctx, aposta_id: int):
    retorno = crud.close_aposta(ctx.author.id, aposta_id, "correr")

    await ctx.send(retorno)


@client.command(nome="desistir", aliases=["desisto", "cancel", "giveup"])
async def desistir(ctx, aposta_id: int):
    retorno = crud.close_aposta(ctx.author.id, aposta_id, "desistir")

    await ctx.send(retorno)

@client.command(name="cor")
async def cor(ctx, cor: str, aposta_id: int):
    cores = ["vermelho", "preto"]

    cor = cor.lower()

    aposta = crud.fetch_aposta(aposta_id)

    if ctx.author.id == aposta[2] or ctx.author.id == aposta[4]:
        if aposta[6] == 2:
                if cor in cores:
                    if ctx.author.id == aposta[2]:            
                        resultado = crud.setcolor(cor, aposta_id, 1)
                    else:
                        resultado = crud.setcolor(cor, aposta_id, 2)

                    vencedor = await client.fetch_user(resultado["vencedor"])
                    perdedor = await client.fetch_user(resultado["perdedor"])

                    message = (
                        f"🎰🤑 TEMOS UM VENCEDOR! 🤑🎰\n\n"
                        f"**-> Número sorteado:** {resultado['emoji']} {resultado['numero']} -> {resultado['cor'].upper()}\n\n"
                        f"**Parabéns, {vencedor.mention}! Você acaba de ganhar {resultado['valor']} créditos de seu adversário {perdedor.mention}.**"
                    )

                    await ctx.send(message)
                else:
                    await ctx.send("❌ Cor inválida! Escolha uma cor que esteja na lista de cores da roleta! [Preto ou Vermelho].")
        else:
            await ctx.send("❌ A aposta ainda está pendente de ser aceita.")
    else:
        await ctx.send("❌ Você não está envolvido em uma aposta para escolher uma cor da roleta.")


@client.command(name="rank", aliases=["Rank", "Ranks"])
async def rank(ctx):
    rank = crud.rank()

    if len(rank) > 0:
        embed = discord.Embed(
            title="🪙 RANDOM RANK 🪙",
            description="Ranking dos usuários com mais créditos",
            color=discord.Color.gold()
        )

        # Adiciona os usuários ao embed
        for n, player in enumerate(rank, start=1):
            user = await client.fetch_user(player[0])
            creditos = player[1]

            if n == 1:
                medalha = "🥇"
                cor = discord.Color.gold()
            elif n == 2:
                medalha = "🥈"
                cor = discord.Color.light_grey()
            elif n == 3:
                medalha = "🥉"
                cor = discord.Color.dark_orange()
            else:
                medalha = "🔹"
                cor = discord.Color.blue()

            embed.add_field(
                name=f"{medalha} {n}º: {user.name}",
                value=f"{creditos} créditos",
                inline=False
            )

        # Adiciona um rodapé
        embed.set_footer(text="Parabéns aos melhores!")

        await ctx.send(embed=embed)
    else:
        await ctx.send('Ocorreu um erro inesperado ao tentar rankear os usuários. Tente novamente mais tarde.')


@client.command(name="admfunctiondeposit")
async def deposit(ctx, user_id, n):

    if ctx.author.id == 377217614520385536:
        credits = crud.deposit(user_id, n)
        if credits:
            await ctx.send("command exec")

#@client.command(name="eventoaleatorio", aliases=["randomevent", "event", "evento"])
#async def eventoaleatorio(ctx):
#    user_id = ctx.author.id

#    evento = crud.random_event(user_id)

#    await ctx.send(f"**🎲 Evento aleatório:**\n\n{evento}")

client.run(mykey)
