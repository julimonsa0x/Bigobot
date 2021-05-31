import discord
from discord.ext import commands
import random
import requests

from apis.functions import typing_sleep, printt

class RedditMeme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        printt("cog de reddit_meme listo")
    

    @commands.command(aliases=['redditmeme','memereddit','meme_reddit'])
    async def reddit_meme(self, ctx, subreddit_to_search=None):
        """
        ES: Busca un meme random en un subreddit dado.
        por defecto envia memes del subreddit r/memes...
        ejemplo: #reddit_meme MemesArgentina
        No spamear el comando caso contrario se causara
        un error 429 y quedara inutilizable por un tiempo.
        •
        EN: Searchs for a random meme in a given subreddit. 
        subreddit r/memes by default if no subreddit is given...
        syntax example: #reddit_meme dankmemes\n        
        """
        
        if subreddit_to_search != None:
            subreddit_url = f"https://www.reddit.com/r/{subreddit_to_search}.json"
        elif subreddit_to_search == None:
            subreddit_url = "https://www.reddit.com/r/memes.json"
            subreddit_to_search = "memes"


        # to-do:
        #   - make request withouth json method
        #   - if req.status_code is valid (200 n others)
        #       - save the json in databases/reddit_json
        #       - use one meme per command and pop used one
        #   - if req.status_code is not valid
        #       sorry bout that but thats the end...

        try:
            memes = requests.get(subreddit_url).json()

            pick_random = random.randint(0, 25)  # to choose between the 25 available posts that json returns.
            
            embedReddit = discord.Embed(
                title = (f"Meme|Post de r/{subreddit_to_search}."),
                color = discord.Color.purple()
            )
            
            titulo_var = memes["data"]["children"][pick_random]["data"]["title"]
            autor_var = memes["data"]["children"][pick_random]["data"]["author"]
            likes_var = memes["data"]["children"][pick_random]["data"]["score"]
            url_var = memes["data"]["children"][pick_random]["data"]["url"]
            
            embedReddit.add_field(name = "**Título**", value = titulo_var, inline = True)
            embedReddit.add_field(name = "**Autor**", value = autor_var, inline = True)
            embedReddit.add_field(name = "**Likes**", value = likes_var, inline = True)
            embedReddit.set_image(url=url_var)
            embedReddit.set_footer(icon_url = ctx.author.avatar_url, text = f"Meme para {ctx.author.name}")
            
            await typing_sleep(ctx)
            await ctx.send(embed = embedReddit)
            print(f'cmdRedditMeme||         Meme enviado a {ctx.author.name}')
        except Exception as e:
            await typing_sleep(ctx)
            await ctx.send(f"Hubo un error al tratar de buscar un meme de reddit, puede ser por error del propio comando o muchas peticiones a los servidores de reddit. Info del error enviada al canal del bigobot.")
            exception = f"==========\n`Excepcion causada:{e}`\n`Traceback:{e.with_traceback}`\n`Razon:{e.args}`\n`Peticion: {str(memes)[:75]}`=========="
            bigobot_chann = 799387331403579462
            bigobot_channel = await self.bot.fetch_channel(bigobot_chann)
            await bigobot_channel.send(exception)



def setup(bot):
    bot.add_cog(RedditMeme(bot))
