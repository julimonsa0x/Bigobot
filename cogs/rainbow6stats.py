#cog testing R6 stats
import asyncio
import discord
import json
from urllib.request import urlopen, Request
import aiohttp
import async_timeout
from discord.ext import commands
from discord.ext.commands import Cog


jsontoenglish = {"wins": "Wins", "has_played": "Ever Played", "losses": "Losses", "kills": "Kills", "deaths": "Deaths",
                 "playtime": "Playtime", "kd": "Kill/Death Ratio", "wlr": "Win/Loss Ratio", "assists": "Assists",
                 "barricades_built": "Barricades Built", "bullets_fired": "Bullets Fired", "bullets_hit": "Bullets Hit",
                 "headshots": "Headshots", "melee_kills": "Melee Kills", "penetration_kills": "Penetration Kills",
                 "reinforcements_deployed": "Reinforcements Deployed", "revives": "Revives",
                 "steps_moved": "Steps Moved", "suicides": "Suicides", True: "Hell Yeah", False: "Never ever"}


class Stats(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def r6stats(self, ctx, player: str=None, platform: str='uplay'):
        '''Comando sobre estadisticas de Rainbow 6 Siege, experimental no funcionando...'''
        if player is None:
            return await ctx.send("Error: Need a proper username")
        try:
            async with aiohttp.ClientSession() as cs:
                with async_timeout.timeout(30):
                    async with cs.get("https://api.r6stats.com/api/v1/players/{}?platform={}"
                                      .format(player, platform)) as r:
                        stats = await r.json()
        except Exception as ex:
            print(ex)
            return await ctx.send("Error: Need a valid username")
        if 'status' in stats:
            return await ctx.send(stats['errors'][0]['detail'])
        embed1 = discord.Embed(title="Stats for {} who also happens to be level {}"
                               .format(stats['player']["username"], stats['player']['stats']['progression']['level']))
        embed2 = discord.Embed(title="Overall Stats for {}".format(stats['player']['username']))
        embed1.add_field(name="Ranked Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['ranked']:
            if jsontoenglish[x] == "Playtime":
                embed1.add_field(name=jsontoenglish[x],
                                 value='{0:.2f} hours'.format(float(stats['player']['stats']['ranked'][x])/3600))
            elif type(stats['player']['stats']['ranked'][x]) is not bool:
                embed1.add_field(name=jsontoenglish[x], value=stats['player']['stats']['ranked'][x])
            else:
                embed1.add_field(name=jsontoenglish[x], value=jsontoenglish[stats['player']['stats']['ranked'][x]])
                break
        embed1.add_field(name="Casual Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['casual']:
            if jsontoenglish[x] == "Playtime":
                embed1.add_field(name=jsontoenglish[x],
                                 value='{0:.2f} hours'.format(float(stats['player']['stats']['casual'][x])/3600))
            elif type(stats['player']['stats']['casual'][x]) is not bool:
                embed1.add_field(name=jsontoenglish[x], value=stats['player']['stats']['casual'][x])
            else:
                embed1.add_field(name=jsontoenglish[x], value=jsontoenglish[stats['player']['stats']['casual'][x]])
        # embed1.add_field(name="Overall Stats", value="------------------------", inline=False)
        for x in stats['player']['stats']['overall']:
            embed2.add_field(name=jsontoenglish[x], value=stats['player']['stats']['overall'][x])
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Stats(bot))