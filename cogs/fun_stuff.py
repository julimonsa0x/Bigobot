# Original author AlexFlipnote / discord_bot.py
# Modified and added stuff by me

import random
import discord
import asyncio
import aiohttp
from discord.ext.commands.core import command
import requests
import json
from datetime import datetime

from io import BytesIO
from discord.ext import commands
from apis import permissions
from databases import ballresponse
import apis.tuning
from apis.functions import printt, typing_sleep, throw_error
from apis.listas import (brawlers, 
                    campeones, 
                    images, 
                    trivias, 
                    trivia_accept, 
                    trivia_decline, 
                    willyooc,
                    roasts)



class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de fun_stuff listo")
    

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consulta 8ball para recibir una respuesta """
        answer = random.choice(ballresponse)
        await typing_sleep(ctx)
        await ctx.send(f"🎱 **Pregunta:** {question}\n**Respuesta:** {answer}")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def pato(self, ctx):
        """ Manda una foto de patos random"""
        r = requests.get('https://random-d.uk/api/v1/random')
        duck_url = r.json()["url"]
        embed = discord.Embed(color = discord.Colour.dark_gold())
        embed.set_image(url = duck_url)
        await ctx.message.delete()
        await typing_sleep(ctx)
        await ctx.send(embed = embed)
        print(f"cmdPato||         {ctx.author.name} pidio una foto de patos")

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cafe(self, ctx):
        """ Manda una foto de cafe random """
        r = requests.get('https://coffee.alexflipnote.dev/random.json')
        coffe_url = r.json()["file"]
        embed = discord.Embed(color = discord.Colour.dark_gold())
        embed.set_image(url = coffe_url)
        await typing_sleep(ctx)
        await ctx.send(embed = embed)
        print(f"cmdCafe||         {ctx.author.name} pidio una foto de cafes")

    @commands.command(aliases=["flip", "coin", "tossacoin", "flipcoin", "caracruz"])
    async def coinflip(self, ctx):
        """ Coinflip! / Cara o cruz, ideal para decisiones de turnos!"""
        # head and tails in english!
        coinsides = ["Cara", "Cruz"]
        await typing_sleep(ctx)
        await ctx.send(f"**{ctx.author.name}** tiro una moneda y toco **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press #F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"por:\n `**{text}**` " if text else ""
        await typing_sleep(ctx)
        await ctx.message.delete()
        await ctx.send(f"**{ctx.author.name}** le ha pagado respetos {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def definir(self, ctx, *search: commands.clean_content):
        """ Encuentra la mejor definicion para tus palabras """
        async with ctx.channel.typing():
            try:
                r = requests.get(f"https://api.urbandictionary.com/v0/define?term={search}").json()
            except Exception as e:
                await typing_sleep(ctx)
                await ctx.send(f"Exception: {e}. Urban API returned invalid data... might be down atm.")

            if not r:
                await typing_sleep(ctx)
                return await ctx.send("Hubo un error...")

            if not len(r["list"]):
                await typing_sleep(ctx)
                return await ctx.send(f"No pude encontrar una definicion para {search}...")

            result = sorted(r["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            await typing_sleep(ctx)
            await ctx.send(f"📚 Definicion para: **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """
        EN: Everything you type after reverse will of course, be reversed
        ES: Lo que escribas se da vuelta, aunque es recomendable usar #tunear 4 <tu_texto>
        Para mas informacion utiliza **#help tunear** 
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await typing_sleep(ctx)
        await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def rating(self, ctx, *, thing: commands.clean_content):
        """ Le doy un rating a lo que sea... """
        rate_amount = random.uniform(0.0, 100.0)
        await typing_sleep(ctx)
        await ctx.send(f"A `{thing}` le doy un... **{round(rate_amount, 2)} / 100**")
        print(f"cmdRating||        el bigobot le dio un rating de {rate_amount} a {thing}")

    @commands.command()
    async def birra(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Toma una cerveza con alguien! 🍻, la sintaxis es #birra <@usuario> <razon> """
        
        # if its yourself or theres no mention
        if not user or user.id == ctx.author.id:
            await typing_sleep(ctx)
            return await ctx.send(f"**{ctx.author.name}**: paaaarty! 🎉 🍺")
        
        # if you mention the bot
        if user.id == self.bot.user.id:
            await typing_sleep(ctx)
            return await ctx.send("Tomare birra contigo 🍻")
        
        # if ??? XDLOL 
        if user.bot:
            await typing_sleep(ctx)
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, acabas de recibir una invitacion 🍺  de parte de: **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Razon:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await typing_sleep(ctx)
            await msg.edit(content=f"**{user.name}** junto a **{ctx.author.name}** estan disfrutando unas birritas 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await typing_sleep(ctx)
            await ctx.send(f"Al parecer **{user.name}** no tenia interes en tomar una pinta con **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, if bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, acabas de recibir una invitacion 🍺  de parte de: **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Razon:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 25:
            emoji = "❤"
        elif hot > 50:
            emoji = "💖"
        elif hot > 75:
            emoji = "💞"
        else:
            emoji = "💔"
        await typing_sleep(ctx)
        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Gira la maquina tragaperras, util para decisiones de turnos """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} Perfecto, Tu ganas! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} Casi perfecto, pero aun ganas! 🎉")
        else:
            await ctx.send(f"{slotmachine} No hay match, no ganas... 😢")

    @commands.command(aliases=['dices','roll_dices','tirardados','tirar_dados','lanzardados'])
    async def dados(self, ctx, user=None, number1=1, number2=6):
        '''
        Tira un dado, recomendado para decidir turnos...
        argumento user opcional.
        argumento number1 y number2 por defecto 1 y 6 pero son modificables
        '''
        if user is None:
            user = ctx.author
        number = random.randint(number1, number2)
        dadosEmbed = discord.Embed(
            title="#Dados",
            description=f"Toco el numero {number} para {user.mention}")
        dadosEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/842125661585276978/1f3b2.png") # dado.png

        await typing_sleep(ctx)
        await ctx.send(embed=dadosEmbed)
        print(f"cmdDados||   A {ctx.author.name} le tocó el dado {number}")

    @commands.command(aliases=['brawler_random','brawler'])
    async def randombrawl(self, ctx):
        '''Brawler random, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
        await ctx.send("3...", delete_after=45.0)
        await asyncio.sleep(0.5)
        await ctx.send("2...", delete_after=45.0)
        await asyncio.sleep(0.5)
        await ctx.send("1...", delete_after=45.0)
        await asyncio.sleep(0.5)
        
        embed = discord.Embed(color = discord.Colour.orange())
        randomBrawl = random.choice(brawlers)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/797964925980246066/c849eb95e858ce12cdc86cb6d4ecb36b00bbdfaa96d9973852d1421661f5aec5200.png")
        embed.add_field(name= "Brawler Aleatorio: ", value=f"{randomBrawl}")
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Le tocó a {ctx.author}")
        
        await typing_sleep(ctx)
        await ctx.send(embed=embed, delete_after=200.0)
        print(f"cmdRandomBrawl|| Brawler aleatorio enviado, en la lista hay: {str(len(brawlers))}")

    @commands.command(aliases=['lolchamp','randomlol','lol','campeonrandom'])
    async def randomchamp(self, ctx):
        '''Campeon random de lol, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
        await ctx.send("3...", delete_after=45.0)
        await asyncio.sleep(0.5)
        await ctx.send("2...", delete_after=45.0)
        await asyncio.sleep(0.5)
        await ctx.send("1...", delete_after=45.0)
        await asyncio.sleep(0.5)

        random_int = random.randint(0, 154)

        with open("databases/lol_champions.json", "r", encoding='utf8') as f:
            key = json.load(f)
            randomCham = key["campeones"][random_int]["campeon"]
            randomSubt = key["campeones"][random_int]["frase"]
            randomImag = key["campeones"][random_int]["icon"]
            
        embed3 = discord.Embed(title=randomCham,description=randomSubt,color = discord.Colour.orange())
        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/797965087767396442/lol-icon.png")
        embed3.set_image(url=randomImag)
        embed3.set_footer(icon_url = ctx.author.avatar_url, text = f"Le tocó a {ctx.author}") 
        
        await typing_sleep(ctx)
        await ctx.send(embed=embed3, delete_after=200.0)
        print(f"cmdRandomChamp|| Campeón aleatorio enviado, en la lista hay: {str(len(campeones))}")

    @commands.command()
    async def meme(self, ctx):
        '''Memes randoms, a quien no le gustan los memes...'''
        embedMeme = discord.Embed(color = discord.Colour.red(), timestamp=datetime.utcnow())
        random_link = random.choice(images)
        if (
                random_link.startswith('https://video.twimg.com/ext_tw_video/') or 
                random_link.startswith('https://imgur') or 
                random_link.startswith('https://www.youtube:') or
                random_link.startswith('https://i.imgur') or 
                random_link.startswith('https://youtu')
            ):
            await typing_sleep(ctx)
            await ctx.send(f"{random_link}")
            print(f'cmdMeme||         Meme enviado a {ctx.author.name}')

        else:
            embedMeme.set_image(url = random_link)
            await typing_sleep(ctx)
            await ctx.send(embed=f"{embedMeme}")
            print(f'cmdMeme||         Meme enviado a {ctx.author.name}')

    @commands.command()
    #@commands.has_permissions(kick_members=True)
    #for if you wanna limit this command usage and prevent spamming
    async def contar(self, ctx, number: int, intervalo):
        '''
        El bot cuenta hasta un numero dado, puede ser re carnasa...
        Los mensajes luego de 30 segundos se autoeliminan...
        Argumento <number>: int | **numero hasta el cual contar**. 
        Argumento <intervalo>: float | **velocidad a la cual contar en segundos**.
        Ejemplo: `#contar 50 0.5` -> el bot contara hasta el 50 a velocidad de 1/2 segundo
        '''
        i = 1
        while i <= number:
            async with ctx.typing():    
                await asyncio.sleep(float(intervalo))
                await ctx.send(f"{i}", delete_after=30.0)
                i += 1

    @commands.command()
    async def trivia(self, ctx):
        '''It's trivia time!!!'''
        await typing_sleep(ctx)
        msg = await ctx.channel.send(random.choice(trivias))
        await msg.add_reaction(u"\u2705")
        await msg.add_reaction(u"\U0001F6AB")

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=15.0)  
            await asyncio.sleep(1)
            await ctx.channel.send("3...", delete_after=15.0)
            await asyncio.sleep(1)
            await ctx.channel.send("2...", delete_after=15.0)
            await asyncio.sleep(1)
            await ctx.channel.send("1...", delete_after=15.0)

        except asyncio.TimeoutError:
            await typing_sleep(ctx)
            await ctx.channel.send("Che me ignoraron la trivia (▀̿Ĺ̯▀̿ ̿) ", delete_after=35.0)

        else:
            if reaction.emoji ==  u"\u2705":
                await typing_sleep(ctx)
                await ctx.message.delete()
                await ctx.channel.send(random.choice(trivia_accept), delete_after=120.0)

            else:
                await typing_sleep(ctx)
                await ctx.message.delete()
                await ctx.channel.send(random.choice(trivia_decline), delete_after=120.0)

    @commands.command()
    async def willy(self, ctx):
        '''videos del willy out of context, un cago de risa...'''
        await typing_sleep(ctx)
        await ctx.send(random.choice(willyooc))
        print(f'cmdWilly||      Willy OOC enviado a {ctx.author.name}')

    @commands.command(aliases=['tunearletras','messletters','changefont'])
    async def tunear(self, ctx, orden: int, *, args=None,):
        '''
        Tunea un texto, la sintaxis es #[tunear] <orden> <el_texto_que_quieras_tunear>. 
        El orden debe ser un numero del 1 al 7 (distintas fuentes)
        • Orden 1: Letras Arabes creo.
        • Orden 2: Letras cursiva solo minuscula
        • Orden 3: Alfabeto en cursiva completo
        • Orden 4: Letras invertidas 
        • Orden 5: Letras minusculas italica 
        • Orden 6: Letras mayusculas grandes
        • Orden 7: Letras dentro de circulos
        • Orden 8: Alfabeto Math Serif Bold
        '''
        
        try:
            if args != None:
                myThiccString = apis.tuning.tunear(args.replace("#tunear", ""), orden)
                await typing_sleep(ctx)
                await ctx.send(myThiccString)
                print(f"cmdTunear1||        {ctx.author.name} tuneó un texto")

            elif args is None and orden is None:
                await typing_sleep(ctx)    
                await ctx.send("Seguido del comando debes introducir un orden (1 a 6) seguido del texto a tunear", delete_after=60.0)
                await ctx.send("A modo de ejemplo: **#tunear 4 textodepruebacopipedro**", delete_after=60.0)
                print(f"cmdTunear||        {ctx.author.name} falló al tunear un texto")

        except Exception as e:
            if isinstance(e, commands.MissingRequiredArgument):
                await typing_sleep(ctx)
                await ctx.send("Debes seguir la sintáxis #tunear <orden>, prueba con #help tunear para mas info.", delete_after=130.0)
                await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y para ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**", delete_after=150.0)
            else:
                await typing_sleep(ctx)
                await throw_error(ctx=ctx, e=e)


    ##############
    ############## COMANDOS DE VIDEOS RANDOMS 
    #---> Lamar roasts Franklin vid <---
    @commands.command()
    async def roast(self, ctx):
        '''Lamar roasts Franklin trending videos...'''
        await typing_sleep(ctx)
        await ctx.send(random.choice(roasts))
        print(f'cmdRoast||      Lamar v Franklin enviado a {ctx.author.name}')

    #---> LocuraBailandoSinPantalones vid <---
    @commands.command()
    async def locurabailando(self, ctx):
        '''Locura bailando...'''
        await ctx.send("http://youtu.be/tvvGVZpnOMA")
        print(f'cmdLocura...||  Video del locurabailando a {ctx.author.name}')

    #---> gordoPistero vid <---
    @commands.command()
    async def pistero(self, ctx):
        '''Gordo pistero'''
        await ctx.send("https://cdn.discordapp.com/attachments/793309880861458473/850956075892998175/gordo_pistero_en_moto_con_cancion_brasilena.mp4")
        print(f'cmdLocura...|| Video del gordopistero enviado a {ctx.author.name}')

    #---> TADEO 1hs EN WHEELIE vid <---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def tadeo(self, ctx):
        '''Video del Tadeo moto moto 1 hora en bucle'''
        await ctx.send("https://youtu.be/ffoXJhzwcHQ")

    #---> MATEUS505 GALO SNIPER vid <---
    @commands.command()
    async def galosniper(self, ctx):
        ''' PLEASE DO NOT ! '''
        embedGalo = discord.Embed(
            title="galo sniper",
            description="galo sniper",
            color=discord.Color.red()
        )
        embedGalo.add_field(name="10 FATOS SOBRE MATEUS505 CARVALHO DO SANTOS", value=None, inline=False)
        embedGalo.add_field(name="FATO 1: ¿NOME DO MATEUS 505?", value="MATEO 505 CARVALHO DO SANTOS")
        embedGalo.add_field(name="FATO 2: ¿QUANTOS ANOS VOCE TEM?", value="20 ANOS", inline=False)
        embedGalo.add_field(name="FATO 3: ¿QUAL SEU MEME FAVORITO?", value="GALO SNIPER")
        embedGalo.add_field(name="FATO 4: ¿QUAL SEU PERSONAGEM FAVORITO?", value="GALO SNIPER", inline=False)
        embedGalo.add_field(name="FATO 5: ¿QUAL SEU FILME FAVORITO", value="GALO SNIPER AMERICANO")
        embedGalo.add_field(name="FATO 6: ¿QUAL SEU ANIME FAVORITO", value="GALO SNIPER SHIPPUDEN", inline=False)
        embedGalo.add_field(name="FATO 7: ¿QUAL SUA COR FAVORITA", value="BRANCO do GALO SNIPER")
        embedGalo.add_field(name="FATO 8: ¿QUAL o SEU INSTAGRAM", value="GALO SNIPER", inline=False)
        embedGalo.add_field(name="FATO 9: ¿QUAL SEU MELHOR AMIGO DA INFANCIA?", value="GALO SNIPER")
        embedGalo.add_field(name="FATO 10: ¿QUAL SEU ANIMAL FAVORITO?", value="Spoky ???? SNIPER", inline=False)
        await ctx.send(embed=embedGalo)
        await ctx.send("https://www.youtube.com/watch?v=cwiVlpW7-XM")
        print(f'cmdGaloSniper||   Video del GALOSNIPER enviado a {ctx.author.name} XD')
    ############## FIN DE VIDEOS DE COMANDOS RANDOMS
    ##############


def setup(bot):
    bot.add_cog(FunCommands(bot))