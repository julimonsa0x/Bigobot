import asyncio
import discord
from discord.ext.commands import Bot

#---------------------------------->>>>> Tic Tac Toe Game
bot = Bot(command_prefix="#")

BLANK = 'BLANK'
pos_1 = 0
pos_2 = 1
pos_3 = 2
pos_4 = 3
pos_5 = 4
pos_6 = 5
pos_7 = 6 
pos_8 = 7
pos_9 = 8
REACTIONEMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🚫"]

#------------------------------------>>>> RPS / PPT BEGINNING
async def ppt(ctx, bot, member:discord.Member=None):
    '''Piedra papel o tijeras'''

    if member == ctx.author and member != None:
        await ctx.send("No puedes jugar contra ti mismo")
        return
    elif member == None:
        await ctx.send("Seguido del comando debes @mencionar a tu contrincante!")

    author = ctx.author
    async with ctx.typing():    
        await asyncio.sleep(0.5)
        await ctx.send(f"{ctx.author.name} y {member.name}, recuerden que se juega a traves de Mensajes Directos...")


    msg1 = await member.send(f" {author} te ha enfrentado a un piedra papel o tijeras, si aceptas reacciona con :white_check_mark: a este mensaje, caso contrario reacciona con :negative_squared_cross_mark: ...")
    await msg1.add_reaction('✅')
    await msg1.add_reaction('❎')
    
    msg2 = await author.send(f" Desafiaste a {member} a un piedra papel o tijeras, ahora espera si {member} acepta o reachaza")
    def check(reaction, user):
        return user == member and str(reaction.emoji) == "✅" or "❎" and reaction.message.id == msg1.id

    reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)

    # >ACEPTO<
    if str(reaction.emoji) =="✅":
        await msg1.delete()
        await author.send(f"{member} aceptó tu desafio, esperando a su elección ") 
        members_choice_1 = await member.send(f" Aceptaste la invitación de {author}, reacciona 🥌 para **roca**, ✂ para **tijeras** o 📰 para **papel**")
        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🥌" or "✂" or "📰"  and reaction.message.id == members_choice_1.id

        reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)

    # --PIEDRA
    if str(reaction.emoji) == "🥌":
        author_choice_1 = await author.send(f"{member} ya hizo su elección, ahora tu turno , reacciona 🥌 para **roca**, ✂ para **tijeras** o  📰 para **papel**")
        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🥌" or "✂" or "📰"  and reaction.message.id == author_choice_1.id

        reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
        if str(reaction.emoji) == "🥌":
            await author.send(f"Es un empate, ambos eligieron **roca**")
            await member.send(f"Es un empate, ambos eligieron **roca**")
            return

        if str(reaction.emoji) == "📰":
            await author.send(f"Tu ganas, elegiste **papel** y {member} eligió **piedra**")
            await member.send(f"Tu pierdes, elegiste **piedra** y {author} eligió **papel**")
            return

        if str(reaction.emoji) == "✂":
            await author.send(f"Tu pierdes, elegiste **tijeras** y {member} eligió **piedra**")
            await member.send(f"Tu ganas, elegiste **piedra** y {author} eligió **tijeras** ")
            return

    # --TIJERA
    if str(reaction.emoji) == "✂":
        author_choice_2 = await author.send(f"{member} ya hizo su elección, ahora tu turno, 🥌 para **piedra**, ✂ para **tijeras** o 📰 para **papel**")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🥌" or "✂" or "📰" and reaction.message.id == author_choice_2.id

        reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)
        if str(reaction.emoji) == "🥌":
            await author.send(f"Tu ganas, elegiste **piedra** y {member} eligió **tijeras**!")
            await member.send(f"Tu pierdes, elegiste **tijeras** y {author} eligió**piedra**!")
            return
        if str(reaction.emoji) == "📰":
            await author.send(f"Tu pierdes, elegiste **papel** y {member} eligió **tijeras**!")
            await member.send(f"Tu ganas, elegiste **tijeras** y {author} eligió **papel**!")
            return
        if str(reaction.emoji) == "✂":
            await author.send(f"Es un empate, ambos eligieron **tijeras**!")
            await member.send(f"Es un empate, ambos eligieron **tijeras**!")
            return

    # --PAPEL
    if str(reaction.emoji) == "📰":
        author_choice_3 = await author.send(f"{member} ya hizo su elección, ahora tu turno: 🥌 para **piedra**, ✂ para **tijeras** o 📰 para **papel**!")

        def check(reaction, user):
            return user == member and str(reaction.emoji) == "🥌" or "✂" or "📰" and reaction.message.id == author_choice_3.id

        reaction, user = await bot.wait_for('reaction_add', timeout=None, check=check)

        if str(reaction.emoji) == "🥌":
            await author.send(f"Tu pierdes, elegiste **piedra** y  {member} eligió **papel**!")
            await member.send(f"Tu ganas, elegiste **papel** y {author} eligió **piedra**!")
            return
        if str(reaction.emoji) == "📰":
            await author.send(f"Es un empate, ambos eligieron **papel**")
            await member.send(f"Es un empate, ambos eligieron **papel**")
            return
        if str(reaction.emoji) == "✂":
            await author.send(f"Tu ganas, elegiste **tijeras** y {member} eligió **papel**!")
            await member.send(f"Tu pierdes, elegiste **papel** y {author} eligió **tijeras**!")
            return

    # >NEGACION<
    if str(reaction.emoji) =="❎":
        await msg1.delete()
        w = await author.send(f"{member} rechazó tu batalla ")
        await asyncio.sleep(15)
        await w.delete()
        return
