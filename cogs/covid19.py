import discord
from discord.ext import commands
import pandas as pd
from datetime import datetime
from matplotlib import pyplot
from apis.covid_api import covid_api_request
from asyncio import sleep
from random import uniform
from functions import printt


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de covid_19 listo")

    @commands.command()
    async def covid(self, ctx, country):
        '''Muestra info del covid sobre un pais especifico, siguiendo la sintaxis #covid <pais>'''
        request_result = covid_api_request(f'dayone/country/{country}')

        data_set = [(datetime.strptime(date_index['Date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b'), death_index['Deaths'])
                    for date_index, death_index in zip(request_result, request_result)]

        # Plot
        data_frame = pd.DataFrame(data_set)
        data_frame.plot(x=0, y=1, color='#00012C', label='Months')

        # Label
        pyplot.title(f'Mostrando muertes en: {country}')
        pyplot.xlabel('Meses')
        pyplot.ylabel('Numero de muertes aprox.')

        # Legend
        pyplot.legend(loc='upper left')

        # Color
        #pyplot.axes().set_facecolor('#9A1622')

        pyplot.savefig('images\\covid_death_graph.png', bbox_inches='tight')

        type_time = uniform(0.5, 2)
        async with ctx.typing():    
            await sleep(type_time)
            await ctx.send(file=discord.File('images\\covid_death_graph.png'))
            print(f"CovidCmd||       Grafico sobre covid en {country} para {ctx.author.name}")


def setup(bot):
    bot.add_cog(Covid(bot))