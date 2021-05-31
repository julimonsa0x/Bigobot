import discord
from discord.colour import Color
from discord.ext import commands
from asyncio import sleep

import os
from dotenv import load_dotenv
import re
from instaloader.structures import Post, Profile
from instaloader import Instaloader

from apis.functions import printt, typing_sleep

load_dotenv()
##########################################

# instantiate base class.
insta = Instaloader(user_agent='chrome')

# Required login for most of the commands
# Consider saving credentials inside .env
insta.login(os.getenv('IG_USER'), os.getenv('IG_PASS'))

def url_to_short_code(post_url:str):
    regexp = '^(?:.*\/(p|tv)\/)([\d\w\-_]+)'
    post_short_code = re.search(regexp, post_url).group(2)
    return str(post_short_code)

def save_post(url:str, new_name:str):
    """ Save a post by providing url """
    shortcode = url_to_short_code(url)
    post = Post.from_shortcode(context=insta.context, shortcode=shortcode)
    insta.download_post(post, target=new_name)


##########################################

class Instagram(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        printt("cog de instagram listo")

    @commands.command()
    async def descargar_post(self, ctx, url:str, nombre:str):
        """
        Descarga un post de instagram de una cuenta publica 
        junto al nombre que le quieras poner al archivo.
        La unica condicion es que el archivo sea menor a 8mb.
        Para archivos mayores se necesita servidor con boost nivel 2...
        """
        try:
            save_post(url, nombre)
            await typing_sleep(ctx)

            # search for the downloaded file
            for filename in os.listdir(f'./{nombre}'):
                # check if filename is compatible:
                if os.path.getsize(f"{nombre}/{filename}") < 8388607:
                    if filename.endswith('.jpg') or filename.endswith('.mp4') or filename.endswith('.png'):

                        # get the extension
                        ext = filename[-4:]

                        # get the title from the saved .txt
                        with open(f"{nombre}/{filename[:-4]}.txt", "r", encoding='utf8') as f:
                            title = f.readlines()

                        file = discord.File(f"{nombre}/{filename}", filename=f"{nombre}{ext}")

                        # create the embed
                        instaEmbed = discord.Embed(
                            title = "Post descargado",
                            description = f"**Titulo del post**:\n{''.join(title)}"
                        )
                        instaEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/793309880861458473/847642387601686528/3b21c7efd2ba9c119fb8d361acacc31d.png?width=410&height=410")
                        instaEmbed.set_image(url=f"attachment://{filename}")
                        instaEmbed.set_footer(icon_url=f"{ctx.author.avatar_url}",text=f"Peticion de {ctx.author.name}")

                        # send the post
                        await ctx.message_delete()
                        await typing_sleep(ctx)
                        await ctx.send(embed=instaEmbed, file=file)

        except Exception as e:
            await ctx.send(f"Ocurrio un error al intentar de descargar un post de instagram...\nExcepcion: `{e}`\nTraceback: `{e.with_traceback}`")



def setup(bot):
    bot.add_cog(Instagram(bot))
