import asyncio
import os
from datetime import datetime
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
    last_modified = os.path.getmtime(__file__)  # __file__ pega o caminho deste arquivo
    last_update = datetime.fromtimestamp(last_modified).strftime("%d/%m/%Y - %H:%M")
    
    print(f'Bot is working. Last update -> {last_update}')


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
    embed = discord.Embed(
        title="🎲 **AJUDA DO RANDOM**",
        description="Olá! Eu sou o **Random**, seu companheiro de aventuras aleatórias! "
                   "Aqui está tudo que você precisa saber para me usar:",
        color=0x3498db 
    )

    embed.set_thumbnail(url="https://i.imgur.com/CpmmKLI.png")

    # Comandos principais
    embed.add_field(
        name="🎁 **COMANDOS BÁSICOS**",
        value=(
            "```\n"
            "!item       → Gera um item aleatório para sua mochila.\n"
            "!mochila    → Mostra todos os itens que você coletou.\n"
            "!descartar  → Remove um item da sua mochila.\n"
            "!trocar     → Substitui um item por outro aleatório.\n"
            "!melhorar   → Expande sua mochila para guardar mais itens.\n"
            "!enigma     → Mostra os gênios que resolveram o enigma supremo.\n"
            "```"
        ),
        inline=False
    )

    # Como funciona
    embed.add_field(
        name="📦 **SOBRE A MOCHILA**",
        value=(
            "• Você começa com **10 espaços** na mochila.\n"
            "• Use `!melhorar` para aumentar sua capacidade.\n"
            "• Itens duplicados? Use `!trocar` ou `!descartar`.\n"
            "• Quer um desafio? Tente resolver o `!enigma`!"
        ),
        inline=False
    )

    # Footer com dica
    embed.set_footer(
        text="Dica: Digite !comandos para ver a lista completa de comandos.",
        icon_url="https://i.imgur.com/CpmmKLI.png" 
    )

    await ctx.send(embed=embed)

