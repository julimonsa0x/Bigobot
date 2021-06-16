"""
Requires GENIUS_ACCESS_TOKEN .env 
"""
import discord
from discord.ext import commands
import lyricsgenius
from apis.functions import printt

from discord_slash import cog_ext, SlashContext

import os
from dotenv import load_dotenv  # to get the .env TOKEN
load_dotenv()


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de lyrics listo")

    @cog_ext.cog_slash(description="Busca las letras de una cancion. Argumento artista debe ser de una sola palabra")
    async def lyrics(self, ctx: SlashContext, artista: str, *, cancion):
        """
        #lyrics, #letras, #buscar_letras, todos sirven igual.
        Se sube un archivo .txt para que sea mas facil su lectura. 
        Argumento 1 <artist_name>: nombre del artista.
        Argumento 2 <song_name>: nombre de la cancion.
        """
        genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))
        song = genius.search_song(artist=artista, title=cancion)
        
        with open(f'databases/{cancion[:7]}_lyrics.txt', 'w', encoding='utf-8') as file:
            file.write(song.lyrics)
            printt("Lyrics saved successfully")
        
        await ctx.send(
            content=f"Mostrando Letras para **{cancion}**", 
            file=discord.File(f'databases/{cancion[:7]}_lyrics.txt')
        )
        
        # to check the song lyrics from shell
        # printt(f"=== Beginning ===", delay=0.075)
        # printt(str(song.lyrics))
        # printt(f"====== End ======", delay=0.075)
    

def setup(bot):
    bot.add_cog(Lyrics(bot))
