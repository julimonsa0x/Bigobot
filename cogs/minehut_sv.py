# cog to extract json data from a minehut sv
# source: github.com/afazio1/robotic-nation-proj/blob/master/projects/discord-bot/minecraft-bot.py

import discord
from discord.ext import commands
from discord.ext.commands import Cog
import requests
from functions import printt


class MinehutInfo(Cog):	
    def __init__(self, bot):
	    self.bot = bot

    @Cog.listener()
    async def on_ready(self):
	    printt("cog de minehut_server info listo")

    @commands.command()
    async def minehut(self, ctx, arg):
        '''Info sobre servers de Minehut, debes introducir el nombre del server'''
        r = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
        json_data = r.json()

        description = json_data["server"]["motd"]
        online = str(json_data["server"]["online"])
        playerCount = str(json_data["server"]["playerCount"])

        embed = discord.Embed(
            title=arg + " Server Info",
            description='Description: ' + description + '\nOnline: ' + online + '\nPlayers: ' + playerCount,
            color=discord.Color.dark_green()
        )
        embed.set_thumbnail(url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

        await self.bot.send(embed=embed)  #bot.send does not works anymore now is ctx.send.....

def setup(bot):
    bot.add_cog(MinehutInfo(bot))