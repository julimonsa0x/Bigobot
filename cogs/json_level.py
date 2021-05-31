import typing
import discord
from discord.ext import commands
import json

from main import bigo_guild_base, bigo_guild_id
from apis.functions import typing_sleep, printt
import apis.functions

class LevelSystem(commands.Cog):      
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        printt("cog de json_level listo")

    
    @commands.command(aliases = ['rank','lvl','nivel'])
    async def level(self, ctx, member: discord.Member = None):
        """ Muestra el nivel basado en cantidad de comentarios enviados de un @miembro """
        if not member:
            user = ctx.message.author
            with open('databases/level.json','r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

            embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.message.delete()
            await typing_sleep(ctx)
            await ctx.send(embed = embed)
        else:
            with open('databases/level.json','r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(member.id)]['level']
            exp = users[str(ctx.guild.id)][str(member.id)]['experience']
            embed = discord.Embed(title = 'Nivel {}'.format(lvl), description = f"{exp} XP" ,color = discord.Color.green())
            embed.set_author(name = member, icon_url = member.avatar_url)

            await ctx.message.delete()
            await typing_sleep(ctx)
            await ctx.send(embed = embed)


    @commands.command(aliases=['cambiar_prefijo','set_prefix'])
    @commands.has_permissions(administrator = True)
    async def changeprefix(self, ctx, prefix):
        """ Comando para cambiar el prefijo de activacion del bot, por defecto es # """
        try:
            with open("databases/prefixes.json", "r") as f:
                prefixes = json.load(f)
            prefixes[str(ctx.guild.id)] = prefix
            with open("databases/prefixes.json", "w") as f:
                json.dump(prefixes,f, indent=2)
            await ctx.message.delete()
            await typing_sleep(ctx)
            await ctx.send(f":exclamation: Mi nuevo prefijo para este servidor ahora es: {prefix}")
        except Exception as e:
            await typing_sleep(ctx)
            await ctx.send(f"Al parecer no tienes los permisos necesarios para cambiar mi prefijo.\nMas info:```Excepcion:{e}\nRazon: {e.args}```")


    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if message.author.bot:
            pass

        if not message.author.bot:
            print('====| Mensaje obtenido para level.json...')
            try:
                with open('databases/level.json','r') as f:
                    users = json.load(f)
                    print('====| Mensaje cargado con exito !')
            except Exception as e:
                pass
                #printt('====| !! Hubo un error al escribir en la base de datos de niveles !!')
            await apis.functions.update_data(users, message.author,message.guild)
            await apis.functions.add_experience(users, message.author, 4, message.guild)
            await apis.functions.level_up(users, message.author,message.channel, message.guild)

            with open('databases/level.json','w') as f:
                json.dump(users, f, indent=4)
        
        # not necesary because sends a command twice...
        # there's already a .process_comm..., at main.py
        # await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(LevelSystem(bot))
