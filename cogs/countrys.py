# Author: Me

import discord
from discord.ext import commands
from asyncio import sleep

from random import uniform
from random import choice
from apis.functions import typing_sleep, printt

import json


class CountryGuesses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de country_guesses listo")

     
    @commands.command()
    async def paises(self, ctx):
        """Comando para adivinar paises de todo el mundo"""
        URL_IMAGES = "https://flagcdn.com/96x72/" # finishes with {country}.png!

        filee = open("databases/countrys.json", "r", encoding="utf-8")
        countrys = json.load(filee)
        
        # create a list to later, randomly pick the correct optionS
        countrys_list = []
        country_tuple = choice(list(countrys.items()))
        rand_fake_guess_1= choice(list(countrys.items()))[1]  #:str index the tuple, only country's name is required 
        rand_fake_guess_2 = choice(list(countrys.items()))[1]  #:str index the tuple, only country's name is required
        country_code = country_tuple[0]
        country_name = country_tuple[1]  #:str
        # print(f"selected country is: {country_tuple}")


        countrys_list.append(country_name)
        countrys_list.append(rand_fake_guess_1)
        countrys_list.append(rand_fake_guess_2)
        

        choice1 = choice(countrys_list)  # random country 1
        countrys_list.remove(choice1)
        choice2 = choice(countrys_list)  # random country 2
        countrys_list.remove(choice2)
        choice3 = choice(countrys_list)  # random country 3
        countrys_list.remove(choice3)
    

        embed = discord.Embed(
            title = "Adivina el pais",
            color = discord.Colour.orange())
        embed.set_image(url=f"{URL_IMAGES}{country_code}.png")
        embed.add_field(name="*Opcion 1*", value=f"{choice1}", inline=False)
        embed.add_field(name="*Opcion 2*", value=f"{choice2}", inline=False)
        embed.add_field(name="*Opcion 3*", value=f"{choice3}", inline=False)
        embed.set_footer(text="Reacciona a los emotes de abajo")
        
        timeoutEmbed = discord.Embed(
            title=" :alarm_clock: **Te quedaste sin tiempo**",
            description="Intenta otra vez"
        )

        correct_country = discord.Embed(title="*Correcto*  ✨  🎉  🥳", color=discord.Colour.green())
        fake_country = discord.Embed(title="*Incorrecto*  😔", color=discord.Colour.red()).add_field(name=f"El pais correcto era:", value=country_name)

        await ctx.message.delete()
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        

        # check for user reaction to emotes.
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda reaction, user: user == ctx.author and reaction.emoji in ["1️⃣", "2️⃣", "3️⃣"], 
                timeout=15
            )
            if reaction.emoji == "1️⃣":
                if choice1 not in country_tuple:
                    await typing_sleep(ctx)
                    await msg.delete()
                    await ctx.send(embed=fake_country)
                else:
                    await typing_sleep(ctx)
                    await ctx.send(embed=correct_country) 
            
            if reaction.emoji == "2️⃣":
                if choice2 not in country_tuple:
                    await typing_sleep(ctx)
                    await msg.delete()
                    await ctx.send(embed=fake_country)
                else:
                    await typing_sleep(ctx)
                    await ctx.send(embed=correct_country)
            
            if reaction.emoji == "3️⃣":
                if choice3 not in country_tuple:
                    await typing_sleep(ctx)
                    await msg.delete()
                    await ctx.send(embed=fake_country)
                else:
                    await typing_sleep(ctx)
                    await ctx.send(embed=correct_country)
        
        
        # except block triggered when timeout.
        except:
            await typing_sleep(ctx)
            await msg.delete()
            await ctx.send(embed = timeoutEmbed, delete_after=15.0)

        filee.close()


def setup(bot):
    bot.add_cog(CountryGuesses(bot))
