# Original author AlexFlipnote / discord_bot.py

import time
import discord
import psutil
import os

from datetime import datetime
from discord.ext import commands
from apis.default import timeago
from functions import printt


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

        @commands.Cog.listener()
        async def on_ready(self):
	        printt("cog de bot_info listo")

    @commands.command()
    async def about(self, ctx):
        """ Some info about the bot | Algo de informacion sobre el bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embedColour = discord.Embed.Empty
        if hasattr(ctx, "guild") and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        # If not thumbnail, try using self.bot.user.avatar_url or self.ctx.bot.user.avatar_url or ctx.bot.user.avatar_url when not in cogs
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/836063449989513216/bigobot_avatar.png")
        #embed.add_field(name="Ultimo inicio", value=timeago(datetime.now() - self.bot.uptime), inline=False)
        embed.add_field(name="Libreria", value=f"discord.py: {discord.__version__}", inline=False)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )", inline=False)
        embed.add_field(name="Comandos totales", value=len([x.name for x in self.bot.commands]), inline=False)
        embed.add_field(name="Uso de RAM", value=f"{ramUsage:.2f} MB", inline=False)
        embed.add_field(name="Codigo fuente", value="https://github.com/julimonsa0x/Bigobot")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Solicitud de: {ctx.author.name}")

        await ctx.send(content=f"ℹ About **{ctx.bot.user}**", embed=embed)
        print(f"cmdAbout||       {ctx.author.name} just requested the info about the bot")

def setup(bot):
    bot.add_cog(Information(bot))