"""
Requires GENIUS_ACCESS_TOKEN .env 
"""
import discord
from discord.ext import commands
import lyricsgenius
from functions import printt
from functions import typing_sleep

import os
from dotenv import load_dotenv  # to get the .env TOKEN
load_dotenv()


class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
	    printt("cog de lyrics listo")

    @commands.command(aliases=['letras','liricas','buscar_letras', 'search_lyrics'])
    async def lyrics(self, ctx, artist_name: str, *, song_name):
        """
        #lyrics, #letras, #buscar_letras, todos sirven igual.
        Se sube un archivo .txt para que sea mas facil su lectura. 
        Argumento 1 <artist_name>: nombre del artista.
        Argumento 2 <song_name>: nombre de la cancion.
        Using lyricsgenius==3.0.1 searchs lyrics by song and artist.
        """
        genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))
        song = genius.search_song(artist=artist_name, title=song_name)
        
        with open(f'databases/{song_name[:7]}_lyrics.txt', 'w', encoding='utf-8') as file:
            file.write(song.lyrics)
            printt("Lyrics saved successfully")
        
        await typing_sleep(ctx)
        await ctx.send(f"***Letras para {song_name}***")
        await ctx.send(file=discord.File(f'databases/{song_name[:7]}_lyrics.txt'))
        #printt(f"=== Beginning ===", delay=0.075)
        #printt(str(song.lyrics))
        #printt(f"====== End ======", delay=0.075)
    

def setup(bot):
    bot.add_cog(Lyrics(bot))
