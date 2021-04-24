# cog to extract json data from a minecraft sv
# source: github.com/afazio1/robotic-nation-proj/blob/master/projects/discord-bot/minecraft-bot.py

import discord
from discord.ext import commands
from discord.ext.commands import Cog
import requests
from asyncio import sleep
from random import uniform


class ServerInfo(Cog):	
    def __init__(self, bot):
	    self.bot = bot

    @Cog.listener()
    async def on_ready(self):
	    print("cog de server_statuses listo")

    @commands.command()
    async def server_mc(self, ctx, server_ip: str):
        '''Info sobre servers solo versiones +1.7, debes introducir la IP del servidor...'''
        r = requests.get('https://api.mcsrvstat.us/2/' + server_ip)
        json_data = r.json()

        map_name = str(json_data["map"])
        sv_version = str(json_data["version"])
        mods_amount = len(json_data["mods"]["names"])  # may require len(list(...))
        sv_descript = str(json_data["motd"]["raw"][0])
        is_online = "Activo" if str(json_data["online"]) == "True" else "Apagado"
        actual_players = str(json_data["players"]["online"])
        max_players = str(json_data["players"]["max"])
        players_list = "\n".join([i for i in json_data["players"]["list"]])

        embed = discord.Embed(
            title= "Info sobre el server",
            color=discord.Color.dark_green())
        embed.set_thumbnail(url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")
        embed.add_field(name="Nombre del mapa: ", value=f"{map_name}", inline=False)
        embed.add_field(name="Descripcion del mapa: ", value=f"{sv_descript}", inline=True)
        embed.add_field(name="Version del Server : ", value=f"{sv_version}", inline=False)
        embed.add_field(name="Estado de conexion: ", value=f"{is_online}", inline=True)
        embed.add_field(name="Mods Totales: ", value=f"{mods_amount}", inline=False)
        embed.add_field(name="Capacidad maxima: ", value=f"{max_players} jugadores", inline=True)
        embed.add_field(name=f"Jugadores actuales {actual_players}: ", value=f"{players_list}", inline=False)
        
        type_time = uniform(0.5, 2)    
        async with ctx.typing():    
            await sleep(type_time)
            await ctx.send(embed=embed)
            print(f"ServerInfoCmd||         Informacion sobre server para {ctx.author.name}")

def setup(bot):
    bot.add_cog(ServerInfo(bot))