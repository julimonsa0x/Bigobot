# Original author AlexFlipnote / discord_bot.py
# Stuff modified and added by me.
# Repo: https://github.com/AlexFlipnote/discord_bot.py

import os
import discord
from discord.ext import commands
import re
from urllib import parse, request
from io import BytesIO
from apis import default
from time import strftime
import json
import secrets
from pytube import extract  # required by the descarga cmd
from asyncio import sleep
import wikipedia
import pyqrcode
import requests

from apis.functions import (bro_birthdays_check,  # required by usuario command
                        typing_sleep,
                        printt,
                        degrees_to_cardinal)


class ComandosGenerales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        printt('cog de comandos_generales listo')


    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        '''Muestra el avatar de un @usuario que menciones'''
        if member is None:
            await typing_sleep(ctx)
            await ctx.send("Seguido del comando debes @Mencionar a alguien")
            await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")

        embedAvatar = discord.Embed(
            description = f'[**URL de la imagen**]({member.avatar_url})',  
            color = discord.Colour.green())
        embedAvatar.set_author(name=f"Avatar de: {member.name}#{member.discriminator}", icon_url=member.avatar_url)
        embedAvatar.set_image(url = member.avatar_url)
        embedAvatar.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}")
        await typing_sleep(ctx)
        await ctx.send(embed=embedAvatar)
        print(f"cmdAvatar||          Avatar de {member.name}#{member.discriminator} para {ctx.author.name}")

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """ Muestra los roles del servidor """
        allroles = ""

        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            allroles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t[ Users: {len(role.members)} ]\r\n"

        data = BytesIO(allroles.encode("utf-8"))
        await ctx.send(content=f"Roles del server **{ctx.guild.name}**", file=discord.File(data, filename=f"{default.timetext('Roles')}"))

    @commands.command(aliases=['join_date','fecha_unido','unido_el','unido','joined'])
    @commands.guild_only()
    async def joinedat(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f"**{user}** se unió a **{ctx.guild.name}**\n{default.date(user.joined_at)}"
        
        await typing_sleep(ctx)
        await ctx.message.delete()
        await ctx.send(embed=embed)
    
    @commands.command()
    async def password(self, ctx, nbytes: int = 18):
        """ 
        Comando que genera una contraseña segura y te la envia por md.
        El bot no guarda las contraseñas, esto puede ser verificado en el repositorio del bigobot.
        La misma es una cadena de texto URL-safe aleatoria y tendra una cantidad `nbytes` de bytes.
        La encriptacion utilizada es Base64, por ende en promedio cada byte resulta en 1,3 caracteres.
        """
        if nbytes not in range(3, 1401):
            await typing_sleep(ctx)
            return await ctx.send("El argumento **nbytes** debe ser un numero entre 3 y 1301!")
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await typing_sleep(ctx)
            await ctx.send(f"Te mandare un mensaje con la contraseña generada  **{ctx.author.name}**")
        await typing_sleep(ctx)
        await ctx.author.send(f"🎁 **Esta es tu contraseña:**\n`{secrets.token_urlsafe(nbytes)}`", delete_after=60.0)
        await ctx.author.send(f"Recuerda guardarla en un lugar seguro, estos mensajes se autoeliminaran en 1 minuto", delete_after=60.0)

    @commands.command()
    @commands.guild_only()
    async def mods(self, ctx):
        """ Chequea que moderadores estan activos en el server actual. """
        message = ""
        all_status = {
            "online": {"users": [], "emoji": "🟢"},
            "idle": {"users": [], "emoji": "🟡"},
            "dnd": {"users": [], "emoji": "🔴"},
            "offline": {"users": [], "emoji": "⚫"}
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} {' | '.join(all_status[g]['users'])}\n"

        await ctx.send(f"Mods en **{ctx.guild.name}**\n{message}")

    @commands.command(aliases=['sv_info','info_sv','guild_info','about_server','about_guild'])
    @commands.guild_only()
    async def info(self, ctx):
        """ Muestra información sobre el server actual. """
        embed2 = discord.Embed(
        title=f"{ctx.guild.name}",
        description="Un poco de info del sv",
        color=discord.Color.blue())

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        embed2.add_field(name=":calendar: *Sv creado el*", value=f'{ctx.guild.created_at.strftime("%d/%m/%Y, %H:%M:%S")}')
        embed2.add_field(name=":crown: Server *ADMIN*", value=f"{ctx.guild.owner}")
        embed2.add_field(name=":earth_americas: Region del server", value=f"{ctx.guild.region}", inline = False)
        embed2.add_field(name=":id: *Server ID*", value=f"{ctx.guild.id}")
        embed2.add_field(name=":family_mmbb: *Miembros totales*", value=f"{ctx.guild.member_count}")
        embed2.add_field(name=":family_mmbb: *Personas*", value=f"{len(list(filter(lambda m: not m.bot, ctx.guild.members)))}", inline = False)
        embed2.add_field(name=":robot: *Bots*", value=f"{len(list(filter(lambda m: m.bot, ctx.guild.members)))}")
        embed2.add_field(name=":scroll: *Roles*", value=f"{len(ctx.guild.roles)}")
        embed2.add_field(name=":traffic_light: *Estado de conexion*", value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", inline = False)
        embed2.add_field(name=":sound: Canales de voz", value=f"{len(ctx.guild.voice_channels)}")
        embed2.add_field(name=":speech_balloon: Canales de texto", value=f"{len(ctx.guild.text_channels)}")
        embed2.add_field(name=":no_entry: Baneos", value=f"{len(await ctx.guild.bans())}", inline = False)  
        embed2.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed2.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}")

        await typing_sleep(ctx)
        await ctx.send(embed=embed2)
        print(f'cmdInfo||      Info sobre {ctx.guild.name} enviada a {ctx.author.name}')   

    @commands.command(aliases=["icon", "guild_avatar", "guild_icon"])
    async def server_avatar(self, ctx):
        """ Envia el avatar del server. """
        if not ctx.guild.icon:
            return await ctx.send("Este servidor no tiene un avatar...")
        await ctx.send(f"Avatar de **{ctx.guild.name}**\n{ctx.guild.icon_url_as(size=1024)}")

    @commands.command(aliases=['cartel','banner','server_cartel','guild_banner'])
    async def server_banner(self, ctx):
        """ Envia el banner del server. """
        if not ctx.guild.banner:
            return await ctx.send("Este servidor no tiene un banner (requiere boost de 2 niveles -> 74,85USD/mes)...")
        await ctx.send(f"Banner de **{ctx.guild.name}**\n{ctx.guild.banner_url_as(format='png')}")

    @commands.command(aliases=['quien','user','user_info','member_info',''])
    @commands.guild_only()
    async def usuario(self, ctx, member: discord.Member = None):
        '''Informacion sobre @Mencion'''
        if member is None:
            await typing_sleep(ctx)
            await ctx.send("Seguido del comando debes @Mencionar a alguien")
            await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        
        fecha_Cumple = bro_birthdays_check(member.id)

        embedWho = discord.Embed(
            title = member.name, 
            description = member.mention, 
            color = discord.Colour.green())
        embedWho.add_field(name = "ID", value = member.id, inline = False)
        embedWho.add_field(name = "Cumple", value = fecha_Cumple, inline = False)
        embedWho.add_field(name = "Es bot?", value = member.bot, inline = False)
        embedWho.add_field(name = "Mayor Rol", value = member.top_role.mention, inline = False)
        embedWho.add_field(name = "Estado", value = str(member.status).title(), inline = False)
        embedWho.add_field(name = "Actividad", value = f"{str(member.activity.type).split('.')[-1].title() if member.activity else 'N/A'} {member.activity.name if member.activity else ''}", inline = False)
        embedWho.add_field(name = "Unido el", value = member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline = False)
        try:
            embedWho.add_field(name = "En discord desde", value = member.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline = False)
        except Exception:
            pass
        embedWho.set_thumbnail(url = member.avatar_url)
        embedWho.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}#{member.discriminator}")
        
        await typing_sleep(ctx)
        await ctx.send(embed=embedWho)
        print(f"cmdQuien||       Info sobre {member.name}#{member.discriminator} para {ctx.author.name}")

    @commands.command(aliases=['rol_n_col','rol_col','rolescolors'])
    async def roles_n_colors(self, ctx):
        '''Prints all roles with his respective HEX color, useful for dev's...'''
        roles_quantity = 0
        for role in ctx.guild.roles:
            await ctx.send(f" El rol '{role.name}' tiene un codigo de color HEX: {role.color}")
            roles_quantity += 1
        
        await typing_sleep(ctx)
        await ctx.send(f" {ctx.author.mention} recomiendo usar el comando *#borrar {roles_quantity}* para limpiar este desastre...")
        print(f"cmdRolesColors||     {ctx.author.name} requested the roles n colors")
    
    @commands.command()
    async def youtube(self, ctx, *, search):
        '''Busca un video de youtube y miralo, en discord android / ios se abre la app youtube'''
        try:
            query_string = parse.urlencode({'search_query': search})
            html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
            search_results = re.findall('/watch\?v=(.{11})', html_content.read().decode())
            # print(search_results) uncomment if you wanna see detailed results
            await typing_sleep(ctx)
            await ctx.send('https://youtube.com/watch?v=' + search_results[0])
            print(f'cmdYoutube||     {ctx.author.name} buscó el video {search} en yt')
        
        except Exception as e:
            if isinstance(e, commands.MissingRequiredArgument):
                await typing_sleep(ctx)
                await ctx.send("Seguido del comando debes introducir el nomber del video a buscar")
                await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y para ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")    
            else:
                await typing_sleep(ctx)
                await ctx.send(f":exclamation:  Hubo un error al ejecutar el comando. Info detallada:")
                await ctx.send(f"`Excepcion: {e}`\n`Razon: {e.args}`\n`Traceback: {e.with_traceback}`")

    @commands.command()
    async def descarga(self, ctx, url=None):   
        '''
        Introduce una url de un video de YT y se te redirigirá
        a otra pagina para descargar tal video en .mp3 o .mp4...
        '''
        if url != None:
            id = extract.video_id(url)
            downl_url = f"https://www.y2mate.com/es/convert-youtube/{id}"
            await typing_sleep(ctx)
            await ctx.message.delete()
            await ctx.send(f"Aqui esta el video listo para ser descargado: {downl_url}")
            print(f"cmdDescarga||            {ctx.author.name} descargo un video...")                
        else:
            await typing_sleep(ctx)
            await ctx.send("No se pudo convertir con exito el video...", delete_after=60.0)
            print(f"cmdDescarga||            {ctx.author.name} no pudo descargar un video...")     

    @commands.command()
    async def repite(self, ctx, *, arg=None):
        ''' Repito lo que escribas, con tts. '''
        if arg == None:
            await typing_sleep(ctx)
            await ctx.send("Seguido del comando, escribe lo que quieres que repita", tts=True, delete_after=20.0)
            print(f'cmdRepite||       {ctx.author.name} intentó repetir sin argumentos')
        else:
            await typing_sleep(ctx)
            await ctx.message.delete()
            await ctx.send(f"{str(arg)}", tts=True)
            print(f'cmdRepite||         {ctx.author.name} repitió "{arg}"')
    
    @commands.command()
    async def temporal(self, ctx, *, arg):
        '''Repite tu mensaje por 3 segundos y no queda rastro (aunque puede chusmearse con #chusmear)''' 
        await ctx.message.delete()
        ## send the message
        await typing_sleep(ctx)
        message = await ctx.send(arg, tts=True)
        ## wait for 3 seconds
        await sleep(3)  
        ## delete the message
        await message.delete()

    @commands.command()
    async def chusmear(self, ctx):
        '''Chusmea el ultimo mensaje borrado, de cualquier canal y de cualquier usuario'''
        try:
            contents, author, channel_name, time = self.bot.sniped_messages[ctx.guild.id]
            
        except:
            await ctx.channel.send("No encontré un mensaje para chusmear ◔̯◔")
            return

        embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Borrado de : #{channel_name}")

        await typing_sleep(ctx)
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['wikipedia'])
    async def wiki(self, ctx, lang:str='es', *, search):
        """
        Busca en wikipedia, lenguaje español por defecto. 
        para buscar en un lenguaje especifico introduce las iniciales del lenguaje
        ejemplo sintaxis: #wiki <lang> <tu busqueda>
        ejemplo 2: #wiki elon musk (al ignorar el 2do parametro "lang", busca por defecto en español)
        ejemplo 3: #wiki fr google (fr buscara en frances...)
        """
        try:
            wikipedia.set_lang(f"{lang}")
            result = wikipedia.summary(f"{search}")   
            if len(result) <= 2000:
                await typing_sleep(ctx)
                await ctx.send(f"```{result}```")
                print(f"cmdWikipedia||     {ctx.author.name} buscó en wikipedia: {search}")
                print(f" longitud de result : {len(result)} ")

            else:
                wikipedia.set_lang(f"{lang}")
                result = wikipedia.summary(f"{search}")
                result = result[:1996] + "..."
                await typing_sleep(ctx)
                await ctx.send(f"```{result}```")
                print(f"cmdWikipedia||     {ctx.author.name} buscó en wikipedia: {search}")

        except Exception as e:
            if isinstance(e, commands.MissingRequiredArgument):
                await ctx.send("Para una búsqueda correcta debes seguir la sintaxis **#wiki <lenguaje> <tu_busqueda>**. Para buscar en inglés -> en | Para buscar en español -> es | (símbolo del lenguaje)")
                await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
                print(f"cmdWiki||     {ctx.author.name} falló al buscar en wikipedia por falta de argumentos")
            else:
                print(e)

    @commands.command(aliases=['codigoqr'])
    async def qr(self, ctx, *, qrstring: str=None):
        '''
        ES: Crea y devuelve el QR de un texto, puede ser un texto cualquiera, URL, etc. 
        No funciona con imagenes y otro tipo de archivos, solamente texto.
        EN: Creates and returns a QR code of any text, images are not supported...'''
        if qrstring == None:
            await typing_sleep(ctx)
            await ctx.send(f'{ctx.author.mention} debes seguir la sintaxis #qr <texto a convertir> \n Solo funciona con textos, ej: urls, links, etc., no con numeros...')
            await sleep(15)
            await ctx.channel.purge(limit=2)  # elimina los 2 mensajes anteriores...
        
        elif qrstring != None:
            url = pyqrcode.create(qrstring)
            url.png('images/qr.png', scale=6)  # saves qr image
            await ctx.message.delete()
            await typing_sleep(ctx)
            await ctx.send(f'{ctx.author.mention} aca esta tu QR', file=discord.File('images/qr.png'))

        # openweathermap api key sensible stored in .env 
    
    api_key = os.getenv('OWM_API_KEY')
    @commands.command()
    async def clima(self, ctx, *, location: str=None):
        '''Clima de la ubicacion que introduzcas'''
        if location == None:
            await ctx.send('Debes seguir la sintaxis #clima <ubicacion>')
        elif location != None:
            location = str(location.lower())
            weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric' # change metric for imperial if u prefer degrees in farenheit
            try:
                # get the json 
                weather_json = requests.get(weather_url).json() 
                embed_weather = discord.Embed(
                        title=f'Clima en {location} ',
                        description=f'Asi esta el clima en {location}.',
                        color=discord.Colour.gold())
                if weather_json['weather'][0]['main'] == 'Clouds':
                        actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835639669030942/cloudy.png"
                        weather_traduction = "Nubes."
                elif weather_json['weather'][0]['main'] == 'Clear':
                        actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835642999046144/soleado.png"
                        weather_traduction = "Despejado."
                elif weather_json['weather'][0]['main'] == 'Rain':
                    actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835641904726016/lluvia.png"
                    weather_traduction = "Lluvia."
                
                # populate the json
                wind_direction = degrees_to_cardinal(weather_json['wind']['deg'])
                embed_weather.add_field(name="Estado", value=f"{weather_traduction}", inline=False)
                embed_weather.add_field(name="Temperatura", value=f"{weather_json['main']['temp']} °C", inline=False)
                embed_weather.add_field(name="Sensacion termica", value=f"{weather_json['main']['feels_like']} °C", inline=False)
                embed_weather.add_field(name="Temperatura minima", value=f"{weather_json['main']['temp_min']} °C", inline=False)
                embed_weather.add_field(name="Temperatura maxima", value=f"{weather_json['main']['temp_max']} °C", inline=False)
                embed_weather.add_field(name="Presion", value=f"{weather_json['main']['pressure']} mbar", inline=False)
                embed_weather.add_field(name="Humedad", value=f"{weather_json['main']['humidity']} %", inline=False)
                embed_weather.add_field(name="Velocidad del viento", value=f"{weather_json['wind']['speed']} km/h", inline=False)
                embed_weather.add_field(name="Direccion del viento", value=f"{wind_direction}", inline=False)
                embed_weather.set_thumbnail(url=f"{actual_state}")
                
                await typing_sleep(ctx)
                await ctx.send(embed=embed_weather)
                print(f'cmdClima||        {ctx.author.name} solicito el clima en {location}')

            except KeyError:
                await typing_sleep(ctx)
                error_embed = discord.Embed(title='Hubo un error', description=f'No fue posible encontrar el clima para {location}...')
                await ctx.send(embed=error_embed)
                print(f'cmdClima||        {ctx.author.name} fallo al solicitar el clima de {location}')

    @commands.command(aliases=["monsa", "dev", "desarrollador", "creador"])
    async def autor(self, ctx):
        '''Info sobre mi autor'''
        embedMine = discord.Embed(
            title="Acerca de mi",
            color=discord.Color.blurple()
        )
        embedMine.set_author(name="Juli Monsa", url="https://www.steamcommunity.com/id/JuliMonsa", icon_url="https://cdn.discordapp.com/attachments/793309880861458473/797528089726418974/yo_quien_mas.png")
        embedMine.add_field(name="Canal YT:", value=f" https://www.youtube.com/channel/UCeQLgYEcEj9PteUzWWa2bRA", inline= False)
        embedMine.add_field(name="Perfil de Steam:", value=f" https://www.steamcommunity.com/id/JuliMonsa", inline= False)
        embedMine.add_field(name="Github:", value=f" https://github.com/julimonsa0x", inline= False)
        embedMine.add_field(name="Telegram:", value=f" @julimonsa0x", inline= False)
        embedMine.add_field(name="Discord:", value=f" JuliTJZ#2364", inline= False)
        embedMine.add_field(name="Instagram: ", value=f" @0xjulimonsa", inline= False)
        embedMine.add_field(name="Replit:", value=f" https://repl.it/@julimonsa0x", inline= False)
        #embedMine.add_field(name="Página de", value=f"", inline= False)
        embedMine.set_thumbnail(url="https://i.imgur.com/mmF8hSX.png")  # ETHER ADDRESS 
        embedMine.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}")
        
        await ctx.message.delete()
        await typing_sleep(ctx)
        await ctx.send(embed=embedMine)
        print(f'cmdInfoSobreMí||         Info del autor enviada a {ctx.author.name}')

def setup(bot):
    bot.add_cog(ComandosGenerales(bot))