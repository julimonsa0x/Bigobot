# Python version 3.8.10
# .env file required by 5 variables
# read readme.md before starting
# ---------------------------------------->
import os
import sys
from discord.guild import Guild  # to get python version ????? who modified this ahh fuck pylance...
from dotenv import load_dotenv  # to get the .env TOKEN
# ----------------------------------------->  # discord.py fundamentals 
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot, errors
from discord.utils import get
#import DiscordUtils ---- > pip install but not required yet
import asyncio
# ----------------------------------------->  # Required Libraries 
import datetime
import json
import random
import re
import time
from datetime import date, datetime, time, timedelta
from io import BytesIO
from time import strftime
#import urllib3
from urllib import parse, request
import aiofiles
import aiohttp
#import certifi
import png
import requests
#from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from discord_slash import SlashCommand, SlashContext
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType


#<-------------------------------------------> Custom imports
import apis.listas
import apis.tuning
import game
from apis.functions import (degrees_to_cardinal, 
                       get_dolar, 
                       printt,
                       typing_sleep,
                       word_to_emoji,
                       bro_birthdays_check,
                       throw_error,
                       )

load_dotenv()

# ----------------------------------------> Beginning of code and some variables

now = datetime.now()

current_hora = now.strftime("%H:%M:%S")
current_hour = now.strftime("%d/%m/%Y, %H:%M:%S")  # mm/dd/YY H:M:S format
   
bot_developer_id = '485259816399536128' # that's me.

intents = discord.Intents.all() 


