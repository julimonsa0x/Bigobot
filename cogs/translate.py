import discord
from discord.ext import commands
from translate import Translator

from functions import printt, typing_sleep


class Traductor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de traducciones listo")

    
    @commands.command(aliases=['translate','translator','traductor','traduce'])
    async def traducir(self, ctx, a_idioma, de_idioma='en', *, contenido):
        """
        Traduce un texto de un idioma, a otro idioma que quieras.
        Los argumentos <de_idioma> y <a_idioma> deben ser del tipo: <es>, 
        <en>, <fr>, <br>, <jp>, etc.
        A modo de ejemplo, se quiere traducir <hello how are you> a español
        Se sigue la sintaxis: #traducir es en hello how are you
        Las traducciones pueden no ser del todo ciertas!!!
        Translations may not be 100% accurate!!!
        """
        translator = Translator(to_lang=a_idioma, from_lang=de_idioma)
        trans = translator.translate(contenido)
        await typing_sleep(ctx)
        await ctx.send(f":abcd: :repeat: Esta es la traduccion:\n```{trans}```")

    
def setup(bot):
    bot.add_cog(Traductor(bot))