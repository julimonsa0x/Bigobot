import discord
from discord import colour
from discord.colour import Color
from discord.ext import commands
from functions import printt
from facebook_scraper import get_posts
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
    async def fb_post(self, ctx, *facebook_page: str, max_pages=2):
        """
        temp cmd to get facebook posts and return a rich content embed
        facebook_page arg: str
        max_pages: int (default 2)
        """
        
        post = dict(get_posts(facebook_page, page_limit=max_pages, extra_info=True, options={"comments": True}))
        post_title = post["post_text"]
        post_link = post["post_url"]
        post_likes = post["likes"]
        post_comments = post["comments"]
        post_shares = post["shares"]
        try:
            post_image = get_image(post)
        except Exception:
            post_image = post["image"]

        post_embed = discord.Embed(
            title=f"{post_title[15:]}...",
            description=f"[Link al posteo]({post_link})",
            colour=discord.Colour.blue()
        )
        post_embed.set_image(url=post_image)
        post_embed.add_field(name="Likes del posteo", value=post_likes)
        post_embed.add_field(name="Comentarios del posteo", value=post_comments)
        post_embed.add_field(name="Veces compartido", value=post_shares)
        post_embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Solicitud de: {ctx.author.name}")

        await typing_sleep(ctx)
        await ctx.send(self, embed=post_embed)


    

def setup(bot):
    bot.add_cog(fb_posts(bot))
