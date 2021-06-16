# Original author AlexFlipnote / discord_bot.py
# Modified and added stuff by me

import random
import discord
import asyncio
import aiohttp
from discord.ext.commands.core import command
from discord_slash.model import SlashCommandPermissionType
import requests
import json
from datetime import datetime

from io import BytesIO
from discord.ext import commands
from apis import permissions
from databases import ballresponse
import apis.tuning
from apis.functions import printt, throw_error
from apis.listas import (brawlers, 
                    campeones, 
                    images, 
                    trivias, 
                    trivia_accept, 
                    trivia_decline, 
                    willyooc,
                    roasts,
                    brawlers_images)


from discord_slash import cog_ext, SlashContext


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de fun_stuff listo")
    

    @cog_ext.cog_slash(description="Consulta 8ball para recibir una respuesta a una preugnta que escribas")
    async def eightball(self, ctx: SlashContext, *, pregunta):
        answer = random.choice(ballresponse)
        await ctx.send(content=f"🎱 **Pregunta:** {pregunta}\n**Respuesta:** {answer}")

    @cog_ext.cog_slash()
    async def pato(self, ctx: SlashContext):
        """ Manda una foto de patos random"""
        r = requests.get('https://random-d.uk/api/v1/random')
        duck_url = r.json()["url"]
        embed = discord.Embed(color = discord.Colour.dark_gold())
        embed.set_image(url = duck_url)
        await ctx.message.delete()
        await ctx.send(content="pato random", embed = embed)
        print(f"cmdPato||         {ctx.author.name} pidio una foto de patos")

    @cog_ext.cog_slash()
    async def cafe(self, ctx: SlashContext):
        """ Manda una foto de cafe random """
        r = requests.get('https://coffee.alexflipnote.dev/random.json')
        coffe_url = r.json()["file"]
        embed = discord.Embed(color = discord.Colour.dark_gold())
        embed.set_image(url = coffe_url)
        await ctx.send(content="toma un cafe", embed = embed)
        print(f"cmdCafe||         {ctx.author.name} pidio una foto de cafes")

    @cog_ext.cog_slash(description="Tira una moneda y devuelve cara o cruz...")
    async def coinflip(self, ctx: SlashContext):
        # head and tails in english!
        coinsides = ["Cara", "Cruz"]
        embedCoin=discord.Embed(title=f"toco **{random.choice(coinsides)}**!")
        await ctx.send(content=f"**{ctx.author.name}** tiro una moneda", embed=embedCoin)

    @cog_ext.cog_slash(description="paga respetos con un texto opcional.")
    async def f(self, ctx: SlashContext, *, texto=None):
        """ Press #F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"por:\n `**{texto}**` " if texto else ""
        embedF = discord.Embed(title=f"{reason}{random.choice(hearts)}")
        await ctx.message.delete()
        await ctx.send(content=f"**{ctx.author.name}** le ha pagado respetos", embed=embedF)

    @cog_ext.cog_slash(description="busca una definicion para cualquier texto.")
    async def definir(self, ctx: SlashContext, *busqueda):
        """ Encuentra la mejor definicion para tus palabras """
        try:
            r = requests.get(f"https://api.urbandictionary.com/v0/define?term={busqueda}").json()
        except Exception as e:
            await ctx.send(content=f"Exception: {e}. Urban API returned invalid data... might be down atm.")

        if not r:
            return await ctx.send(content="Hubo un error...")

        if not len(r["list"]):
            return await ctx.send(content=f"No pude encontrar una definicion para {busqueda}...")

        result = sorted(r["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

        definition = result["definition"]
        if len(definition) >= 1000:
            definition = definition[:1000]
            definition = definition.rsplit(" ", 1)[0]
            definition += "..."

        await ctx.send(content=f"📚 Definicion para: **{result['word']}**```fix\n{definition}```")

    @cog_ext.cog_slash(description="invierte un texto, aunque es recomendable utilizar #tunear 4 <texto>.")
    async def invierte(self, ctx, *, text: str):
        """
        Lo que escribas se da vuelta, aunque es recomendable usar #tunear 4 <tu_texto>
        Para mas informacion utiliza **#help tunear** 
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @cog_ext.cog_slash(description="Punteo lo que sea")
    async def rating(self, ctx: SlashContext, *, thing):
        """ Le doy un rating a lo que sea... """
        rate_amount = random.uniform(0.0, 100.0)
        await ctx.send(content=f"A `{thing}` le doy un... **{round(rate_amount, 2)} / 100**")
        print(f"cmdRating||        el bigobot dio un rating")

    @cog_ext.cog_slash()
    async def birra(self, ctx: SlashContext, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Toma una cerveza con alguien! 🍻, la sintaxis es #birra <@usuario> <razon> """
        
        # if its yourself or theres no mention
        if not user or user.id == ctx.author.id:
            return await ctx.send(content=f"**{ctx.author.name}**: paaaarty! 🎉 🍺")
        
        # if you mention the bot
        if user.id == self.bot.user.id:
            return await ctx.send(content="Tomare birra contigo 🍻")
        
        # if ??? XDLOL 
        if user.bot:
            return await ctx.send(content=f"Me encantaria tomar una birra contigo **{ctx.author.name}**, pero no creo que sea posible por ahora...")

        beer_offer = f"**{user.name}**, acabas de recibir una invitacion 🍺  de parte de: **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Razon:** {reason}" if reason else beer_offer
        msg = await ctx.send(content=beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** junto a **{ctx.author.name}** estan disfrutando unas birritas 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(content=f"Al parecer **{user.name}** no tenia interes en tomar una pinta con **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, if bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, acabas de recibir una invitacion 🍺  de parte de: **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Razon:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @cog_ext.cog_slash(description="el calentometro (hotmeter) puntua del 1~100 cualquier cosa que intrduzcas.")
    async def hotmeter(self, ctx: SlashContext, *, user: discord.Member = None):
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
        await ctx.send(content=f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @cog_ext.cog_slash(description="simula una maquina tragaperras, ideal para turnos.")
    async def slot(self, ctx):
        """ Gira la maquina tragaperras, util para decisiones de turnos """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(content=f"{slotmachine} Perfecto, Tu ganas! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(content=f"{slotmachine} Casi perfecto, pero aun ganas! 🎉")
        else:
            await ctx.send(content=f"{slotmachine} No hay match, no ganas... 😢")

    @cog_ext.cog_slash(description="Lanza dados del 1 al 6. Comando personalizable, los ultimos dos argumentos pueden cambiar su digito!")
    async def dados(self, ctx: SlashContext, user=None, number1=1, number2=6):
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

        await ctx.send(content="Dados lanzados!", embed=dadosEmbed)
        print(f"cmdDados||      Comando utilizado")

    @cog_ext.cog_slash(description="Aparece un brawler random")
    async def randombrawl(self, ctx: SlashContext):
        '''Brawler random, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
        msg = await ctx.send("1...")
        await asyncio.sleep(0.5)
        await msg.edit("2...")
        await asyncio.sleep(0.5)
        await msg.edit("3...", delete_after=30.0)
        await asyncio.sleep(0.5)
        
        randomBrawl = random.choice(brawlers)
        order = brawlers.index(randomBrawl)
        imageBrawl = brawlers_images[order]

        embed = discord.Embed(color = discord.Colour.orange())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/797964925980246066/c849eb95e858ce12cdc86cb6d4ecb36b00bbdfaa96d9973852d1421661f5aec5200.png")
        embed.set_image(url=imageBrawl)
        embed.add_field(name= "**Brawler Aleatorio:**", value=f"**{randomBrawl}**")
        embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Le tocó a {ctx.author}")
        
        await ctx.send(content="Este es el brawler", embeds=[embed], delete_after=50.0)
        print(f"cmdRandomBrawl|| Brawler aleatorio enviado, en la lista hay: {str(len(brawlers))}")

    @cog_ext.cog_slash(description="Aparece un campeon random del lol")
    async def randomchamp(self, ctx: SlashContext):
        '''Campeon random de lol, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
        # countdown
        msg = await ctx.send("1...")
        await asyncio.sleep(0.5)
        await msg.edit("2...")
        await asyncio.sleep(0.5)
        await msg.edit("3...", delete_after=30.0)
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
        
        await ctx.send(content="Este es el campeon", embeds=[embed3], delete_after=50.0)
        print(f"cmdRandomChamp|| Campeón aleatorio enviado, en la lista hay: {str(len(campeones))}")

    @cog_ext.cog_slash(name="meme", description="a quien no le gustan los memes?")
    async def meme(self, ctx: SlashContext):

        random_link = random.choice(images)
        if (
                random_link.startswith('https://video.twimg.com/ext_tw_video/') or 
                random_link.startswith('https://imgur') or 
                random_link.startswith('https://www.youtube:') or
                random_link.startswith('https://i.imgur') or 
                random_link.startswith('https://youtu')
            ):
                await ctx.send(content=f"{random_link}")

        else:
            embedMeme = discord.Embed(title='meme random cortesia del bigobot',color = discord.Colour.red())
            embedMeme.set_image(url = str(random_link))
            await ctx.send(content="meme salido del horno", embeds=[embedMeme])

    @cog_ext.cog_slash(description="1er argumento number, un numero. 2do argumento int. tiempo de espera en segundos")
    async def contar(self, ctx: SlashContext, number: int, intervalo):
        '''
        El bot cuenta hasta un numero dado, puede ser re carnasa...
        Los mensajes luego de 30 segundos se autoeliminan...
        Argumento <number>: int | **numero hasta el cual contar**. 
        Argumento <intervalo>: float | **velocidad a la cual contar en segundos**.
        Ejemplo: `#contar 50 0.5` -> el bot contara hasta el 50 a velocidad de 1/2 segundo
        '''
        i = 1
        while i <= number:    
            await asyncio.sleep(float(intervalo))
            await ctx.send(content=f"{i}", delete_after=30.0)
            i += 1

    @cog_ext.cog_slash()
    async def trivia(self, ctx: SlashContext):
        '''It's trivia time!!!'''
        msg = await ctx.channel.send(content=random.choice(trivias))
        await msg.add_reaction(u"\u2705")
        await msg.add_reaction(u"\U0001F6AB")

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=15.0)  
            # countdown
            msg = await ctx.send("1...")
            await asyncio.sleep(1)
            await msg.edit("2...")
            await asyncio.sleep(1)
            await msg.edit("3...", delete_after=30.0)
            await asyncio.sleep(1)

        except asyncio.TimeoutError:
            await ctx.channel.send(content="Che me ignoraron la trivia (▀̿Ĺ̯▀̿ ̿) ", delete_after=35.0)

        else:
            if reaction.emoji ==  u"\u2705":
                await ctx.message.delete()
                await ctx.channel.send(content=random.choice(trivia_accept), delete_after=120.0)

            else:
                await ctx.message.delete()
                await ctx.channel.send(content=random.choice(trivia_decline), delete_after=120.0)

    @cog_ext.cog_slash()
    async def willy(self, ctx: SlashContext):
        '''videos del willy out of context, un cago de risa...'''
        await ctx.send(content=random.choice(willyooc))
        print(f'cmdWilly||      video de Willy OOC enviado')

    @cog_ext.cog_slash(description="Tunea un texto (fuente), 2do argumento <orden> 1 ~ 8, 3er argumento <tutexto>")
    async def tunear(self, ctx: SlashContext, orden: int, *, args=None):
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
                await ctx.send(content=myThiccString)
                print(f"cmdTunear1||        {ctx.author.name} tuneó un texto")

            elif args is None and orden is None:
                await ctx.send(content="Seguido del comando debes introducir un orden (1 a 8) seguido del texto a tunear", delete_after=30.0)
                await ctx.send(content="A modo de ejemplo: **#tunear 4 textodepruebacopipedro**", delete_after=30.0)
                print(f"cmdTunear||        {ctx.author.name} falló al tunear un texto")

        except Exception as e:
            if isinstance(e, commands.MissingRequiredArgument):
                await ctx.send(content="Debes seguir la sintáxis #tunear <orden>, prueba con #help tunear para mas info.", delete_after=130.0)
                await ctx.send(content="Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y para ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**", delete_after=150.0)
            else:
                await throw_error(ctx=ctx, e=e)


    ##############
    ############## COMANDOS DE VIDEOS RANDOMS 
    #---> Lamar roasts Franklin vid <---
    @cog_ext.cog_slash()
    async def roast(self, ctx: SlashContext):
        '''Lamar roasts Franklin trending videos...'''
        await ctx.send(content=random.choice(roasts))
        print(f'cmdRoast||      Lamar v Franklin enviado.')

    #---> LocuraBailandoSinPantalones vid <---
    @cog_ext.cog_slash()
    async def locurabailando(self, ctx: SlashContext):
        '''Locura bailando...'''
        await ctx.send("http://youtu.be/tvvGVZpnOMA")
        print(f'cmdLocura...||  Video del locurabailando a {ctx.author.name}')

    #---> gordoPistero vid <---
    @cog_ext.cog_slash()
    async def pistero(self, ctx: SlashContext):
        '''Gordo pistero'''
        await ctx.send(content="https://cdn.discordapp.com/attachments/793309880861458473/850956075892998175/gordo_pistero_en_moto_con_cancion_brasilena.mp4")
        print(f'cmdLocura...||      Video del gordopistero enviado')

    #---> TADEO 1hs EN WHEELIE vid <---
    @cog_ext.cog_slash()
    async def tadeo(self, ctx: SlashContext):
        '''Video del Tadeo moto moto 1 hora en bucle'''
        await ctx.send(content="https://youtu.be/ffoXJhzwcHQ")

    #---> MATEUS505 GALO SNIPER vid <---
    @cog_ext.cog_slash()
    async def galosniper(self, ctx: SlashContext):
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
        embedGalo.set_footer(text="galo sniper")
        
        await ctx.send(content="https://www.youtube.com/watch?v=cwiVlpW7-XM", embed=embedGalo)
        print(f'cmdGaloSniper||   Video del GALOSNIPER enviado a {ctx.author.name} XD')
    ############## FIN DE VIDEOS DE COMANDOS RANDOMS
    ##############


def setup(bot):
    bot.add_cog(FunCommands(bot))