# Author: Me (try block)
#         and
#         elixss_ (except block)
#           -> Asyncpraw tutorial: Meme command in discord.py | tutorial from youtube

import discord
from discord.ext import commands
import asyncpraw
import random
import requests

from dotenv import load_dotenv
from os import getenv
load_dotenv()

from apis.functions import typing_sleep, printt
REDDIT_ICON = 'https://media.discordapp.net/attachments/793309880861458473/852006681126895666/toppng.com-reddit-logo-reddit-icon-698x698.png?width=498&height=498'


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
        syntax example: #reddit_meme dankmemes
        Please do not spam the command, thanks.
        """
        
        if subreddit_to_search != None:
            subreddit_url = f"https://www.reddit.com/r/{subreddit_to_search}.json"
        elif subreddit_to_search == None:
            subreddit_url = "https://www.reddit.com/r/memes.json"
            subreddit_to_search = "memes"

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
        except:
            printt("====| El 1er metodo para extraer memes fallo, usando el 2do metodo")
            
            reddit = asyncpraw.Reddit(
                client_id = getenv('CLIENT_ID'),
                client_secret = getenv('CLIENT_SECRET'),
                username= 'JuliTJZ',
                password = getenv('REDDIT_PASSWORD'),
                user_agent = 'app:bigobot/user:JuliTJZ'
            )

            subreddit = await reddit.subreddit(subreddit_to_search)
            all_subs = []
            top = subreddit.top(limit=350)

            async for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            name = random_sub.title
            url = random_sub.url

            embed = discord.Embed(
                title=f'__{name}__',
                colour=discord.Color.purple(),
                timestamp = ctx.message.created_at,
                url=url
            )

            embed.set_image(url=url)
            embed.set_footer(text="meme listo! :clinking_glass:", icon_url=REDDIT_ICON)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(RedditMeme(bot))
