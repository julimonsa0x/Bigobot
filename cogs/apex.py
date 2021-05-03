import discord
from discord.ext import commands
from functions import get_apex_data, printt
import asyncio

class Apex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de apex_stats listo")


    @commands.command()
    async def apex(self, ctx, plataforma: str, usuario: str):
        """ 
        Using the tracker.gg API to return an embed with stats about someone
        Sintaxis del comando: #apex <plataforma> <usuario>
        El argumento plataforma debe ser: origin, xb1 o psn
        ejemplo 1: #apex origin Retekekw (muestra las stats de reteke)
        ejemplo 2: #apex xb1 Xspkxkenny
        ejemplo 3: #apex psn SvgXunis
        """

        apex_json, apex_status = get_apex_data(plataforma, usuario)
        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # jump to start, left, right, jump to end
        current = 0

        # Page 1 | General stats
        if apex_status:
            try:
                rankName = apex_json["data"]["segments"][0]["stats"]["rankScore"]["metadata"]["rankName"]
                rankPic = apex_json["data"]["segments"][0]["stats"]["rankScore"]["metadata"]["iconUrl"]
                level = apex_json["data"]["segments"][0]["stats"]["level"]["displayValue"]
                kills = apex_json["data"]["segments"][0]["stats"]["kills"]["displayValue"]
                damage = apex_json["data"]["segments"][0]["stats"]["damage"]["displayValue"]
                headshots = apex_json["data"]["segments"][0]["stats"]["headshots"]["displayValue"]
                finishers = apex_json["data"]["segments"][0]["stats"]["finishers"]["displayValue"]
                arKills = apex_json["data"]["segments"][0]["stats"]["arKills"]["displayValue"]

            except Exception as e:
                print("exception occurred: " + e.args)

        # Page 2 | Main legend stats
        legend_is_main = apex_json["data"]["segments"][1]["metadata"]["isActive"]  # returns boolean
        # if else in case of non-expected key-value
        if legend_is_main:
            legendMain = apex_json["data"]["segments"][1]["metadata"]["name"]
        else:
            legendMain = apex_json["data"]["metadata"]["activeLegendName"]
        legendMainPic = apex_json["data"]["segments"][1]["metadata"]["imageUrl"]
        killsMain = str(apex_json["data"]["segments"][1]["stats"]["kills"]["displayValue"]).replace(",", ".")
        totalBulletsMain = str(apex_json["data"]["segments"][1]["stats"]["tacticalBulletsAmped"]["displayValue"]).replace(",", ".")
        season6WinsMain = apex_json["data"]["segments"][1]["stats"]["season6Wins"]["displayValue"]
        season6KillsMain = apex_json["data"]["segments"][1]["stats"]["season6Kills"]["displayValue"]

        # Page 3 | Second legend
        secondLegend = apex_json["data"]["segments"][2]["metadata"]["name"]
        secondLegendPic = apex_json["data"]["segments"][2]["metadata"]["imageUrl"]
        second_has_stats = apex_json["data"]["segments"][2]["stats"] # returns boolean
        if second_has_stats:
            secondKills = apex_json["data"]["segments"][2]["stats"]["kills"]["displayValue"] 
            secondHeadshots = apex_json["data"]["segments"][2]["stats"]["headshots"]["displayValue"]
        
        elif not second_has_stats:
            secondStats = f"No pude obtener datos correctos para {secondLegend}"
    
        # Page 4 | Third Legend
        thirdLegend = apex_json["data"]["segments"][3]["metadata"]["name"]
        thirdLegendPic = apex_json["data"]["segments"][3]["metadata"]["imageUrl"]
        third_has_stats = apex_json["data"]["segments"][3]["stats"] # returns boolean
        if third_has_stats:
            thirdKills = apex_json["data"]["segments"][3]["stats"]["kills"]["displayValue"] 
            thirdHeadshots = apex_json["data"]["segments"][3]["stats"]["headshots"]["displayValue"]
       
        elif not third_has_stats:
            thirdStats = f"No pude obtener datos correctos para {thirdLegend}"
        
        #####################################
        #####################################

        # Page 1 embed | General Stats
        page1 = discord.Embed(
            title="Stats generales", 
            description="Usa los botones de abajo para cambiar de pagina.", 
            colour=discord.Colour.orange()
        )
        page1.add_field(name="Rango", value=rankName, inline=True)
        page1.add_field(name="Nivel", value=level, inline=True)
        page1.add_field(name="Bajas", value=kills, inline=True)
        page1.add_field(name="Daño total", value=damage, inline=True)
        page1.add_field(name="Headshots", value=headshots, inline=True)
        page1.add_field(name="Finalizadores", value=finishers, inline=True)
        page1.add_field(name="Bajas de AR", value=arKills, inline=True)
        page1.set_thumbnail(url=rankPic)
        page1.set_footer(text=f"Page n° {current}")

        # Page 2 embed | Main legend Stats
        page2 = discord.Embed(
            title="Stats: Leyenda Main", 
            colour=discord.Colour.orange()
        )
        page2.add_field(name="Leyenda", value=legendMain, inline=True)
        page2.add_field(name="Bajas", value=killsMain, inline=True)
        page2.add_field(name="Balas disparadas", value=totalBulletsMain, inline=True)
        page2.add_field(name="Victorias en Season 6", value=season6WinsMain, inline=True)
        page2.add_field(name="Bajas en Season 6", value=season6KillsMain, inline=True)
        page2.set_thumbnail(url=legendMainPic)
        page2.set_footer(text=f"Page n° {current}")

        # Page 3 embed | Second legend
        page3 = discord.Embed(
            title=f"Stats: {secondLegend}", 
            colour=discord.Colour.orange()
        )
        if second_has_stats:
            page3.add_field(name="Leyenda", value=secondLegend, inline=True) # # # #
            page3.add_field(name="Bajas", value=secondKills, inline=True)
            page3.add_field(name="Headshots", value=secondHeadshots, inline=True)
            page3.set_thumbnail(url=secondLegendPic)
        elif not second_has_stats:
            page3.add_field(name="Hubo un error", value=secondStats)
        page3.set_footer(text=f"Page n° {current}")

        # Page 4 embed | Third legend
        page4 = discord.Embed(
            title=f"Stats: {thirdLegend}", 
            colour=discord.Colour.orange()
        )
        if third_has_stats:
            page4.add_field(name="Leyenda", value=thirdLegend, inline=True) # # # #
            page4.add_field(name="Bajas", value=thirdKills, inline=True)
            page4.add_field(name="Headshots", value=thirdHeadshots, inline=True)
            page4.set_thumbnail(url=thirdLegendPic)
            page4.set_footer(text=f"Page n° {current}")
        elif not third_has_stats:
            page4.add_field(name="Hubo un error", value=thirdStats)
        page4.set_footer(text=f"Page n° {current}")

        # Asyncio.TimeoutError Embed
        pageTimeout = discord.Embed(title="Asyncio.TimeoutError ", color=discord.Colour.red())
        pageTimeout.add_field(name="not working embed", value="rewrite the command and react within 2 minutes")

        pages_list = [page1, page2, page3] 
        msg = await ctx.send(embed=pages_list[current])
        printt(f"cmdApexStats||         {ctx.author.name} busco las estadisticas de {usuario} en Apex")
        
        for button in buttons:
            await msg.add_reaction(button)  
        
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", 
                    check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, 
                    timeout=120
                )

            except asyncio.TimeoutError:
                await msg.edit(embed=pageTimeout)

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0
                    
                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1
                        
                elif reaction.emoji == u"\u27A1":
                    if current < len(pages_list)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(pages_list)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=pages_list[current])

def setup(bot):
    bot.add_cog(Apex(bot))