# comandos
@client.command(name='comandos', aliases=['commands'])
async def comandos(ctx):
    embed = discord.Embed(
        title="📜 **LISTA DE COMANDOS DO RANDOM**",
        description="Olá! Eu sou o **Random**, seu companheiro de aventuras aleatórias! "
                   "Aqui está tudo o que você pode fazer comigo:",
        color=0x9B59B6
    )

    embed.set_thumbnail(url="https://i.imgur.com/CpmmKLI.png")

    embed.add_field(
        name="🔹 **INTERAÇÃO**",
        value=(
            "```\n"
            "!ola        → Cumprimenta o bot\n"
            "!ajuda      → Explica como usar o bot\n"
            "!comandos   → Mostra esta lista\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="🎁 **ITENS & MOCHILA**",
        value=(
            "```\n"
            "!item              → Gera um item aleatório\n"
            "!mochila           → Mostra seus itens\n"
            "!descartar [n]     → Descarta o item nº [n]\n"
            "!troca [n] @user [n] → Troca itens com outro jogador\n"
            "!melhorarmochila [n] → Expande sua mochila (+2 créditos/espaço)\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="💰 **CRÉDITOS & RANKING**",
        value=(
            "```\n"
            "!creditos       → Mostra seus créditos\n"
            "!rank           → Top 10 usuários\n"
            "!apostar [n] @user → Aposta créditos na roleta\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="🧩 **DESAFIO**",
        value=(
            "```\n"
            "!enigma → Mostra os gênios que resolveram o desafio supremo\n"
            "```"
        ),
        inline=False
    )

    embed.add_field(
        name="📌 **EXEMPLOS PRÁTICOS**",
        value=(
            "• `!descartar 2` → Descarta o 2º item da mochila\n"
            "• `!troca 3 @Jogador 1` → Oferece seu item 3 pelo item 1 do @Jogador\n"
            "• `!melhorarmochila 5` → +5 espaços (custa 10 créditos)\n"
            "• `!apostar 10 @Rival` → Aposta 10 créditos contra @Rival"
        ),
        inline=False
    )

    embed.set_footer(
        text="Dica: Use !ajuda para explicações detalhadas de cada comando.",
        icon_url="https://i.imgur.com/CpmmKLI.png"
    )

    await ctx.send(embed=embed)

# Open Bag
@client.command(name='abrirmochila', aliases=['mochila', 'bag', 'openbag'])
async def abrirmochila(ctx):
    user_id = ctx.author.id
    bag, slots = crud.open_bag(user_id)
    
    if not bag:
        embed = discord.Embed(
            title="📦 Mochila Vazia",
            description="Sua mochila está vazia! Use o comando **`!item`** para coletar itens.",
            color=0xff0000  # Vermelho (pode mudar para qualquer cor em HEX)
        )
        return await ctx.send(embed=embed)

    # Configurações da paginação
    itens_por_pagina = 10
    paginas = [bag[i:i + itens_por_pagina] for i in range(0, len(bag), itens_por_pagina)]
    pagina_atual = 0
    total_paginas = len(paginas)

    # Função para criar o Embed da página atual
    def criar_embed(pagina_idx):
        pagina = paginas[pagina_idx]
        embed = discord.Embed(
            title=f"🎒 Mochila de {ctx.author.display_name}",
            description=f"**Espaços:** `{len(bag)}/{slots}`\n**Página:** `{pagina_idx + 1}/{total_paginas}`",
            color=0x00ff00  # Verde (personalize!)
        )
        
        # Adiciona um thumbnail (opcional)
        embed.set_thumbnail(url=ctx.author.avatar.url)
        
        # Adiciona os itens em campos (organizados)
        itens_str = ""
        inicio = pagina_idx * itens_por_pagina + 1
        for n, item in enumerate(pagina, start=inicio):
            itens_str += f"`{n}.` {item}\n"
        
        embed.add_field(
            name="📋 Itens:",
            value=itens_str if itens_str else "*Nenhum item nesta página*",
            inline=False
        )
        
        # Rodapé (opcional)
        embed.set_footer(text="Navegue usando as reações abaixo →")
        return embed

    # Envia a mensagem inicial
    mensagem = await ctx.send(embed=criar_embed(pagina_atual))

    # Adiciona navegação por reações (se houver mais de uma página)
    if total_paginas > 1:
        await mensagem.add_reaction('⬅️')
        await mensagem.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == mensagem.id and str(reaction.emoji) in ['⬅️', '➡️']

        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                
                if str(reaction.emoji) == '➡️' and pagina_atual < total_paginas - 1:
                    pagina_atual += 1
                elif str(reaction.emoji) == '⬅️' and pagina_atual > 0:
                    pagina_atual -= 1
                
                await mensagem.edit(embed=criar_embed(pagina_atual))
                try:
                    await reaction.remove(user)
                except discord.errors.Forbidden:
                    pass  # Ignora erro de permissão
                
            except asyncio.TimeoutError:
                try:
                    await mensagem.clear_reactions()
                except discord.errors.Forbidden:
                    pass
                break

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


@client.command(name="aposta", aliases=["apostar", "gambly", "fazeraposta", "bet", "bets"])
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
        if aposta[8] == 2:
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


@client.command(name="enigma", aliases=["enigmatas", "Enigma"])
async def enigma(ctx):
    primeiro_lugar_id = 285508502057779200
    segundo_lugar_id = 567404024853299226 

    primeiro_lugar = await client.fetch_user(primeiro_lugar_id)
    segundo_lugar = await client.fetch_user(segundo_lugar_id)

    embed = discord.Embed(
        title="🏆 Pódio do Enigma do Baú",
        description="**Estes são os únicos que decifraram o mistério:**",
        color=0xFFD700 
    )

    embed.add_field(
        name="🥇 1º Lugar - O Mestre dos Enigmas",
        value=f"👑 **{primeiro_lugar.display_name}**\n*'O Homem Mais Inteligente do Universo'*",
        inline=False
    )
    embed.set_thumbnail(url=primeiro_lugar.avatar.url)

    embed.add_field(
        name="🥈 2º Lugar - O Gênio Incompreendido",
        value=f"🔮 **{segundo_lugar.display_name}**\n*'O Segundo Homem Mais Inteligente do Universo'*",
        inline=False
    )

    embed.add_field(
        name="🥉 3º Lugar - Vago",
        value="*Este lugar aguarda o próximo gênio...*",
        inline=False
    )

    embed.set_footer(text="Será que alguém mais conseguirá resolver o próximo enigma?")

    await ctx.send(embed=embed)

#@client.command(name="eventoaleatorio", aliases=["randomevent", "event", "evento"])
#async def eventoaleatorio(ctx):
#    user_id = ctx.author.id

#    evento = crud.random_event(user_id)

#    await ctx.send(f"**🎲 Evento aleatório:**\n\n{evento}")

client.run(mykey)
