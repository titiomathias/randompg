# Random Play Game - Discord Bot

<p>
    A bot that randomize RPG magic items for players. The users have a limit of 2 items/curiosities for day. The <b>items list aren't available on github</b>.
</p>

<br>

<img src="https://i.imgur.com/3WuQXPc.png">

<br>

<p>Commands list:</p>
<ul>
    <li><code>!ola</code> - Me cumprimenta. / Greets me.</li>
    <li><code>!ajuda</code> ou <code>!help</code> - Explica o que eu sou e como você pode me usar. / Explains what I am and how you can use me.</li>
    <li><code>!comandos</code> - Mostra a lista de comandos disponíveis. / Shows the list of available commands.</li>
    <li><code>!item</code> - Gera um item aleatório para você. / Generates a random item for you.</li>
    <li><code>!mochila</code> - Lista os itens na mochila do usuário. / Lists the items in the user's backpack.</li>
    <li><code>!descartar [numero]</code> - Descarta um item da sua mochila de acordo com seu índice. Exemplo: <code>!descartar 1</code>  
        / Discards an item from your backpack based on its index. Example: <code>!descartar 1</code></li>
    <li><code>!troca [numero] @usuario [numero]</code> - Troca um item de sua mochila com o de outro usuário.  
        Exemplo: <code>!troca 1 @fulano 2</code>  
        / Trades an item from your backpack with another user's item. Example: <code>!troca 1 @user 2</code>  
        (this command requests to trade your item number 1 for item number 2 of the mentioned user)</li>
    <li>
        <code>!creditos</code> - Mostra os créditos do usuário e sua mecânica. / <code>!credits</code> - Show user credits and your working.
    </li>
    <li>
        <code>!melhorarmochila</code> - Aumenta a mochila em 1 espaço em troca de 2 créditos do usuário. / <code>!improvebag</code> - Improve bag 1 slots for 2 user credits.
    </li>
    <li>
        <code>!apostar [creditos} @usuario</code> - Aposta um número de créditos na roleta com outro usuário. / <code>!bet [credits} @user</code> - Bets a number of credits in roulette with another user.
    </li>

</ul>

<br>

<p><b>Technical Details:</b></p>
<ul>
    <li>
        Application: <a href="https://www.python.org/downloads/release/python-3128/">Python v3.12.8</a>.
    </li>
    <li>
        Database: <a href="https://docs.python.org/3/library/sqlite3.html">Sqlite3 v3.13.2</a> (In Dev)
    </li>
    <li>
        All requirements and libs in <code>requirements.txt</code>.
    </li>
</ul>