#------------------------------------>>>> RPS ENDING

async def LoadGames(ctx, bot):
    embed = discord.Embed(
        title = "Escoje un juego",
        description = "1️⃣: Ta te ti \n\n 2️⃣: Piedra papel o tijeras \n\n 3️⃣: Coming soon..."
    )
    await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=embed)

    await msg.add_reaction('1️⃣')
    await msg.add_reaction('2️⃣')
    await msg.add_reaction('3️⃣')
    await msg.add_reaction('4️⃣')

    def checkReaction(reaction, user):
        return user != bot.user and (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣')

    reaction, user = await bot.wait_for("reaction_add", timeout=25.0, check=checkReaction)
    if str(reaction.emoji) == '1️⃣':
        await ticTacToe(ctx, bot)
        pass
    elif str(reaction.emoji) == '2️⃣':
        await ctx.send("para jugar al piedra papel o tijeras, debes usar el comando #ppt aparte y @mencionar contra quien quieres jugar...")
        pass
    elif str(reaction.emoji) == '3️⃣':
        await ctx.send("Proximamente...")
        pass
    elif str(reaction.emoji) == '4️⃣':
        await ctx.send("copipedro <:copi:770818273217609758>")
        pass
    else:
        await ctx.send("No obtuve respuesta, escribe el comando de vuelta si deseas jugar...", delete_after=10)


#---------------------------------->>>>> Tic Tac Toe Game BEGINNING
async def ticTacToe(ctx, bot):
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🚫"]
    board = [BLANK, BLANK, BLANK,
            BLANK, BLANK, BLANK,
            BLANK, BLANK, BLANK]

    currentPlayer = 2
    player_1 = await getUserChar(ctx, bot, currentPlayer - 1)
    player_2 = await getUserChar(ctx, bot, currentPlayer)

    await ctx.channel.purge(limit=3)

    def checkNotBot(reaction, user):
        return user != bot.user

    
    turn=1
    while checkWin(player_1, player_2, board) == BLANK and turn <= 9:
        await ctx.send(f"Turno del jugador {currentPlayer % 2 + 1}")
        msg = await ctx.send(printBoard(player_1, player_2, board))
        for i in range(len(emojis)):
            await msg.add_reaction(emojis[i])

        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
        
        print(str(reaction.emoji))
        
        if str(reaction.emoji) == "🚫":
            print("Cerrado")
            turn = 100
            await ctx.channel.purge(limit=2)

        else:
            if currentPlayer % 2 == 0:           # player 1 turn
                makeMove(reaction.emoji, emojis, player_1, board)
            else:                                # player 2 turn
                makeMove(reaction.emoji, emojis, player_2, board)

            await ctx.channel.purge(limit=2)

        winner = checkWin(player_1, player_2, board)
        if winner != BLANK:
            await ctx.send(f'El ganador es el jugador {currentPlayer % 2 + 1}! \n Te gustaria jugar de nuevo?')
            msg = await ctx.send(printBoard(player_1, player_2, board))
            await msg.add_reaction(':white_check_mark:')
            await msg.add_reaction(':x:')
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
            if str(reaction.emoji == ':white_check_mark:'):
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🚫"]
                board = [BLANK, BLANK, BLANK,
                        BLANK, BLANK, BLANK,
                        BLANK, BLANK, BLANK]
                turn = 0
                currentPlayer = 1 
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send('Juego terminado!')

        elif turn >= 9:
            await ctx.send('Es un empate! \nDeseas jugar otra vez?')
            msg = await ctx.send(printBoard(player_1, player_2, board))
            await msg.add_reaction(':white_check_mark:')
            await msg.add_reaction(':x:')
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)
            if str(reaction.emoji == ':white_check_mark:'):
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🚫"]
                board = [BLANK, BLANK, BLANK,
                        BLANK, BLANK, BLANK,
                        BLANK, BLANK, BLANK]
                turn = 0
                currentPlayer = 1 
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send("...")



        currentPlayer += 1
        turn += 1

