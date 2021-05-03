# Original author AlexFlipnote / discord_bot.py

import random
import discord
import secrets
import asyncio
from random import uniform
import aiohttp
import requests
import json

from io import BytesIO
from discord.ext import commands
from apis import permissions
from databases import ballresponse
from functions import printt

type_time = uniform(0.5, 2)


class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de fun_stuff listo")
    

    @commands.command(aliases=["8ball"])
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consulta 8ball para recibir una respuesta """
        answer = random.choice(ballresponse)
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(f"🎱 **Pregunta:** {question}\n**Respuesta:** {answer}")


    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def pato(self, ctx):
        """ Manda una foto de patos random"""
        r = requests.get('https://random-d.uk/api/v1/random')
        duck_url = r.json()["url"]
        embed = discord.Embed(color = discord.Colour.dark_gold())
        embed.set_image(url = duck_url)
        async with ctx.typing():    
            await asyncio.sleep(type_time)
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
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(embed = embed)
            print(f"cmdCafe||         {ctx.author.name} pidio una foto de cafes")

    @commands.command(aliases=["flip", "coin", "tossacoin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        # head and tails in english!
        coinsides = ["Cara", "Cruz"]
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(f"**{ctx.author.name}** tiro una moneda y toco **{random.choice(coinsides)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"for **{text}** " if text else ""
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(f"**{ctx.author.name}** le ha pagado respetos {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def definir(self, ctx, *search: commands.clean_content):
        """ Encuentra la mejor definicion para tus palabras """
        async with ctx.channel.typing():
            try:
                r = requests.get(f"https://api.urbandictionary.com/v0/define?term={search}").json()
            except Exception as e:
                async with ctx.typing():    
                    await asyncio.sleep(type_time)
                    await ctx.send(f"Exception: {e}. Urban API returned invalid data... might be down atm.")

            if not r:
                return await ctx.send("Hubo un error...")

            if not len(r["list"]):
                return await ctx.send(f"No pude encontrar una definicion para {search}...")

            result = sorted(r["list"], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result["definition"]
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(" ", 1)[0]
                definition += "..."

            async with ctx.typing():    
                await asyncio.sleep(type_time)
                await ctx.send(f"📚 Definicion para: **{result['word']}**```fix\n{definition}```")

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        """
        EN: Everything you type after reverse will of course, be reversed
        ES: Lo que escribas se da vuelta, aunque es recomendable usar #tunear 4 <tu_texto>
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(f"🔁 {t_rev}")

    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.author.send(f"🎁 **Esta es tu contraseña:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command()
    async def rating(self, ctx, *, thing: commands.clean_content):
        """ Le doy un rating a lo que sea... """
        rate_amount = random.uniform(0.0, 100.0)
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.send(f"A `{thing}` le daria un... **{round(rate_amount, 2)} / 100**")
            print(f"cmdRating||        el bigobot le dio un rating de {rate_amount} a {thing}")

    @commands.command()
    async def birra(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Toma una cerveza con alguien! 🍻, la sintaxis es #birra <@usuario> <razon> """
        
        # if its yourself or theres no mention
        if not user or user.id == ctx.author.id:
            async with ctx.typing():    
                await asyncio.sleep(type_time)
                return await ctx.send(f"**{ctx.author.name}**: paaaarty! 🎉 🍺")
        
        # if you mention the bot
        if user.id == self.bot.user.id:
            return await ctx.send("Toma birra contigo 🍻")
        
        # if ??? XDLOL 
        if user.bot:
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
            async with ctx.typing():    
                await asyncio.sleep(type_time)
                await msg.edit(content=f"**{user.name}** junto a **{ctx.author.name}** estan disfrutando unas birritas 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
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
        async with ctx.typing():    
            await asyncio.sleep(type_time)
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


def setup(bot):
    bot.add_cog(Fun_Commands(bot))