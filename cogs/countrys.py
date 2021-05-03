import discord
from discord.ext import commands
from functions import printt
from asyncio import sleep

from random import uniform
from random import choice

import json

type_time = uniform(0.5, 2)

class countryGuess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de country_guesses listo")

     
    @commands.command()
    async def paises(self, ctx):
        URL_IMAGES = "https://flagcdn.com/96x72/" # finishes with {country}.png!

        filee = open("databases/countrys.json", "r", encoding="utf-8")
        
        countrys = json.load(filee)
        country_tuple = choice(list(countrys.items()))
        rand_fake_guess_1= choice(list(countrys.items()))[1]
        rand_fake_guess_2 = choice(list(countrys.items()))[1]
        country_code = country_tuple[0]
        country_name = country_tuple[1]
        print(f"selected country is: {country_tuple}")
        
    
        embed = discord.Embed(
            title = "Adivina el pais",
            color = discord.Colour.dark_green())
        embed.set_image(url=f"{URL_IMAGES}{country_code}.png")
        embed.add_field(name="Opcion 1", value=f"{rand_fake_guess_1}", inline=False)
        embed.add_field(name="Opcion 2", value=f"{country_name}", inline=False)
        embed.add_field(name="Opcion 3", value=f"{rand_fake_guess_2}", inline=False)
        
        correct_country = discord.Embed(title="Correcto")
        fake_country = discord.Embed(title="Incorrecto").add_field(name=f"El pais correcto era:", value=country_name)
        fake_country2 = discord.Embed(title="Incorrecto").add_field(name=f"El pais correcto era:", value=country_name)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        

        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in ["1️⃣", "2️⃣", "3️⃣"], timeout=15)
            if reaction.emoji =="1️⃣":
                async with ctx.typing():    
                    await sleep(type_time)
                    await msg.delete()
                    await ctx.send(embed=fake_country)
            
            if reaction.emoji =="2️⃣":
                async with ctx.typing():    
                    await sleep(type_time)
                    #await msg.delete() if it's correct, dont delete initial embed
                    await ctx.send(embed=correct_country)
            
            if reaction.emoji =="3️⃣":
                async with ctx.typing():    
                    await sleep(type_time)
                    await msg.delete()
                    await ctx.send(embed=fake_country2)
        
        except Exception:
            await ctx.send("An exception occurred, try again !")



        filee.close()


def setup(bot):
    bot.add_cog(countryGuess(bot))
