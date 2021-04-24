# Original author AlexFlipnote / discord_bot.py

import time
import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from apis.default import timeago

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

        @commands.Cog.listener()
        async def on_ready(self):
	        print("cog de bot_info listo")

    @commands.command()
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Ultimo inicio", value=timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(name="Libreria", value=f"discord.py: {discord.__version__}", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )", inline=True)
        embed.add_field(name="Comandos totales", value=len([x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="Uso de RAM", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))