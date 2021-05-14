import discord
from discord.ext import commands
from facebook_scraper import get_posts
from functions import printt
from functions import typing_sleep


def get_image(dict_content: str):
    if "image" in dict_content and "images" in dict_content:
        return dict_content["image"]
    if "image" in dict_content:
        return dict_content["image"]
    if "images" in dict_content:
        return dict_content["images"][0]


class fb_posts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de fb_posts listo")


    @commands.command()
    async def fb_post(self, ctx, post_amount:int=1):
        """
        Comando para devolver un embed con contenidos de posts de la EPET 14
        Argumento <post_amount>, numero entre 1 y 10, aconsejable >2
        Aproximadamente, 2 a 3 posts/embeds x post_amount.

        Por favor no spamear el comando, mucho menos con argumento <post_amount> 
        elevado en numero ya que se corre el riesgo de quedar inutil (el comando)
        por parte de facebook (politicas de uso relacionadas con el scraping de robots)
                
        Command to return a rich content embed of facebook EPET 14 posts.
        Argument <post_amount>:int (default 1), max 10 posts.
        Approximately, 2-3 posts per page.
        """
        
        postt = get_posts('EPET-14-Institucional-312214785790856', pages=post_amount, extra_info=True, options={"comments": True})
        for i in range(post_amount):
            
            await typing_sleep(ctx)
            await ctx.send(f"Mostrando un aproximado de {float(post_amount) * 2.5} posts")

            for post in postt:
                post_title = post["post_text"]
                post_link = post["post_url"]
                post_likes = post["likes"]
                post_comments = post["comments"]
                post_shares = post["shares"]
                try:
                    post_image = get_image(post)
                except Exception:
                    post_image = post["image"]
                
                #print(f"===== POST {i + 1}====")
                #print(post_title)
                #print(post_link)
                #print(f"===== POST {i + 1}====\n")

                post_embed = discord.Embed(
                    title=f"{post_title[:15]}...",
                    description=f"[Link al posteo]({post_link})",
                    colour=discord.Colour.blue()
                )
                if post_image != None:
                    post_embed.set_image(url=post_image)
                post_embed.set_thumbnail(url="https://media.discordapp.net/attachments/793309880861458473/842630187161485312/logo_epet_14.png?width=410&height=373")
                post_embed.add_field(name="Titulo", value=post_title, inline=False)
                post_embed.add_field(name="Likes :thumbsup:", value=post_likes, inline=True)
                post_embed.add_field(name="Comentarios :speech_balloon:", value=post_comments, inline=True)
                post_embed.add_field(name="Compartido", value=f"{post_shares} veces", inline=True)
                post_embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Solicitud de: {ctx.author.name}")

                try:
                    await typing_sleep(ctx)
                    await ctx.send(embed=post_embed)
                except Exception as e:
                    await typing_sleep(ctx)
                    await ctx.send(f"=========\nAn exception \n'*{e}*' occured. Content: ```{e.args}```\n=========")
                    
    

def setup(bot):
    bot.add_cog(fb_posts(bot))