def get_prefix(bot, mssg):
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)
        #print(prefixes)
    return prefixes[str(mssg.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)


bigo_guild_id = 559592087054450690  # if bot is public, call the var "base_guild_id"
bigo_guild_base = bot.fetch_guild(bigo_guild_id)  # if bot is public, call the var "base_guild"


# --------> Bot en marcha <-------
@bot.event 
async def on_ready():
    
    ddb = DiscordComponents(bot)
    
    bot.reaction_roles = []
    bot.welcome_channels = {} # store like {guild_id : (channel_id, message)}
    bot.goodbye_channels = {}
    bot.sniped_messages = {}
    bot.ticket_configs = {}
    bot.warnings = {}
    #alphascript cmd

    #bot warnings.txt
    for guild in bot.guilds:
        async with aiofiles.open(f"databases/{guild.id}.txt", mode="a") as temp:
            pass

        bot.warnings[guild.id] = {}

    for file in ["databases/reaction_roles.txt", "databases/welcome_channels.txt", "databases/goodbye_channels.txt", "databases/ticket_configs.txt"]:
        async with aiofiles.open(file, mode="a") as temp:
            pass
    #alphascript cmd

    async with aiofiles.open("databases/reaction_roles.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))
    #alphascript cmd

    async with aiofiles.open("databases/welcome_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.welcome_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
    #alphascript cmd

    async with aiofiles.open("databases/goodbye_channels.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.goodbye_channels[int(data[0])] = (int(data[1]), " ".join(data[2:]).strip("\n"))
    #alphascript cmd

    async with aiofiles.open("databases/ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            bot.ticket_configs[int(data[0])] = [int(data[1]), int(data[2]), int(data[3])]
    #alphascript cmd

    for guild in bot.guilds:
        # Populate prefixes.json for every joined guild
        # prefixes.json must be an empty json by default
        with open("databases/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(guild.id)] = "#"
        with open("databases/prefixes.json", "w") as f:
            json.dump(prefixes,f, indent=2)
        print(f"Added the prefix `#` to {guild.name}!")
        
        # populate the joined_guilds apis.listas 
        try:
            apis.listas.joined_guilds.append(guild)
        except:
            pass

        # last, bot warnings.
        async with aiofiles.open(f"databases/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]

    
    # change presence of the bot and prints some info
    await bot.change_presence(
        activity=discord.Streaming(
        name="--> #ayuda",
        url="http://www.twitch.tv/slakun10")
    )
    printt('----------------------------------------------------->>>', 0.001)   
    printt(f" El bot fue logeado correctamente como: {bot.user} a las {current_hour} <¬", 0.001)
    printt(f" Nombre del bot: {bot.user.name} <¬", 0.001)
    printt(f" ID del bot: {bot.user.id} <¬", 0.001)
    printt(f" Estoy en {len(bot.guilds)} servidores! <¬", 0.001)
    printt(f" Con un total de {len(set(bot.get_all_members()))} miembros <¬", 0.001)
    printt(' |            author: JuliTJZ             |', 0.001)
    printt(' |          created : 23/12/2020          |', 0.001)
    printt(' |        last updated: 10/06/2021        |', 0.001)
    printt(f' |      Python: 3.8.10, Oct 14 2019       |', 0.001)
    printt(f' |          Discord.py:  {discord.__version__}            |', 0.001)
    printt('---------------------------------------------------->>>', 0.001)

    # connected message to "bigobot-testing" of Los Bigotazos
    channel = bot.get_channel(799387331403579462)
    await channel.send(f' :white_check_mark:  Connected at {current_hora} UTC')
    channel2 = bot.get_channel(791042478982824000)
    await channel2.send(f' :white_check_mark:  Connected at {current_hora} UTC')


##------> Statuses del Bot <--------
async def change_presence():
    await bot.wait_until_ready()
    # wait 35 secs. to start the change_presence loop...
    await asyncio.sleep(35)
    while not bot.is_closed():
        status = random.choice(apis.listas.bot_statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)

async def feliz_jueves():
    await bot.wait_until_ready()  
    await asyncio.sleep(60)  # wait for 1 min to start the weekly reminder

    while not bot.is_closed():

        # if json doesnt exists, create it.
        if not os.path.exists("json_files/felizjueves.json"):
            with open('json_files/felizjueves.json', 'w', encoding="utf8") as thu:
                content = '{"is_sent":false}'
                json.dump(content, thu, indent=2)
        
        # read the json to check if already sent
        with open('json_files/felizjueves.json', 'r', encoding="utf8") as thur:
            content = json.load(thur)
        is_sent = content["is_sent"]

        today_int = datetime.today().weekday()  # range 0 - 6 
        #date_sent = str(date.today())  # YYYY-MM-DD

        # if today is not thursday, wait 24hs.
        if not today_int == 3:
            print("====| Hoy no es jueves, esperando 24hs...")
            await asyncio.sleep(60 * 60 * 24)
        
        # if today IS thursday send message
        # and wait for a whole week to resend
        if today_int == 3:
            if (is_sent == "false") or (is_sent is False):
                
                general_bigos = await bot.fetch_channel(559592087641915433)
                
                try:
                    felizjuevesEmbed = discord.Embed(title=" :tada: **Feliz Jueves** :partying_face:")
                    felizjuevesEmbed.set_image(url='https://cdn.discordapp.com/attachments/793309880861458473/849848243662618644/Feliz_Jueves.mp4')
                    await general_bigos.send(embed=felizjuevesEmbed)
                    with open('json_files/felizjueves.json', 'w', encoding="utf8") as thursd:
                        content["is_sent"] = True
                        json.dump(content, thursd, indent=2)
                    print("====| Enviado con exito el feliz jueves mañanero semanal!")

                except Exception as e:
                    print(f"!!!Hubo un error al enviar el feliz jueves semanal: Excepcion:{e}\nCausa:{e.__cause__}\nTracebak{e.with_traceback()}")
                
                # wait for a whole week now
                await asyncio.sleep(60 * 60 * 24 * 7)

bot.loop.create_task(feliz_jueves())
bot.loop.create_task(change_presence())

############################################################################
##### ----------------->>>>  Comienzo de eventos  <<<<---------------- #####
@bot.event
async def on_message(msg):
    try:
        if (msg.split()[0] == bot.user) or (bot.user in msg.content):
            
            with open("databases/prefixes.json", "r") as f:
                prefixes = json.load(f)
            
            pre = prefixes[str(msg.guild.id)] 
            
            await msg.channel.send(
                f"Mi prefijo en este servidor es: {pre}\nPara cambiarlo usa: `{pre}changeprefix`.", 
                delete_after=30.0
            )
    
    except Exception as e:
        pass
        #print(f"Excepcion al mencionar al bot: {e}\n{e.args}")

    await bot.process_commands(msg)

# Required by json_level.py CONSIDER MOVING IT
@bot.event
async def on_guild_join(guild):
    # prefixes stuff for json_level.py
    with open("databases/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "#"
    with open("databases/prefixes.json", "w") as f:
        json.dump(prefixes,f, indent=2)
    
    # when bot joins a guild automatically 
    # append guild to lsit
    try:
        apis.listas.joined_guilds.append(guild)
    except:
        pass

    # when joined auto-send and set padlocked info
    await guild.send("#setpadlockedinfo", delete_after=20)    

@bot.event
async def on_raw_reaction_add(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            await payload.member.add_roles(bot.get_guild(payload.guild_id).get_role(role_id))
            return

    if payload.member.id != bot.user.id and str(payload.emoji) == "🎫":  #u"\U0001F3AB":
        msg_id, channel_id, category_id = bot.ticket_configs[payload.guild_id]

        if payload.message_id == msg_id:
            guild = bot.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_num = 1 if len(category.channels) == 0 else int(category.channels[-1].name.split("-")[1]) + 1
            ticket_channel = await category.create_text_channel(f"Ticket: {ticket_num}", topic=f"Canal creado para el ticket: {ticket_num}.", permission_synced=True)

            await ticket_channel.set_permissions(payload.member, read_messages=True, send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(f"{payload.member.mention} Gracias por crear un ticket, esta funcion es experimental y puede dar errores. Use **'-cerrar'** para cerrar el ticket :).")

            try:
                await bot.wait_for("message", check=lambda m: m.channel == ticket_channel and m.author == payload.member and m.content == "-cerrar", timeout=3600)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()

@bot.event
async def on_raw_reaction_remove(payload):
    for role_id, msg_id, emoji in bot.reaction_roles:
        if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
            guild = bot.get_guild(payload.guild_id)
            await guild.get_member(payload.user_id).remove_roles(guild.get_role(role_id))
            return
            #alphascript cmd

@bot.event # alphascript cmd
async def on_member_join(member):
    for guild_id in bot.welcome_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.welcome_channels[guild_id]
            cur_chan_members = len(bot.get_guild(guild_id).members)
            current_channel = bot.get_guild(guild_id).get_channel(channel_id)
            arrival = random.choice(apis.listas.new_arrival)
            try:
                await current_channel.send(f"{message} {member.mention}")
                await current_channel.send(f"{arrival} {member.mention} somos {cur_chan_members} miembros!")
                await current_channel.send(f"Recuerda explorar mis comandos con `#ayuda` o `#comandos`")
                return
            except Exception as e:
                printt(f"Hubo un error al mandar el mensaje de bienvenida: {e}\nTraceback{e.with_traceback}")

@bot.event # alphascript cmd
async def on_member_remove(member):
    for guild_id in bot.goodbye_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.goodbye_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{message} {member.mention}")
            return      

@bot.event # alphascript cmd
async def on_message_delete(message): 
    try:
        bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)
    except Exception as e:
        # ignora las excepciones del bigobot provenientes de un MD.
        if isinstance(e, AttributeError):
            pass
        else:
            print(f"El bot detecto un error debido a un mensaje borrado.\nExcepcion:{e}\nTraceback:{e.with_traceback()}\nArgs:{e.args}")
##### --------------->>>>  Finalizacion de eventos  <<<<-------------- #####
############################################################################


############################################################################
#### -------------->>>>  Acá comienzan los comandos  <<<<-------------- ####
@bot.command(aliases=['setpadlocked','setpadlockedinfo'])
@commands.has_permissions(administrator=True)
async def set_info_channels(ctx):
    """
    An admin/mod command only to set the padlocked info channels.
    For this command to work properly, create 3 private voice channels
    at the top of the guild with the role @everyone and the connect 
    voice permission set to false. After that copy the 3 id of the channels
    and replace the total_chan, real_chan and bot_chan variables with the 
    ids    
    """

    guild = ctx.guild
    if guild.id == bigo_guild_id:
        # create variables 
        total_members = guild.member_count
        real_members = len(list(filter(lambda m: not m.bot, guild.members)))
        bot_members = len(list(filter(lambda m: m.bot, guild.members)))
        # fetch channels
        total_chan = await bot.fetch_channel(846513178144931870)  # replace here with your copied ID
        real_chan = await bot.fetch_channel(846540695904452676)  # replace here with your copied ID
        bot_chan = await bot.fetch_channel(846540959177113610)  # replace here with your copied ID
        # edit channels
        try:
            await total_chan.edit(name=f"✔️ Miembros Totales: {total_members}")
            await real_chan.edit(name=f"🧍 Personas: {real_members}")
            await bot_chan.edit(name=f"🤖 Bots: {bot_members}")
        except Exception as e:
            await ctx.send(f":exclamation: Ocurio un error al ejecutar el comando: Info detallada:\n==========\n`Excepcion:{e}`\n`Razon:{e.args}`\n`Traceback:{e.with_traceback()}`", delete_after=180.0)

@bot.command(aliases=['reqticket','pedirticket'])
async def pedir_ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    '''Ideal para peticiones a admins y moderadores, la sintaxis puede verse al escribir el comando sin argumentos (#pedir_ticket a secas)'''
    if msg is None or category is None:
        await typing_sleep(ctx)
        await ctx.channel.send("Para que no haya errores, debes poner #pedir_ticket + <id del mensaje a reaccionar> + <id de la categoria de canales>")
        await ctx.channel.send("Este comando consiste en crear subcanales de ayuda, comando experimental...")
        return

    bot.ticket_configs[ctx.guild.id] = [msg.id, msg.channel.id, category.id] # this resets the configuration

    async with aiofiles.open("databases/ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("databases/ticket_configs.txt", mode="w") as file:
        await file.write(f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)
                

    await msg.add_reaction(u"\U0001F3AB")
    await typing_sleep(ctx)
    await ctx.channel.send("Sistema de tickets configurado exitosamente :thumbsup:") 
    #alphascript cmd

@bot.command()
async def ticket_menu(ctx):
    '''Muestra la info sobre #pedir_ticket'''
    try:
        msg_id, channel_id, category_id = bot.ticket_configs[ctx.guild.id]

    except KeyError:
        await ctx.channel.send("Todavía no has configurado el sistemas de tickets, para ello usa #pedir_ticket")

    else:
        embed = discord.Embed(title="Configuración del sistema de tickets", color=discord.Color.green())
        embed.description = f"**ID del mensaje a reaccionar** : {msg_id}\n"
        embed.description += f"**ID de la categoria de canal** : {category_id}\n\n"

        await ctx.channel.send(embed=embed)
        #alphascript cmd

@bot.command(aliases=['emoterol','rol_emote','rol_reaction','rol_react','rolreaction'])
@commands.has_permissions(administrator=True)
async def rol_reaccion(ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
    '''
    Creas un mensaje reaccionable para un determinado rol, quien reaccione a dicho mensaje obtendra tal rol 
    ejemplo de uso: #rol_reaccion Consiglieres 836026898584829963 :thumbsup: 
    '''
    if role != None and msg != None and emoji != None:
        try:    
            await msg.add_reaction(emoji)
            bot.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))

            async with aiofiles.open("databases/reaction_roles.txt", mode="a") as file:
                emoji_utf = emoji.encode("utf-8")
                await file.write(f"{role.id} {msg.id} {emoji_utf}\n") # TO_DO: improve file.write poor detailed content 

            await typing_sleep(ctx)
            await ctx.channel.send("Reacción definida con éxito :thumbsup:")
            print(f"cmdSetReaccion||       {ctx.author.name} definió la reaccion para el rol: {role}")
        
        except discord.errors.Forbidden:
            await typing_sleep(ctx)
            await ctx.send(f"Lo siento {ctx.author.name} pero no tienes permisos suficientes para realizar esta accion")

    else:
        await typing_sleep(ctx)
        await ctx.send("Argumentos no válidos, debe ser de la forma #comando <nombre del rol> <id del mensaje a reaccionar> <emoji>")
        await ctx.send("La idea de este comando es fijar un mensaje para que sea reaccionado y así obtener el rol asignado")
        await ctx.send(f"{ctx.author.mention} ten en cuenta que el nombre del rol debe ser identico al rol")
        print(f"cmdSetReaccion||          {ctx.author.name} falló al definir una reaccion para un rol")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_canal_bienvenida(ctx, new_channel: discord.TextChannel=None, *, message=None):
    '''
    ES: Asigna un canal de bienvenida junto a un mensaje, a modo de ejemplo: #set_canal_bienvenida <ID_del_canal_de_texto> <mensaje>
    Ejemplo practico: #set_canal_bienvenida 123423798689324 Bienvenido al server de _____.....
    Si no sabes como obtener el id de un canal debes tener activado el modo desarrollador. Para eso
    debes ir a Ajustes de Usuario > Avanzado > desarrollador. Esto habilitara la opcion de copiar el
    ID de un canal de texto cuando des click derecho en el mismo...
    
    EN: Assigns a welcome channel along a message, e.g: #set_canal_bienvenida <ID_del_canal_de_texto> <mensaje>
    Practical example: #set_canal_bienvenida 123423798689324 Welcome to _____'s guild.....
    If you are not able to copy the ID of a text channel you should activate developer mode. For that
    you gotta go to User settings > Advanced > Developer. Now you'll be able to copy a text channel's ID
    when right clicking it...
    '''
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.welcome_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"El canal de bienvenida ahora es: {channel.name}, y el mensaje de bienvenida será: \"{message}\"")
                await channel.send("¡Ahora este es el nuevo canal de bienvenida!")
                print(f"cmdCanaldeBienvenida||    {ctx.author.name} definió el canal de bienvenida a {channel.name}")

                async with aiofiles.open("databases/welcome_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("No pude encontrar ese canal :(")
        print(f"cmdCanaldeBienvenida|| {ctx.author.name} falló al setear un canal de bienvenida...")

    else:
        await ctx.channel.send("No incluiste el nombre del canal o el mensaje a setear")
        print(f"cmdCanaldeBienvenida|| {ctx.author.name} falló al setear un canal de bienvenida...")

@bot.command()
@commands.has_permissions(administrator=True)
async def set_canal_despedida(ctx, new_channel: discord.TextChannel=None, *, message=None):
    '''Asigna un canal de despedida junto a un mensaje'''
    if new_channel != None and message != None:
        for channel in ctx.guild.channels:
            if channel == new_channel:
                bot.goodbye_channels[ctx.guild.id] = (channel.id, message)
                await ctx.channel.send(f"El canal de despedida ahora es: {channel.name}, junto al mensaje: {message}")
                await channel.send("¡Este es el nuevo canal de despedida!")
                print(f"cmdCanaldeDespedida||    {ctx.author.name} definió el canal de despedida a {channel.name}")

                async with aiofiles.open("databases/goodbye_channels.txt", mode="a") as file:
                    await file.write(f"{ctx.guild.id} {new_channel.id} {message}\n")

                return

        await ctx.channel.send("No pude encontrar ese canal :(")
        print(f"cmdCanaldeDespedida||    {ctx.author.name} falló al setear un canal de Despedida...")

    else:
        await ctx.channel.send("No incluiste el nombre del canal o el mensaje a setear...")
        print(f"cmdCanaldeDespedida||    {ctx.author.name} falló al setear un canal de Despedida...")

@bot.command()
@commands.has_permissions(administrator=True)
async def advertencias(ctx, member: discord.Member=None):
    '''Muestra las advertencias de un @usuario'''
    if member is None:
        return await ctx.send("No he podido encontrar a ese miembro u olvidaste mencionarlo")
    
    embed = discord.Embed(title=f"Mostrando advertencias de {member.name}", description="", colour=discord.Colour.red())
    try:
        i = 1
        for admin_id, reason in bot.warnings[ctx.guild.id][member.id][1]:
            admin = ctx.guild.get_member(admin_id)
            embed.description += f"**Advertencia(s)  {i}**, dadas por {admin.mention}, razón: *'{reason}'*.\n"
            i += 1

        await ctx.send(embed=embed)

    except KeyError: # no warnings
        await ctx.send("Este usuario no cuenta con advertencias :thumbsup:")
        
@bot.command()
@commands.has_permissions(administrator=True)
async def advertir(ctx, member: discord.Member=None, *, reason=None):
    '''
    Advierte a un usuario junto a una razon, ideal para moderadores. 
    Comando experimental y no funcional al 100%
    Requerido permiso de administracion para poder usar el comando.
    '''
    warned =  member.id
    warner = ctx.author.id
    
    if member is None:
        return await ctx.send("No he podido encontrar a ese miembro u olvidaste mencionarlo.")
        
    if reason is None:
        return await ctx.send("Olvidaste la razón por la cual advertir a este usuario.")

    try:
        first_warning = False
        bot.warnings[ctx.guild.id][member.id][0] += 1
        bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

    except KeyError:
        first_warning = True
        bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

    count = bot.warnings[ctx.guild.id][member.id][0]

    # create the .txt warnings file. (base file)
    async with aiofiles.open(f"databases/{member.name}_adverts.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    warn_json = {
        "Warnings":[
            {
                "warn_no.": count,
                "warned_id": warned,
                "warner_id": warner,
                "reason": reason,
            }
        ]
    }

    new_warn = {    
        "warn_no.": count,
        "warned_id": warned,
        "warner_id": warner,
        "reason": reason
    }

    if first_warning:
        async with aiofiles.open(f"databases/{member.name}_adverts.json", "w") as file_json:
            await json.dump(warn_json, file_json, indent=4)

    if not first_warning:
        async with aiofiles.open(f"databases/{member.name}_adverts.json", "r+") as data_file:
            data = json.load(data_file)
            data = data["Warnings"][0]
            data.update(new_warn)
            #data_file.seek(0)
            await json.dump(data, data_file, indent=4)

    await typing_sleep(ctx)
    await ctx.send(f"{member.mention} tiene {count} {'advertencia' if first_warning else 'advertencias'}.")
    print(f"cmdAdvertir||      {ctx.author.name} advirtio a {member} por {count}° vez a las {current_hour}")



#-------------> RIP command <-----------------
@bot.command()
async def rip(ctx, member:discord.Member=None):
    '''Tumba de @alguien a quien menciones'''
    # first we put the member avatar pic
    if not member:
        member = ctx.author

    rip = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\rip.jpg")

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((112, 108))

    rip.paste(pfp, (72, 123))

    rip.save('images/prip.jpg')

    # then we add the dead date
    rip_image = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\prip.jpg")  
    lapiz = ImageDraw.Draw(rip_image)
    font_lapida = ImageFont.truetype(r'fonts/Roboto-Black.ttf', size = 25) 
    ripped_user = member.name
    titulo_lapida = "R I P"
    lapiz.text((101, 47), titulo_lapida, font = font_lapida, fill = "black")
    lapiz.text((70, 290), ripped_user, font = font_lapida, fill = "black")
    rip_image.save('images/prip2.jpg')


    await typing_sleep(ctx)
    await ctx.send(file = discord.File(r'images/prip2.jpg'))
    print(f'cmdRip||          {ctx.author.name} ripeo a {member} el {current_hour}')


#############
#############
def make_circular(im):
    offset = (im.width - im.height) // 2
    im = im.crop((offset, 0, im.height + offset, im.height))

    mask = Image.new("L", im.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + im.size, fill=255)

    out = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    out.putalpha(mask)
    return out


# -----> Make a user avatar circular.png <-----
@bot.command()
async def circular(ctx, user:discord.Member=None):
    if user is None:
        await ctx.send(":exclamation: You forgot to mention someone, try again.")
    
    if user != None:
        avatar = user.avatar_url_as(size = 1024) 
        avt = BytesIO(await avatar.read())
        imga = Image.open(avt)
        imguser = imga.resize((340, 340))  
        imguser.save("images/avatar_save2.png")


        with Image.open("images/avatar_save2.png") as im:
            im = im.convert("RGBA")

            circular_im = make_circular(im)
            circular_im.save("images/avatar_save2_circular.png")
        
        await typing_sleep(ctx)
        await ctx.send("Aqui esta la foto circular", file=discord.File('images/avatar_save2_circular.png'))


# ---> Welcome a user with a template <-----
@bot.command()
async def crear_template(ctx, member:discord.Member=None, *, content):
    if member != None:
        templat = Image.open('images/welcome_template.png')
        template = templat.copy()

        idraw = ImageDraw.Draw(template)
        title = ImageFont.truetype(r'fonts/Roboto-Black.ttf', size = 360)      # Title fonts
        subtitle = ImageFont.truetype(r'fonts/Roboto-Bold.ttf', size = 240)     # Subtitle fonts

        name = member.name

        idraw.text((493, 116), name, font = title, fill = "white")
        idraw.text((465, 600), content, font = subtitle, fill = "white")

        avatar_circ = Image.open('images/avatar_save2_circular.png')

        template.paste(avatar_circ, (122, 97))          
        template.save("images/final_template.png")    #saves the final photo with info

        await typing_sleep(ctx)
        await ctx.send("aqui esta el template", file=discord.File('images/final_template.png', spoiler=True))
##############
##############


#----------> Another PILLOW command <-----------
@bot.command()
async def profile(ctx, user: discord.Member = None):
    '''Muestra una foto con datos sobre un usuario @mencionado, comando en desarrollo y con bugs...'''
    if user == None:
        user = ctx.author

    image = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\profile.jpg")       #ORIGINAL ONE PS4
    img = image.resize((900, 500))                                                         #ORIGINAL ONE PS4
    #image = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\demo_city.png")       # USING DEMO_CITY, no .resize

    idraw = ImageDraw.Draw(img)      #ORIGINAL ONE PS4
    #idraw = ImageDraw.Draw(image)   # USING DEMO_CITY 
    title = ImageFont.truetype(r'fonts/Roboto-Black.ttf', size = 60)      # Title fonts
    subtitle = ImageFont.truetype(r'fonts/Roboto-Bold.ttf', size = 40)     # Subtitle fonts

    name = user.name
    namename = "En el server desde: " + user.joined_at.strftime("%d/%m/%Y")
    is_bot = user.top_role.mention
    memberid = user.id
    idraw.text((200, 30), name, font = title, fill = "white")
    idraw.text((200, 120), namename, font = subtitle, fill = "white")
    idraw.text((200, 210), is_bot, font = subtitle, fill = "white")
    idraw.text((200, 300), memberid, font = subtitle, fill = "white")
    
    avatar = user.avatar_url_as(size = 1024) 
    avt = BytesIO(await avatar.read())
    imga = Image.open(avt)
    imguser = imga.resize((100, 100))  
    imguser.save("images/avatar_save.png")
    
    #imguser_open = Image.open("images/avatar_save.jpg")
    
    img.paste(imguser, (50, 50))          
    img.save("images/profile_save.png")    #saves the final photo with info
    #image.paste(imguser_open, (50, 50))
    #image.save("images/profile_save2.png")    #this two lasts ones works with  the output one line 622
    
    await typing_sleep(ctx)
    await ctx.send(file = discord.File("images/profile_save2.png"))


#----------> Crear emoji desde una URL <--------
@bot.command()
async def crearemoji(ctx, url_emoji=None, *, name):
    '''
    Crea un emote a partir de una URL, aconsejable un formato menor de 512x512.
    Si desconoces el tamaño de la imagen probablemente no se cree el emoji...
    Aconsejable que la URL sea directo a una imagen y no a una pagina en si.
    '''
    if url_emoji == None:
        await ctx.message.delete()
        await typing_sleep(ctx)
        await ctx.send("Debes seguir esta sintaxis: #crearemoji <url> <nombre_del_emoji>")
    
    elif url_emoji != None:
        guild = ctx.guild
        if ctx.author.guild_permissions.manage_emojis:
            r = requests.get(url_emoji)
            img = Image.open(BytesIO(r.content), mode='r')
            try:
                img.seek(1)

            except EOFError:
                is_animated = False

            else:
                is_animated = True

            if is_animated == True:
                await ctx.message.delete()
                await typing_sleep(ctx)
                await ctx.send("No pueden crearse emojis animados!")

            elif is_animated == False:
                try:
                    b = BytesIO()
                    img.save(b, format='PNG')
                    b_value = b.getvalue()
                    emoji = await guild.create_custom_emoji(image=b_value, name=name)
                    await ctx.message.delete()
                    await typing_sleep(ctx)
                    await ctx.send(f'Emoji creado satisfactoriamente, aquí está: <:{name}:{emoji.id}> y su id es:\n`<:{name}:{emoji.id}>`')
                    print(f"cmdCrearEmoji||     {ctx.author.name} creo el emoji custom '{name}' ")
                
                except Exception as e:
                    await typing_sleep(ctx)
                    await ctx.message.delete()
                    await ctx.send("Hubo un error al tratar de crear el emote, lo mas probable es que su resolucion sea mayor a 512x512... Detalles del error enviada al canal del bigobot")
                    exception = f"`Excepcion causada:{e}`\n`Razon:{e.args}`\n`Traceback:{e.with_traceback()}`"
                    bigobot_chann = 799387331403579462
                    bigobot_channel = await bot.fetch_channel(bigobot_chann)
                    await bigobot_channel.send(exception)

@crearemoji.error
async def crearemoji_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltan argumentos, debes seguir la sintaxis #crearemoji <url_de_la_imagen_a_convertir> <nombre_del_emoji>. Recuerda tener espacio suficiente en el servidor para emojis y que no sea .gif")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y para ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        print(f"cmdCrearEmoji||      {ctx.author.name} fallo al crear un emoji ")
    else:
        pass


@slash.slash(description="Comando de prueba")
async def testcmd(ctx: SlashContext):
    await ctx.send(content="Working!")


@slash.slash(description="comando test buttons")
async def testButtons(ctx):
    m = await ctx.send(
        components = [
            [
                Button(style=ButtonStyle.blue, label="click test"),
                Button(style=ButtonStyle.URL, label="Repositorio", url="https://github.com/julimonsa0x/Bigobot"),
                Button(style=ButtonStyle.URL, label="Invitame a tu sv :robot:", url="https://discord.com/api/oauth2/authorize?client_id=788950461884792854&permissions=8&scope=bot%20applications.commands"),
            ],
        ],
    )
    while True:
        interaction = await bot.wait_for("button_click")
        await interaction.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f":white_check_mark: {interaction.button.label} has been clicked!"
        )
        await ctx.send(content=" :white_check_mark: another message!")


@bot.command()
async def testButton(ctx):
    m = await ctx.send(
        components = [
            Button(style=ButtonStyle.blue, label="click test"),
            Button(style=ButtonStyle.URL, label="Repositorio", url="https://github.com/julimonsa0x/Bigobot"),
            Button(style=ButtonStyle.URL, label="Invitame a tu sv :robot:", url="https://discord.com/api/oauth2/authorize?client_id=788950461884792854&permissions=8&scope=bot%20applications.commands"),
        ]
    )
    while True:
        interaction = await bot.wait_for("button_click")
        await interaction.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f":white_check_mark: {interaction.button.label} has been clicked!"
        )
        await ctx.send(":white_check_mark:")


#-------->COMANDOS DE AYUDA inicio<----------
#----> menu de comandos <---- 
@bot.command()
async def comandos(ctx):
    ''' Lista casi completa de los comandos del bigobot '''
    embedCmd = discord.Embed(
        color=discord.Colour.orange(),
        title=f"Menu de comandos a tu orden {ctx.author.name} :thumbsup:",
        description='Si prefieres una ayuda mas personal, escribe "#ayuda"',
        timestamp=ctx.message.created_at
    )
    embedCmd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/794724078224670750/25884936-fd9d-4627-ac55-d904eb5269cd.png") #icono del bigobot
    embedCmd.add_field(name="Recordatorio sobre uso el bigobot", value="Los comandos son sensibles a las mayusculas, no es lo mismo `#meme` que `#MEME`...", inline=False)
    embedCmd.add_field(name="-->Categoria #ofertas", value="Busca ofertas de juegos en 5 distintas plataformas, accede a la lista completa con **#help OfertasJuegos** ", inline=False)
    embedCmd.add_field(name="-->Comando #matecomandos", value="operaciones que puede resolver el bot a detalle", inline=False)
    embedCmd.add_field(name="-->Categoria  #dolar_cot", value="Busca la cotizacion del dolar y calcula el dolar tarjeta (ideal para compras online, incluyendo impuestos). Accede a la lista completa con **#help DolarCotizacion**", inline=False)
    embedCmd.add_field(name="-->Categoria  #comandos_generales", value="Diversos comandos multipropositos como `#avatar`, `#info`, `#usuario`, `#youtube`, `#repite` y mas. Accede a la lista completa con **#help ComandosGenerales**", inline=False)
    embedCmd.add_field(name="-->Categoria  #fun_stuff", value="Comandos varios divertidos, acceder a la lista completa con **#help FunCommands**", inline=False)
    embedCmd.add_field(name="-->Comando  #help", value="Lista de todas las categorias y todos los comandos", inline=False)
    embedCmd.add_field(name="-->Comando  #ping", value="Muestra tu latencia con respecto al bot", inline=False)
    embedCmd.add_field(name="-->Comando #reacciona, #...", value="Este y muchos otros comandos en ----> #moar", inline=False)
    embedCmd.add_field(name="-->Sugerencia", value="Comandos detallados por seccion con #ayuda", inline=False)
    embedCmd.set_footer(text = "Listo para ayudarte ;)/🥂")

    await typing_sleep(ctx)
    await ctx.send(file=discord.File('images/comandos.png'))
    await ctx.send(embed=embedCmd)
    print(f"cmdComandos||   Comandos de ayuda enviados correctamente a {ctx.author.name} a las {current_hour}")

# menu #moar para las "interacciones" del bot
# comando especifico para Los Bigotazos
@bot.command()
async def moar(ctx): 
    '''Comandos no mencionados en #comandos'''
    if ctx.guild == bigo_guild_base or ctx.guild == bigo_guild_id:
        embedMoar = discord.Embed(
            color=discord.Colour.green(),
            title="Estas son las demás interacciones del bot",
            timestamp=datetime.utcnow()
        )
        embedMoar.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/794724078224670750/25884936-fd9d-4627-ac55-d904eb5269cd.png") #icono del bigobot
        embedMoar.add_field(name="Interacción #mato", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #rubén", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #claudia", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #lezca", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #lesca", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #nico", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #seki", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #ey", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #flaco", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #che", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #copi", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #tevenin", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #hola", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #firu", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #pepo", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Interacción #pistero", value="El bot interacciona/habla", inline=False)
        embedMoar.add_field(name="Comando  #tadeo", value="que mas puede ser, que se te ocurre osea...", inline=False)
        embedMoar.add_field(name="Comando  #galosniper", value="galo sniper", inline=False)
        embedMoar.add_field(name="Comando  #willy", value="willy out of context", inline=False)
        embedMoar.add_field(name="Comando  #locurabailando", value="muestra *locurabailandosinpantalones.mp4* ", inline=False)
        embedMoar.add_field(name="y muchos mas", value="Simplemente probá con los nombres de los bros o con otra cosa, sin olvidar el prefijo #", inline=False)
        
        await typing_sleep(ctx)
        await ctx.send(embed=embedMoar)
        print(f"cmdMoar||      Mas interacciones enviadas correctamente a {ctx.author.name} a las {current_hour}")

    
@bot.command()
async def ayuda(ctx):
    '''Te manda un MD con los comandos'''
    author = ctx.message.author #define al autor del mensaje quien pide la ayuda
    embed_help = discord.Embed(
        colour=discord.Colour.orange(),
        title='Estos son los comandos disponibles ',
        timestamp=datetime.utcnow(),
    )
    #embed_help.set_author(name=f"Menu de comandos a tu orden {ctx.author.name}")
    embed_help.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/794724078224670750/25884936-fd9d-4627-ac55-d904eb5269cd.png") #icono del bigobot
    embed_help.add_field(name="--> Comandos interactivos ", value="Por ejemplo #juegos, #dados, #trivia, #randomchamp, #randombrawl, #ppt, #meme, y mucho mas...", inline=False)
    embed_help.add_field(name="--> Comandos sobre videos ", value="#pistero, #tadeo, #golaso, #spider, #locurabailando, #galosniper, #roast, #willy")
    embed_help.add_field(name="--> Comandos útiles ", value="#dolar, #qr, #steamcito, #info, #clima, #youtube, #letras, #fb_post, #chusmear, #descarga, #repite, #tunear, #wiki, #crearemoji", inline=False)
    embed_help.add_field(name="--> Comandos para admins ", value="#advertir, #advertencias, #kick, #ban, #set_canal_bienvenida, #set_canal_despedida, #pedir_ticket, #rol_reaccion, #setdelay", inline=False)
    embed_help.add_field(name="--> Comandos matemáticos", value="#matecomandos", inline=False)
    embed_help.add_field(name="--> Comandos de conversion", value="#bin_a_dec, #dec_a_bin, #hex_a_dec, #dec_a_hex, #num_a_rom", inline=False)
    embed_help.add_field(name="--> Ayuda de un comando especifico", value="#help <comando>, a modo de ejemplo si quieres ver la ayuda del comando #descarga, seria: `#help descarga`...")
    embed_help.set_footer(text = "Listo para ayudarte ;)/🥂", icon_url=ctx.author.avatar_url)
    
    await typing_sleep(ctx)
    await author.send(file=discord.File('images/ayuda.png'))
    await author.send(embed=embed_help, delete_after = 360.0)
    print(f"cmdAyuda||   Ayuda de comandos solicitada por {ctx.author.name} a las {current_hour}")
#-------->COMANDOS DE AYUDA fin<----------


#------------------------------------------>>>>>
###-------------- Operaciones Matemáticas final ------------>>>>

#------> Slow Mode command <------
@bot.command()
@commands.has_permissions(kick_members=True)
async def setdelay(ctx, seconds: int):
    '''Define el modo lento a una cantidad determinada, debes tener permisos suficientes (kick permissions al menos)'''
    await ctx.channel.edit(slowmode_delay=seconds)
    await typing_sleep(ctx)
    await ctx.send(f"El modo lento ha sido definido en {seconds} segundos!")

@setdelay.error
async def setdelay_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await typing_sleep(ctx)
        await ctx.send("Debes seguir la sintaxis #setdelay <segundos>, para desactivar el modo lento el argumento <segundos> debe ser cero")

#---> MD a usuario 12 con ID <---
@bot.command()
@commands.has_permissions(administrator=True)
async def md(ctx, user_id=None, *, args=None):
    '''Envia un MD a una ID, solo funciona con ID's de usuarios...'''
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id) #fetch_user convierte una ID dada a su apodo (nombre de usuario sin #id)
            await typing_sleep(ctx)
            await target.send(args)
            await ctx.channel.send(f"Le enviaste un md con éxito a: {target.name}")
            print(f"cmdMD||       {ctx.author.name} le envió un md a {target.name} diciendole: {args} a las {current_hour}")
        except:
            await typing_sleep(ctx)
            await ctx.channel.send("No se pudo enviar el md, este comando funciona con ID y no con @Mención")       
    else:
        await typing_sleep(ctx)
        await ctx.channel.send("Debes proporcionar una ID, seguido del mensaje a enviar!")
        print(f"cmdMD||        {ctx.author.name} falló al enviar un md")

#---> DM a usuarios con @mencion <---
@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, member_mention: discord.Member, *, args=None):
    '''Envia un MD a un @usuario, solo funciona con @menciones...'''
    if member_mention != None or args != None:
        try:
            await member_mention.send(args)
            await typing_sleep(ctx)
            await ctx.channel.send(f"Le enviaste un md con éxito a: {member_mention.name}")
            print(f"cmdMD||    {ctx.author.name} le envió un md a {member_mention.name} diciendole: {args} a las {current_hour}")
        except:
            await typing_sleep(ctx)
            await ctx.channel.send("No se pudo enviar el dm, este comando funcion con @Mención y no con ID")       
    else:
        await typing_sleep(ctx)
        await ctx.channel.send("Debes @mencionar un usuario, seguido del mensaje a enviar!")
        print(f"cmdMD||     {ctx.author.name} falló al enviar un md")


#---> Mensajes a canales con el bot 13<---
@bot.command()
@commands.has_permissions(administrator=True)
async def mensaje(ctx, channel_id=None, *, args=None):
    '''Envia un mensaje a un canal con su ID, sintaxis #mensaje <id_del_canal> <mensaje_aqui>'''
    if channel_id != None and args != None:
        try:
            target = await bot.fetch_channel(channel_id) #fetch_channel utilizado una ID de un canal dado para poder usar target.name
            await target.send(args)
            await typing_sleep(ctx)
            await ctx.channel.send(f"Enviaste un mensaje con éxito a: {target.name}")
            print(f"cmdMensaje||       {ctx.author.name} le envió un mensaje a {target.name} diciendole: {args} ")
        except:
            await typing_sleep(ctx)
            await ctx.channel.send("No se pudo enviar el mensaje.")       
    else:
        await typing_sleep(ctx)
        await ctx.channel.send("Debes proporcionar una ID de un canal, seguido del mensaje a enviar!")
        print(f"cmdMensaje||       {ctx.author.name} falló al enviar un mensaje")

#----------> Kick Command <---------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    '''Kick a un usuario, requiere permisos'''

    await typing_sleep(ctx)
    msg = await ctx.channel.send(f"Estas seguro que quieres kickear a {member}?")
    await msg.add_reaction(u"\u2705") # emoji OK
    await msg.add_reaction(u"\U0001F6AB") # emoji NO

    try:
        reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=10)

    except asyncio.TimeoutError:
        await typing_sleep(ctx)
        await ctx.channel.send("Pasaron 10 segundos, me fui a la bosta amigo/a")
        print(f"cmdKick||      {member} iba a ser kickeado {ctx.author.name} pero safo")

    else:
        if reaction.emoji ==  u"\u2705":
            await typing_sleep(ctx)      
            embed = discord.Embed(
                title=f"Kickeado porque {random.choice(apis.listas.frases)}",
                colour=0x2859B8,
                description=f"{member.mention} fue kickeado del server."
            )
            await member.kick(reason=reason)
            await ctx.send(embed=embed)
            print(f"cmdKick||      {member} fue kickeado correctamente por {ctx.author.name} el {current_hour} ")

        else:
            await typing_sleep(ctx)
            await ctx.channel.send(f"{member} no fue kickeado y safó...")
            print(f"cmdKick||      {member} iba a ser kickeado {ctx.author.name} pero safo")

#----------> Ban Command <---------
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    '''Banea a un usuario, requiere permisos. Argumento reason opcionable.'''
    await typing_sleep(ctx)
    msg = await ctx.channel.send(f"Estas seguro que quieres **banear** a {member}?")
    await msg.add_reaction(u"\u2705")
    await msg.add_reaction(u"\U0001F6AB")

    try:
        reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=10)

    except asyncio.TimeoutError:
        await typing_sleep(ctx)
        await ctx.channel.send("Pasaron 10 segundos, me tome el palo amigo/a")
        print(f"cmdBan||        {member} iba a ser baneado {ctx.author.name} pero safo")

    else:
        if reaction.emoji ==  u"\u2705":
            await typing_sleep(ctx)      
            embed = discord.Embed(
                title=f"Baneado porque {random.choice(apis.listas.frases)}",
                colour=0x2859B8,
                description=f"{member.mention} fue **baneado** del server."
            )
            await member.ban(reason=reason)
            await ctx.send(embed=embed)
            print(f"cmdBan||        {member} fue baneado correctamente por {ctx.author.name} el {current_hour} ")

        else:
            await typing_sleep(ctx)
            await ctx.channel.send(f"{member} no fue baneado asi que safo")
            print(f"cmdBan||        {member} iba a ser baneado {ctx.author.name} pero safo")


#------------>  interaccion con el bot   <---------------
@bot.listen('on_message')
async def on_message(message):
    msg = message.content
    if msg.startswith('#reacciona') or msg.startswith('#reaccion'):
        channel = message.channel
        await channel.send('mandame un 👍 capo (si o si amarillo)')
        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=20.0, check=check) #bot.wait_for was client.wait_for
        except asyncio.TimeoutError:
            await channel.send('👎')
        else:
            await channel.send('🧉' + '<:copi:770818273217609758>' + '<:doble:774509983832080385>')
            return
    if message.author == bot.user:  # to ignore bot messages
        return
    if msg.startswith('#che'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    if msg.startswith('#bot'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    if msg.startswith('#bigobot'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    if msg.startswith('#copibot'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    elif msg.startswith('#ey'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    elif msg.startswith('#tevenin'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    elif msg.startswith('#capo'):
        await message.channel.send("{}".format(random.choice(apis.listas.botCall)))
    elif msg.startswith('#claudia'):
        await message.channel.send(word_to_emoji("claudia"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.lacla)))
    elif msg.startswith('#flaco'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.botCall)))
    elif msg.startswith('#ruben'):
        await message.channel.send(word_to_emoji("ruben"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.rubenes)))
    elif msg.startswith('#pibe'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.botCall)))
    elif msg.startswith('#rubén'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.rubenes)))
    elif msg.startswith('#nico'):
        await message.channel.send(word_to_emoji("nico"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.nicolas)))
    elif msg.startswith('#seki'):
        await message.channel.send(word_to_emoji("seki"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.sekiam)))
    elif msg.startswith('#franc'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.sekiam)))
    elif msg.startswith('#franki'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.sekiam)))
    elif msg.startswith('#copi'):
        await message.channel.send(word_to_emoji("copi"))
        await message.channel.send(word_to_emoji("pedro"))
    elif msg.startswith('#hola'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.botCall)))
    elif msg.startswith('#Hola'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.botCall)))
    elif msg.startswith('#claudio'):
        await message.channel.send('ese está en plaza huincul')
    elif msg.startswith('#hentai'):
        await message.channel.send('sos pajin eh :alien:')
    elif msg.startswith('#mato'):
        await message.channel.send(word_to_emoji("mato"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.matote)))
    elif msg.startswith('#matu'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.matote)))
    elif msg.startswith('#Mato'):
        await message.channel.send("{}".format(random.choice(apis.apis.listas.matote)))
    elif msg.startswith('#lezca'):
        await message.channel.send(word_to_emoji("lezca"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.inválido)))
    elif msg.startswith('#lesca'):
        await message.channel.send(word_to_emoji("lesca"))
        await message.channel.send("{}".format(random.choice(apis.apis.listas.inválido)))
    elif msg.startswith('#firu'):
        await message.channel.send(word_to_emoji("firu"))
        await message.channel.send("wof wof xd")
    elif msg.startswith('#ursula'):
        await message.channel.send('gorda mala leche como dijeron <@!343963045682216960> y <@!343971450644070410>') #primero el tambo segundo el nico
    elif msg.startswith('-monsa'):
        await message.channel.send('mi creador')
    elif msg.startswith('#menem'):
        await message.channel.send(word_to_emoji("menem"))
        await message.channel.send('se movió a la bolocco ese un capo')
    elif msg.startswith('-Monsa'):
        await message.channel.send('un distinto')
    elif msg.startswith('-tadeo'):
        await message.channel.send('gordo puto, por cierto, con "#tadeo" pones el video ( ͡° ͜ʖ ͡°) 🚴‍♂️')
    elif msg.startswith('#costi'):
        await message.channel.send(word_to_emoji("costi"))
        await message.channel.send('un carnasa 🐕')
    elif msg.startswith('#pela'):
        await message.channel.send('un capo')
    elif msg.startswith('#tambo'):
        await message.channel.send(word_to_emoji("tambo"))
        await message.channel.send("{}".format(random.choice(apis.listas.tamborindegui)))
    elif msg.startswith('#tobo'):
        await message.channel.send(word_to_emoji("tobo"))
        await message.channel.send("{}".format(random.choice(apis.listas.tamborindegui)))
    elif msg.startswith('#pepo'):
        await message.channel.send('ese tambien es puto')
    elif msg.startswith('#puto'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('Chupala bigob') or msg.startswith('chupala bigob'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#tonto'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#trolo'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#gil'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#forro'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#bigote'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#tuma'):
        await message.channel.send("{}".format(random.choice(apis.listas.bardeo)))
    elif msg.startswith('#jose'):
        await message.channel.send(word_to_emoji("jose"))
        await message.channel.send("{}".format(random.choice(apis.listas.jopiyo)))
    elif msg.startswith('#jopi'):
        await message.channel.send(word_to_emoji("jopi"))
        await message.channel.send("{}".format(random.choice(apis.listas.jopiyo)))
    elif msg.startswith('#Jopi'):
        await message.channel.send("{}".format(random.choice(apis.listas.jopiyo)))
    elif msg.startswith('#Nico'): 
        await message.channel.send(word_to_emoji("nico"))
        await message.channel.send("{}".format(random.choice(apis.listas.nicolas)))
    elif msg.startswith('#reteke'): 
        await message.channel.send(word_to_emoji("reteke"))
        await message.channel.send("{}".format(random.choice(apis.listas.aquitocartes)))
    elif msg.startswith('#rtk'): 
        await message.channel.send("{}".format(random.choice(apis.listas.aquitocartes)))
    elif msg.startswith('#aquito'): 
        await message.channel.send("{}".format(random.choice(apis.listas.aquitocartes)))
    elif msg.startswith('#wens'): 
        await message.channel.send(word_to_emoji("wensel"))
        await message.channel.send("{}".format(random.choice(apis.listas.nicolas)))  
    elif msg.startswith('#ecla'): 
        await message.channel.send(word_to_emoji("ecla"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#beje'): 
        await message.channel.send(word_to_emoji("beje"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#sofi'): 
        await message.channel.send(word_to_emoji("sofi"))
        await message.channel.send("{}".format(random.choice(apis.listas.sofia)))
    elif msg.startswith('#araragi'):
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#dante'):
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#masilo'):
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#sousken'):
        await message.channel.send(word_to_emoji("souskenin"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#stalker'):
        await message.channel.send(word_to_emoji("stalker"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#ecla'):
        await message.channel.send(word_to_emoji("ecla"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#komiwa'):
        await message.channel.send(word_to_emoji("komiwa"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#krivta'):
        await message.channel.send(word_to_emoji("krivta"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#fiktizio'):
        await message.channel.send(word_to_emoji("fiktizio"))
        await message.channel.send("{}".format(random.choice(apis.listas.asociados)))
    elif msg.startswith('#among'):
        await message.channel.send(word_to_emoji("amongo"))
        await message.channel.send("{}".format(random.choice(apis.listas.amongo)))
    elif msg.startswith('#waif'):
        await message.channel.send(word_to_emoji("waifu"))
        await message.channel.send("{}".format(random.choice(apis.listas.waifu)))   
    elif msg.startswith('#pecetote'): 
        await message.channel.send(word_to_emoji("pecetote"))
        await message.channel.send("rey de reyes")
        return

    if msg.startswith('#copipedro'):
        channel = message.channel
        await channel.send('<:copi:770818273217609758>')
        return


#---------> juego command <--------
@bot.command()
async def juegos(ctx):
    '''ta te ti y otros juegos (otros juegos estan por venir)'''
    await game.LoadGames(ctx, bot)    

@bot.command()
async def ppt(ctx, member : discord.Member=None):
    '''Piedra papel o tijeras contra jugador que menciones'''
    try:
        await game.ppt(ctx, bot, member=member)
    except AttributeError as e:
        await typing_sleep(ctx)
        await ctx.send("Hubo un error :disappointed:")
        await ctx.send(f"```Excepcion:{e}\n\nTraceback:{e.with_traceback()}\n\nCausa:{e.args}```")
        print("pptCmd||        Ocurrio un error en el comando ppt considera echar un ojo")
#-------> juego command end <------

            
# ---------> Purge messages of a mentioned user <--------
@bot.command()
async def borrar(ctx, limit=10, member: discord.Member=None):
    '''
    Borra una cantidad determinada de mensajes, por defecto 10 mensajes pero puedes establecer una 
    cantidad. 
    El argumento <member> pemite borrar especificamente los mensajes de dicho miembro @mencionado.
    Por ejemplo: [#borrar] <cantidad_de_mensajes_que_deseas_borrar> <usuario_de_quien_borrar_mensajes>
    Usar el comando a secas causara una eliminacion de 10 mensajes por defecto. 
    [#borrar] <10> <@usuario_c> causara una eliminacion de los ultimos 10 mensajes del usuario_c....
    '''
    try:
        await ctx.message.delete()  # borra el mensaje del autor al escribir el comando
        msg = []
        try:
            limit = int(limit)     
        except:
            return await ctx.send('Se requiere de un numero para el limite de mensajes a borrar!' + '\n' + 'recuerda seguir la sintaxis #borrar **<cantidad de mensajes a borrar>**')
        if not member:
            await ctx.channel.purge(limit=limit)
            await typing_sleep(ctx)
            return await ctx.send(f":wastebasket: {limit} mensaje(s) borrado(s)", delete_after=10)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await typing_sleep(ctx)
        await ctx.send(f":wastebasket: {limit} mensajes borrados de {member.mention}", delete_after=12)
    
    except Exception as e:
        # check if the msg is older than 2 weeks
        if isinstance(e, errors.CommandInvokeError):
            await typing_sleep(ctx)
            await ctx.send(f":exclamation: {ctx.author.name} solo es posible borrar mensajes con menos de 14 dias de antiguedad...")
        if isinstance(e, errors.BadArgument):
            await typing_sleep(ctx)
            await ctx.send(f":exclamation: {ctx.author.name} esa no es la sintaxis correcta del comando, utiliza `#help borrar`!")
        # otherwise send the name and reason of the exception
        else:
            await typing_sleep(ctx)
            await ctx.send(f":exclamation:  Hubo un error al ejecutar el comando. Info detallada:")
            await ctx.send(f"`Excepcion: {e}`\n`Razon: {e.args}`\n`Traceback: {e.with_traceback()}`")


@slash.slash(description="comando de prueba para submit")
async def submit(ctx, titulo:str, mensaje:str, log=False):
    """
    4th argument log if true shows whole log, default False.
    """
    if not os.path.exists("json_files/submit_data.json"):
        with open('json_files/submit_data.json', 'w', encoding="utf8") as fil:
            fil.write("{}")

    if titulo and mensaje:
        try:
            with open('json_files/submit_data.json', 'r', encoding="utf8") as pepe:
                content = json.load(pepe)
            content[titulo] = mensaje
            with open('json_files/submit_data.json', 'w', encoding="utf8") as pepePepe:
                json.dump(content, pepePepe, indent=2)
            if log:
                await ctx.send(file=discord.File("json_files/submit_data.json", filename="submit_data.json"))
            await ctx.send(content=" :white_check_mark: datos guardados correctamente!")
        except:
            await ctx.send(content="Hubo un error con el comando /submit")
    else:
        await typing_sleep(ctx)
        await ctx.send(content="Faltan argumentos para el comando, utiliza `#help submit` para ver los argumentos que espera la función")



# cog loader cmd
# bot_developer_id Variable is at top of file
@bot.command()
async def load(ctx, extension):
    '''
    Loads an specific cog, developer only atm! 
    Don't include the .py extension!
    '''
    id = str(ctx.author.id)
    if id == bot_developer_id:
        bot.load_extension(f'cogs.{extension}')
        await typing_sleep(ctx)
        await ctx.send(f"{ctx.author.name} cargaste el cog {extension} con exito")
        print(f'cmdLoad||     El cog {extension}.py fue cargado con exito')
    else:
        await typing_sleep(ctx)
        await ctx.send("Solo el desarrollador puede cargar/habilitar los cogs del bot")

# cog unloader cmd
@bot.command()
async def unload(ctx, extension):
    '''
    Unloads an specific cog, developer only!
    Don't include the .py extension!
    '''
    id = str(ctx.author.id)
    if id == bot_developer_id:
        bot.unload_extension(f'cogs.{extension}')
        await typing_sleep(ctx)
        await ctx.send(f"{ctx.author.name} descargaste el cog {extension} con exito")
        print(f'cmdUnload||   El cog {extension}.py fue descargado con exito')
    else:
        await typing_sleep(ctx)
        await ctx.send("Solo el desarrollador puede cargar/habilitar los cogs del bot")


# ---> ping con latencia  4<----
@slash.slash(description='Muestra el ping del bot')
async def ping(ctx, arg=None):
    '''Muestra tu ping con respecto al bot'''
    if arg == "pong":
        await typing_sleep(ctx)
        await ctx.send(content="ah chistoso")
    else:
        await typing_sleep(ctx)
        await ctx.send(content=f"Mi ping es: {round(bot.latency * 1000)}ms")

# ----> Cogs loader <----
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.getenv('TOKEN'))