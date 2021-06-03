import discord
from discord.ext import commands
from translate import Translator

from apis.functions import printt, typing_sleep, throw_error


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
        Los argumentos <de_idioma> y <a_idioma> deben ser del tipo: 
        <es>, <en>, <fr>, <br>, <jp>, etc.
        A modo de ejemplo, se quiere traducir hello how are you a español
        Se sigue la sintaxis: #traducir es en hello how are you
        •   -----------------------------------------------------------   •
        ES: Las traducciones pueden no ser del todo ciertas!!!
        EN: Translations may not be 100% accurate at all!!!
        """
        try:
            if len(contenido) > 496:
                new_content = f"{contenido[:496]}..."
                translator = Translator(to_lang=a_idioma, from_lang=de_idioma)
                trans = translator.translate(new_content)
                await typing_sleep(ctx)
                await ctx.send(f":abcd: :repeat: Esta es la traduccion:\n```{trans}```")
            else:
                translator = Translator(to_lang=a_idioma, from_lang=de_idioma)
                trans = translator.translate(contenido)
                await typing_sleep(ctx)
                await ctx.send(f":abcd: :repeat: Esta es la traduccion:\n```{trans}```")
        except Exception as e:
            await typing_sleep(ctx)
            await throw_error(ctx=ctx,  e=e)
    
def setup(bot):
    bot.add_cog(Traductor(bot))