def makeMove(emoji, emojiList, player, board):
    for index in range(len(REACTIONEMOJI)):
        if REACTIONEMOJI[index] == emoji:
            board[index] = player
            emojiList.remove(emoji)
            break


def checkWin(player1, player2, board):
    # Horizontal lines check --------------------------------------------->>>
    lineHOne = checkDirection(pos_1, pos_2, pos_3, player1, player2, board)
    if lineHOne != BLANK:
        return lineHOne
    lineHTwo = checkDirection(pos_4, pos_5, pos_6, player1, player2, board)
    if lineHTwo != BLANK:
        return lineHTwo
    lineHThree = checkDirection(pos_7, pos_8, pos_9, player1, player2, board)
    if lineHThree != BLANK:
        return lineHThree
    # Vertical lines check ------------------------------------------------>>>
    lineVOne = checkDirection(pos_1, pos_4, pos_7, player1, player2, board)
    if lineVOne != BLANK:
        return lineVOne
    lineVTwo = checkDirection(pos_2, pos_5, pos_8, player1, player2, board)
    if lineVTwo != BLANK:
        return lineVTwo
    lineVThree = checkDirection(pos_3, pos_6, pos_9, player1, player2, board)
    if lineVThree != BLANK:
        return lineVThree
    # Diagonal lines check ------------------------------------------------>>>
    lineDOne = checkDirection(pos_1, pos_5, pos_9, player1, player2, board)
    if lineDOne != BLANK:
        return lineDOne
    lineDTwo = checkDirection(pos_3, pos_5, pos_7, player1, player2, board)
    if lineDTwo != BLANK:
        return lineDTwo
    return BLANK
    

def checkDirection(pos1, pos2, pos3, player1, player2, board):
    if (board[pos1] == board[pos2] == board[pos3]) and (board[pos3] != BLANK):
        if board[pos1] == player1:
            return player1
        elif board[pos1] == player2:
            return player2
    else:
        return BLANK


def printBoard(player1, player2, board):
    blank_char = ":white_large_square:"
    boardMessage = ""
    tile = 1
    for x in range(len(board)):
        if board[x] == BLANK:
            if tile % 3 == 0:
                boardMessage = boardMessage + blank_char + '\n'
            else:
                boardMessage = boardMessage + blank_char
        elif board[x] == player1:
            if tile % 3 == 0:
                boardMessage = boardMessage + player1 + '\n'
            else:
                boardMessage = boardMessage + player1
        elif board[x] == player2:
            if tile % 3 == 0:
                boardMessage = boardMessage + player2 + '\n'
            else:
                boardMessage = boardMessage + player2
        tile += 1
    return boardMessage


async def getUserChar(ctx, bot, currentPlayer):
    await ctx.send("Jugador " + str(currentPlayer) + "escoje tu personaje! (reacciona con un emote)")

    def checkNotBot(reaction, user):
        return user != bot.user

    reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=checkNotBot)

    return str(reaction.emoji)
#------------------------------------->>>>> Tic Tac Toe Game ENDING