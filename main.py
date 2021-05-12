# REMEMBER TO USE Python 3.8.0 WHILE EDITING IN VSC
import asyncio
import datetime
import json
import math
import os
import random
import re
import sys  # to get python version
import time
import urllib
from datetime import date, datetime, time, timedelta
from io import BytesIO
from math import sqrt
from time import gmtime, strftime
#import urllib3
from urllib import parse, request

# ----------------------------------------->  # Required Libraries 
import aiofiles
import aiohttp
import certifi
# ----------------------------------------->  # discord.py fundamentals 
import discord
import numpy as np
import png
import pyqrcode
import requests
import sympy
import wikipedia
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from discord.ext.commands import Bot, errors
from discord.utils import get
from dotenv import load_dotenv  # to get the .env TOKEN
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
from pyqrcode import QRCode
from pytube import extract  # for the descarga cmd
from sympy import (Derivative, Integral, Limit, S, Symbol, diff, integrate,
                   limit, simplify)

import broBdays
import game
#<-------------------------------------------> File imports
import listas
import tuning
from functions import (degrees_to_cardinal, get_apex_data, get_dolar, printt,
                       typing_sleep)
from listas import brosId

load_dotenv()

# ----------------------------------------> Beginning of code

now = datetime.now()

current_hora = now.strftime("%H:%M:%S")
current_hour = now.strftime("%d/%m/%Y, %H:%M:%S")  # mm/dd/YY H:M:S format
   

intents = discord.Intents.all() 
bot = commands.Bot(command_prefix="#", intents=intents)


# --------> Bot en marcha <-------
@bot.event 
async def on_ready():
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

    #bot.warnings
    for guild in bot.guilds:
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
        name="--> #comandos",
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
    printt(' |        last updated: dd/mm/2021        |', 0.001)
    printt(f' |      Python: 3.8.0, Oct 14 2019        |', 0.001)
    printt(f' |          Discord.py:  {discord.__version__}            |', 0.001)
    printt('---------------------------------------------------->>>', 0.001)

    # connected message to "bigobot-testing" of Los Bigotazos
    channel = bot.get_channel(799387331403579462)
    await channel.send(f' :white_check_mark:  Connected at {current_hora}!')
    channel2 = bot.get_channel(791042478982824000)
    await channel2.send(f' :white_check_mark:  Connected at {current_hora}!')

##------> Statuses del Bot <--------
async def change_presence():
    await bot.wait_until_ready()
    # wait 35 secs. to start the change_presence loop...
    await asyncio.sleep(35)
    while not bot.is_closed():
        status = random.choice(listas.bot_statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)
    
bot.loop.create_task(change_presence())

##### ----------------->>>>  Comienzo de eventos  <<<<---------------- #####
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

@bot.event
async def on_member_join(member):
    for guild_id in bot.welcome_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.welcome_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{message} {member.mention}")
            return
            #alphascript cmd

@bot.event
async def on_member_remove(member):
    for guild_id in bot.goodbye_channels:
        if guild_id == member.guild.id:
            channel_id, message = bot.goodbye_channels[guild_id]
            await bot.get_guild(guild_id).get_channel(channel_id).send(f"{message} {member.mention}")
            return
            #alphascript cmd

@bot.event
async def on_message_delete(message):
    bot.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)
    #alphascript cmd
##### --------------->>>>  Finalizacion de eventos  <<<<-------------- #####

############################################################################

#### -------------->>>>  Acá comienzan los comandos  <<<<-------------- ####
@bot.command()
async def pedir_ticket(ctx, msg: discord.Message=None, category: discord.CategoryChannel=None):
    '''Ideal para admins y moderadores, la sintaxis puede verse al escribir el comando sin argumentos (#pedir_ticket a secas)'''
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

@bot.command()
@commands.has_permissions(kick_members=True)
async def rol_reaccion(ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
    '''
    Creas un mensaje reaccionable para un determinado rol, quien reaccione a dicho mensaje obtendra tal rol 
    ejemplo de uso: #rol_reaccion P A C H U S 836026898584829963 :thumbsup: 
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
@commands.has_permissions(kick_members=True)
async def set_canal_bienvenida(ctx, new_channel: discord.TextChannel=None, *, message=None):
    '''ES: Asigna un canal de bienvenida junto a un mensaje, a modo de ejemplo: #set_canal_bienvenida <ID_del_canal_de_texto> <mensaje>
    Ejemplo practico: #set_canal_bienvenida 123423798689324 Bienvenido al server de _____
    Si no sabes como obtener el id de un canal debes tener activado el modo desarrollador. Para eso
    debes ir a Ajustes de Usuario > Avanzado > desarrollador. Esto habilitara la opcion de copiar el
    ID de un canal de texto cuando des click derecho en el mismo...
    EN: Assigns a welcome channel along a message, e.g: #set_canal_bienvenida <ID_del_canal_de_texto> <mensaje>
    Practical example: #set_canal_bienvenida 123423798689324 Welcome to _____'s guild
    If you are not able to copy the ID of a text channel you should activate developer mode. For that
    you gotta go to User settings > Advanced > Developer. Now you'll be able to copy a text channel's ID
    when right clicking...
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
@commands.has_permissions(kick_members=True)
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
    '''Advierte a un usuario junto a una razon, ideal para moderadores. Comando experimental y no funcional al 100%'''
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

    async with aiofiles.open(f"databases/{member.name}_adverts.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

    await ctx.send(f"{member.mention} tiene {count} {'warning' if first_warning else 'warnings'}.")

@bot.command()
#@commands.has_permissions(kick_members=True)    #for if you wanna limit this command usage and prevent spamming
async def contar(ctx, number: int):
    '''Contar hasta un numero dado, puede ser re carnasa...'''
    i = 1
    while i <= number:
        async with ctx.typing():    
            await asyncio.sleep(0.5)
            await ctx.send(f"{i}")
            i += 1

#-----> comando sobre info del autor <-----
@bot.command(aliases=["autor", "dev", "desarrollador", "creador"])
async def monsa(ctx):
    '''Info sobre mi autor'''
    embedMine = discord.Embed(
        title="Acerca de mi",
        timestamp = datetime.utcnow(),
        color=discord.Color.blurple())
    
    #embedMine.set_author(name="Juli Monsa", icon_url="https://cdn.discordapp.com/attachments/793309880861458473/797528089726418974/yo_quien_mas.png")
    embedMine.set_author(name="Juli Monsa", url="https://www.steamcommunity.com/id/JuliMonsa", icon_url="https://cdn.discordapp.com/attachments/793309880861458473/797528089726418974/yo_quien_mas.png")
    embedMine.add_field(name="Canal YT:", value=f" https://www.youtube.com/channel/UCeQLgYEcEj9PteUzWWa2bRA", inline= False)
    embedMine.add_field(name="Perfil de Steam:", value=f" https://www.steamcommunity.com/id/JuliMonsa", inline= False)
    embedMine.add_field(name="Github:", value=f" https://github.com/julimonsa0x", inline= False)
    embedMine.add_field(name="Replit:", value=f" https://repl.it/@julimonsa0x", inline= False)
    embedMine.add_field(name="Telegram:", value=f" @julimonsa0x", inline= False)
    embedMine.add_field(name="Discord:", value=f" JuliTJZ#8141", inline= False)
    #embedMine.add_field(name="Página de", value=f"", inline= False)
    #embedMine.add_field(name="Página de", value=f"", inline= False)
    embedMine.set_thumbnail(url="https://i.imgur.com/mmF8hSX.png")  # ETHER ADDRESS 
    embedMine.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}")
    
    await typing_sleep(ctx)
    await ctx.send(embed=embedMine)
    print(f'cmdInfoSobreMí||         Info del autor enviada a {ctx.author.name} a las {current_hour}')

#---------> comando de joda tucson <--------
@bot.command()
async def tucson(ctx):
    '''tucson que mas'''
    msg = await ctx.send('tucson' + '<:doble:774509983832080385>')
    await msg.add_reaction('<:doble:774509983832080385>')
    print(f"{ctx.author.name} tiró la batiseñal tucson el {current_hour}") 

#-----------> Comando de trivia <-------------
@bot.command()
async def trivia(ctx):
    '''It's trivia time!!!'''
    await typing_sleep(ctx)
    msg = await ctx.channel.send("{}".format(random.choice(listas.trivias)))
    await msg.add_reaction(u"\u2705")
    await msg.add_reaction(u"\U0001F6AB")

    try:
        reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in [u"\u2705", u"\U0001F6AB"], timeout=8.0)  
        await asyncio.sleep(1)
        await ctx.channel.send("3...")
        await asyncio.sleep(1)
        await ctx.channel.send("2...")
        await asyncio.sleep(1)
        await ctx.channel.send("1...")

    except asyncio.TimeoutError:
        await typing_sleep(ctx)
        await ctx.channel.send("Che me ignoraron la trivia (▀̿Ĺ̯▀̿ ̿) ")

    else:
        if reaction.emoji ==  u"\u2705":
            await typing_sleep(ctx)
            await ctx.channel.send("Estoy seguro que sí... :alien:")

        else:
            await typing_sleep(ctx)
            await ctx.channel.send("mmm puede ser pa?¿ ")

#-------------> dolar info 11<----------------
@bot.command()
async def dolar(ctx):
    '''Cotizacion del dolar'''
    compraOfi = get_dolar('compraOfi')
    ventaOfi = get_dolar('ventaOfi')
    varOfi = get_dolar('varOfi')
    compraOfiSolid = get_dolar('compraOfiSolid')
    ventaOfiSolid = get_dolar('ventaOfiSolid')
    compraBlue = get_dolar('compraBlue')
    ventaBlue = get_dolar('ventaBlue')
    varBlue = get_dolar('varBlue')
    compraCcl = get_dolar('compraCcl')
    ventaCcl = get_dolar('ventaCcl')
    varCcl = get_dolar('varCcl')
    compraBolsa = get_dolar('compraBolsa')
    ventaBolsa = get_dolar('ventaBolsa')
    varBolsa = get_dolar('varBolsa')


    embedDolar = discord.Embed(
        Title = "Cotización del dolar",
        color = discord.Colour.green())
    embedDolar.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/801587601474715648/dollar.png")  
    embedDolar.add_field(name=':blue_circle:  Blue:', value=f"Compra: {compraBlue} | Venta: {ventaBlue} | Var. 24h: {varBlue}", inline=False)
    embedDolar.add_field(name=':green_circle:  Oficial:', value=f"Compra: {compraOfi} | Venta: {ventaOfi} | Var. 24h: {varOfi}", inline=False)
    embedDolar.add_field(name=':green_circle:  Oficial con impuestos:', value=f"Compra: {compraOfiSolid} | Venta: {ventaOfiSolid} | \n**¡Valores aproximados!**", inline=False)
    embedDolar.add_field(name=':yellow_circle:  Bolsa:', value=f"Compra: {compraBolsa} | Venta: {ventaBolsa} | Var. 24h: {varBolsa}", inline=False)
    embedDolar.add_field(name=':orange_circle:  Contado con liqui:', value=f"Compra: {compraCcl} | Venta: {ventaCcl} | Var. 24h: {varCcl}", inline=False)
    
    await typing_sleep(ctx)
    await ctx.send(embed=embedDolar)
    print(f"cmdDolar||            {ctx.author.name} solicitó la cot. del dolar el {current_hour}")

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
    '''Crea un emoji a partir de una URL, aconsejable un formato menor de 512x512.
    Si desconoces el tamaño de la imagen porbablemente no se cree el emoji...
    '''
    if url_emoji == None:
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
                await ctx.send("No pueden crearse emojis animados!")

            elif is_animated == False:
                b = BytesIO()
                img.save(b, format='PNG')
                b_value = b.getvalue()
                emoji = await guild.create_custom_emoji(image=b_value, name=name)
                await ctx.send(f'Emoji creado satisfactoriamente, aquí está: <:{name}:{emoji.id}> y su id es:\n```< :{name}:{emoji.id} >```')
                print(f"cmdCrearEmoji||     {ctx.author.name} creo el emoji custom '{name}' ")
                

@crearemoji.error
async def crearemoji_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Faltan argumentos, debes seguir la sintaxis #crearemoji <url_de_la_imagen_a_convertir> <nombre_del_emoji>. Recuerda tener espacio suficiente en el servidor para emojis y que no sea .gif")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y para ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        print(f"cmdCrearEmoji||      {ctx.author.name} fallo al crear un emoji ")

# ----------> Roles Colors <---------
# Be Careful if you have n roles, it'll print n messages
# suggest to use #borrar cmd
@bot.command()
async def roles_n_colors(ctx):
    '''Prints all roles with his respective HEX color, useful for dev's...'''
    roles_quantity = 0
    for role in ctx.guild.roles:
        await ctx.send(f" The role '{role.name}' has a HEX color: {role.color}")
        roles_quantity += 1
    
    await ctx.send(f" {ctx.author.mention} i highly suggest using command *#borrar {roles_quantity}* to clean this mess...")
    print(f"cmdRolesColors||     {ctx.author.name} requested the roles colors")

#--------> Tira un dado 9<--------
@bot.command()
async def dados(ctx, user=None, number1=1, number2=6):
    '''
    Tira un dado, recomendado para decidir turnos...
    argumento user opcional.
    argumento number1 y number2 por defecto 1 y 6 pero son modificables'''
    if user is None:
        user = ctx.author
    number = random.randint(number1, number2)
    dadosEmbed = discord.Embed(
        title="#Dados",
        description=f"Toco el numero {number} para {user.mention}"
        )
    dadosEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/842125661585276978/1f3b2.png") # dado.png

    await typing_sleep(ctx)
    await ctx.send(embed=dadosEmbed)
    print(f"cmdDados||   A {ctx.author.name} le tocó el dado {number}")


#--------> Steamcito Addon link <--------
@bot.command()
async def steamcito(ctx):   
    '''Extension util para steam'''
    await typing_sleep(ctx)    
    await ctx.send("https://emilianog94.github.io/Steamcito-Precios-Steam-Argentina-Impuestos-Incluidos/landing/#howto")
    print(f'cmdSteamcito||            {ctx.author.name} solicitó la web del addon Steamcito')

#-------> repite conmigo CMD 8<--------
@bot.command()
async def repite(ctx, *, arg=None):
    '''Repito lo que escribas y se borra en 15seg'''
    if arg == None:
        await typing_sleep(ctx)
        await ctx.send("Seguido del comando, escribe lo que quieres que repita", tts=True, delete_after=15)
        print(f'cmdRepite||       {ctx.author.name} intentó repetir sin argumentos')
    else:
        await typing_sleep(ctx)
        await ctx.send(f"{str(arg)}", tts=True)
        await ctx.message.delete()
        print(f'cmdRepite||         {ctx.author.name} repitió "{arg}" el {current_hour}')

########
############## COMANDOS DE VIDEOS RANDOMS 
#---> Lamar roasts Franklin vid <---
@bot.command()
async def roast(ctx):
    '''Lamar roasts Franklin trending videos...'''
    await typing_sleep(ctx)
    await ctx.send(random.choice(listas.roasts))
    print(f'cmdRoast||      Lamar v Franklin enviado a {ctx.author.name} a las {current_hour}')


#---> LocuraBailandoSinPantalones vid <---
@bot.command()
async def locurabailando(ctx):
    '''Locura bailando...'''
    await ctx.send("http://youtu.be/tvvGVZpnOMA")
    print(f'cmdLocura...||  Video del locurabailando a {ctx.author.name}')

#---> gordoPistero vid <---
@bot.command()
async def pistero(ctx):
    '''Gordo pistero'''
    await ctx.send("https://video.twimg.com/ext_tw_video/1327280070113644545/pu/vid/332x640/MuugcrrqHBQwQgSo.mp4?tag=1")
    print(f'cmdLocura...|| Video del gordopistero enviado a {ctx.author.name} a las {current_hour}')

#---> TADEO 1hs EN WHEELIE vid <---
@bot.command()
async def tadeo(ctx):
    '''Tadeo moto moto'''
    await ctx.send("https://youtu.be/ffoXJhzwcHQ")
    print(f'cmdTadeo||   Video del tade enviado a {ctx.author.name} XD')

#---> BESTO SPIDERMAN INTRO vid <---
@bot.command()
async def spider(ctx):
    await ctx.send("https://video.twimg.com/ext_tw_video/1343355396174585858/pu/vid/720x720/jUIsR2Z0PN8C-N10.mp4?tag=10")
    print(f'cmdTadeo||   intro de spiderman enviada a {ctx.author.name} XD')

#---> golazo vid <---
@bot.command()
async def golaso(ctx, *, args=None):
    '''golaso...'''
    await ctx.send("https://cdn.discordapp.com/attachments/793309880861458473/796239825090117652/glock_gol.mp4")
    print(f'cmdGolaso||   video del penal festejado con glock-18 para {ctx.author.name} XD')

#---> MATEUS505 GALO SNIPER vid <---
@bot.command()
async def galosniper(ctx):
    '''galo sniper...'''
    embedGalo = discord.Embed(
        title="galo sniper",
        description="galo sniper",
        color=discord.Color.red()
    )
    embedGalo.add_field(name="10 FATOS SOBRE MATEUS505 CARVALHO DO SANTOS", value=None, inline=False)
    embedGalo.add_field(name="FATO 1: ¿NOME DO MATEUS 505?", value="MATEO 505 CARVALHO DO SANTOS")
    embedGalo.add_field(name="FATO 2: ¿QUANTOS ANOS VOCE TEM?", value="20 ANOS", inline=False)
    embedGalo.add_field(name="FATO 3: ¿QUAL SEU MEME FAVORITO?", value="GALO SNIPER")
    embedGalo.add_field(name="FATO 4: ¿QUAL SEU PERSONAGEM FAVORITO?", value="GALO SNIPER", inline=False)
    embedGalo.add_field(name="FATO 5: ¿QUAL SEU FILME FAVORITO", value="GALO SNIPER AMERICANO")
    embedGalo.add_field(name="FATO 6: ¿QUAL SEU ANIME FAVORITO", value="GALO SNIPER SHIPPUDEN", inline=False)
    embedGalo.add_field(name="FATO 7: ¿QUAL SUA COR FAVORITA", value="BRANCO do GALO SNIPER")
    embedGalo.add_field(name="FATO 8: ¿QUAL o SEU INSTAGRAM", value="GALO SNIPER", inline=False)
    embedGalo.add_field(name="FATO 9: ¿QUAL SEU MELHOR AMIGO DA INFANCIA?", value="GALO SNIPER")
    embedGalo.add_field(name="FATO 10: ¿QUAL SEU ANIMAL FAVORITO?", value="Spoky ???? SNIPER", inline=False)
    await ctx.send(embed=embedGalo)
    await ctx.send("https://www.youtube.com/watch?v=cwiVlpW7-XM")
    print(f'cmdGaloSniper|| Video del GALOSNIPER enviado a {ctx.author.name} XD')
############## FIN DE VIDEOS DE COMANDOS RANDOMS
#########

#--------> info del sv 1<-------
@bot.command()
async def info(ctx):
    '''Info sobre el servidor'''
    embed2 = discord.Embed(
        title=f"{ctx.guild.name}",
        description="Un poco de info del sv",
        timestamp=datetime.utcnow(),
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
    #embed2.set_thumbnail(url="https://photos.app.goo.gl/2KgkWLgrErRmC6mx5")

    await typing_sleep(ctx)
    await ctx.send(embed=embed2)
    print(f'cmdInfo|| Info sobre {ctx.guild.name} enviada a {ctx.author.name} a las {current_hour}')


#-------->COMANDOS DE AYUDA inicio<----------
#----> menu de comandos <---- 
@bot.command()
async def comandos(ctx):
    '''Lista de los comandos'''
    author = ctx.message.author
    embedCmd = discord.Embed(
        color=discord.Colour.orange(),
        title=f"Menu de comandos a tu orden {ctx.author.name} :thumbsup:",
        description='si prefieres una ayuda mas personal, poné "#ayuda"',
        timestamp=datetime.utcnow()
    )
    #embedCmd.set_author(name="Author", icon_url="https://i.imgur.com/T5sqleE.png")
    embedCmd.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/794724078224670750/25884936-fd9d-4627-ac55-d904eb5269cd.png") #icono del bigobot
    embedCmd.add_field(name="-->Comando #info", value="Da informacion general sobre el server", inline=False)
    embedCmd.add_field(name="-->Comando #matecomandos", value="operaciones que puede resolver el bot a detalle", inline=False)
    embedCmd.add_field(name="-->Comando #reacciona, #...", value="Este y muchos otros comandos en ----> #moar", inline=False)
    embedCmd.add_field(name="-->Comando  *#youtube*", value="Busca un video que coincida", inline=False)
    embedCmd.add_field(name="-->Comando  #ping", value="Muestra tu latencia con respecto al bot", inline=False)
    embedCmd.add_field(name="-->Comando  #meme", value="Muestra memes randoms", inline=False)
    embedCmd.add_field(name="-->Comando  #quien", value="Muestra información sobre un miembro del server", inline=False)
    embedCmd.add_field(name="-->Comando  #temporal", value="Escribe un mensaje y se borra a los 3 segundos.", inline=False)
    embedCmd.add_field(name="-->Comando  #repite", value="El bot repite tus palabras como un pelotudo + tts=True", inline=False)
    embedCmd.add_field(name="-->Comando  #dados", value="Tira un dado con resultado del 1 al 6", inline=False)
    embedCmd.add_field(name="-->Comando  #md <id> <mensaje>", value="Envía un mensaje a un usuario con el bot con *#md <id del usuario> <tu mensaje>*, si no conoces su id usá *#quien <usuario>* ", inline=False)
    embedCmd.add_field(name="-->Comando  #dolar", value="te muestra la cotización del dolar blue un capo el bot", inline=False)
    embedCmd.add_field(name="-->Comando  #randomchamp", value="Te muestra un campeón random de LOL", inline=False)
    embedCmd.add_field(name="-->Comando  #randombrawl", value="Te muestra un brawler random de BS", inline=False)
    embedCmd.add_field(name="-->Comando  #help", value="Lista de todos los comandos", inline=False)
    embedCmd.add_field(name="-->Sugerencia", value="Comandos detallados por seccion con #ayuda", inline=False)
    embedCmd.set_footer(text = "Listo para ayudarte ;)/🥂")

    await typing_sleep(ctx)
    await ctx.send(embed=embedCmd)
    print(f"cmdComandos||   Comandos de ayuda enviados correctamente a {ctx.author.name} a las {current_hour}")

#menu #moar para las "interacciones" del bot
@bot.command()
async def moar(ctx): 
    '''Comandos no mencionados en #comandos'''
    author = ctx.message.author
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

#menu #matecomandos para las operaciones que puede hacer el bot
@bot.command()
async def matecomandos(ctx):
    '''Comandos sobre matematicas'''
    author = ctx.message.author
    embedMates = discord.Embed(
        color=discord.Colour.dark_blue(),
        title="Estas son las matemáticas que conoce el bot",
        timestamp=datetime.utcnow()
    )
    embedMates.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/794724078224670750/25884936-fd9d-4627-ac55-d904eb5269cd.png") #icono del bigobot
    embedMates.add_field(name="Suma   #suma", value="Para sumar dos números escribe: *#sum A B*", inline=True)
    embedMates.add_field(name="Resta   #resta", value="no flaco/a no hay comando de resta volve a la primaria de última", inline=True)
    embedMates.add_field(name="Multiplicación  #mult", value="Para multiplicar dos números escribe: *#mult A B*", inline=True)
    embedMates.add_field(name="División  #division", value="Para dividir dos números escribe: *#division A B*", inline=True)
    embedMates.add_field(name="Potenciacion y Radicación  #pot", value="Para Potencias y Raíces, escribe: *#pot A B* a modo de ejemplo #pot **2** **3** = *8*, #pot **10** **-3** = *0.001*", inline=True)
    embedMates.add_field(name="Ecuaciones de 2° grado - Baskara  #bask", value="Escribe los tres coeficientes con respectivos signos así: *#bask A B C*, te devolverá raíz positiva y raíz negativa de la ecuación", inline=True)
    embedMates.add_field(name="Raíz cuadrada  #raiz", value="Para hallar la raíz de número escribe: *#raiz A*", inline=True) 
    embedMates.add_field(name="Calcular Límites", value="Para calcular límites con #limite sigue esta sintaxis: (función, variable, punto). Entonces para calcular el límite de f(x) cuando x tiende a 0, debemos escribir: (f(x), x, 0), Puede optar por #help limite", inline=True) 
    embedMates.add_field(name="Calcular Derivadas", value="Para calcular derivadas sigue esta sintaxis: (función, variable, punto). Entonces para calcular el límite de f(x) cuando x tiende a 0, debemos escribir: (f(x), x, 0), Puede optar por #help derivada", inline=True)
    embedMates.add_field(name="Calcular Integrales", value="Para calcular integrales sigue esta sintaxis: (función, variable, punto). Entonces para calcular el límite de f(x) cuando x tiende a 0, debemos escribir: (f(x), x, 0), Puede optar por #help integral", inline=True)
    
    async with ctx.typing():    
        await asyncio.sleep(type_time)
        await ctx.send(embed=embedMates)
        print(f"{ctx.author.name} solicitó los comandos matemáticos")

    
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
    embed_help.add_field(name="--> Comandos interactivos ", value="Por ejemplo #reacciona, #dados, #trivia, #randomchamp, #randombrawl, #moar, #meme, y mucho mas...", inline=False)
    embed_help.add_field(name="--> Comandos sobre videos ", value="#pistero, #tadeo, #golaso, #spider, #locurabailando, #galosniper, #roast, #willy")
    embed_help.add_field(name="--> Comandos útiles ", value="#dolar, #qr, #steamcito, #info, #clima, #youtube, #dm, #md, #chusmear, #descarga, #repite, #tunear, #wiki, #crearemoji", inline=False)
    embed_help.add_field(name="--> Comandos para admins ", value="#advertir, #advertencias, #kick, #ban, #set_canal_bienvenida, #set_canal_despedida, #pedir_ticket, #rol_reaccion, #setdelay", inline=False)
    embed_help.add_field(name="--> Comandos matemáticos", value="#matecomandos", inline=False)
    embed_help.add_field(name="--> Comandos de conversion", value="#bin_a_dec, #dec_a_bin, #hex_a_dec, #dec_a_hex, #num_a_rom", inline=False)
    embed_help.set_footer(text = "Listo para ayudarte ;)/🥂", icon_url=ctx.author.avatar_url)
    
    async with ctx.typing():    
        await asyncio.sleep(type_time)
        await author.send(embed=embed_help)
        print(f"cmdAyuda||   Ayuda de comandos solicitda por {ctx.author.name} a las {current_hour}")
#-------->COMANDOS DE AYUDA fin<----------


#----> Borra mensajes a los 3 segundos 7<----
@bot.command()
async def temporal(ctx, *, arg):
    '''Repite tu mensaje por 3 segundos y no queda rastro (aunque puede chusmearse con #chusmear)'''
    #channel = 559592087054450690     #get the channel, could be useful for a channel whitelist 
    await ctx.message.delete()
    ## send the message
    await typing_sleep(ctx)
    message = await ctx.send(arg, tts=True)
    ## wait for 3 seconds
    await asyncio.sleep(3)  
    ## delete the message
    await message.delete()
    print(f"cmdTemporal||      {ctx.author.name} borró el mensaje '{arg}' a las {current_hour}...")

#-----> Chusmea los mensajes borrados <-----
@bot.command()
async def chusmear(ctx):
    '''Chusmea el ultimo mensaje borrado, de cualquier canal y de cualquier usuario'''
    try:
        contents, author, channel_name, time = bot.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("No encontré un mensaje para chusmear ◔̯◔")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Borrado de : #{channel_name}")

    await typing_sleep(ctx)
    await ctx.channel.send(embed=embed)

@bot.command()
async def avatar(ctx, member: discord.Member):
    '''Muestra el avatar de un @usuario que menciones'''
    embedAvatar = discord.Embed(
        description = f'[**URL de la imagen**]({member.avatar_url})',  
        color = discord.Colour.green(),
        timestamp=datetime.utcnow()
        )
    #embedAvatar.add_field('[URL del avatar]: (str(member.avatar_url))')
    embedAvatar.set_author(name=f"Avatar de: {member.name}#{member.discriminator}", icon_url=member.avatar_url)
    embedAvatar.set_image(url = member.avatar_url)
    embedAvatar.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}")
    await typing_sleep(ctx)
    await ctx.send(embed=embedAvatar)
    print(f"cmdAvatar||          Avatar de {member.name}#{member.discriminator} para {ctx.author.name} a las {current_hour}")


#-----> Comando: "¿quien es?" 6<----
@bot.command()
async def quien(ctx, member: discord.Member): 
    '''Info sobre @Mencion'''
    fecha_Cumple = functions.bro_birthdays_check(member.id)

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
    embedWho.set_thumbnail(url = member.avatar_url)
    embedWho.set_footer(icon_url = ctx.author.avatar_url, text = f"Solicitud de {ctx.author.name}#{member.discriminator}")
    
    await typing_sleep(ctx)
    await ctx.send(embed=embedWho)
    print(f"cmdQuien||       Info sobre {member.name}#{member.discriminator} para {ctx.author.name} a las {current_hour}")

@quien.error
async def quien_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Seguido del comando debes @Mencionar a alguien")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        print(f"cmdQuien||     {ctx.author.name} olvidó mencionar a alguien")
#------------------------------->>>

#----> memes y gifs 5<-----
@bot.command()
async def meme(ctx):
    '''Memes randoms, a quien no le gustan los memes...'''
    embed = discord.Embed(color = discord.Colour.red(), timestamp=datetime.utcnow())
    random_link = random.choice(listas.images)
    if (
            random_link.startswith('https://video.twimg.com/ext_tw_video/') or 
            random_link.startswith('https://imgur') or 
            random_link.startswith('https://www.youtube:') or
            random_link.startswith('https://i.imgur') or 
            random_link.startswith('https://youtu')
        ):
        await typing_sleep(ctx)
        await ctx.send(random_link)
        print(f'cmdMeme||         Meme enviado a {ctx.author.name} a las {current_hour}')
        
    else:
        embed.set_image(url = random_link)
        await typing_sleep(ctx)
        await ctx.send(embed = embed)
        print(f'cmdMeme||         Meme enviado a {ctx.author.name} a las {current_hour}')

#----> Reddit meme <----
@bot.command()
async def reddit_meme(ctx, subreddit_to_search=None):
    """EN: Searchs for a random meme in a given subreddit. 
    subreddit r/memes by default if no subreddit is given...
    syntax example: #reddit_meme dankmemes\n
    ES: Busca un meme random en un subreddit dado.
    por defecto envia memes del subreddit r/memes...
    ejemplo: #reddit_meme MemesArgentina"""
    if subreddit_to_search != None:
        subreddit_url = f"https://www.reddit.com/r/{subreddit_to_search}.json"
    elif subreddit_to_search == None:
        subreddit_url = "https://www.reddit.com/r/memes.json"
        subreddit_to_search = "memes"

    async with aiohttp.ClientSession() as cs:
        async with cs.get(subreddit_url) as resp:
            memes = await resp.json()
            pick_random = random.randint(0, 25)
            embedReddit = discord.Embed(
                title = (f"Meme/post de r/{subreddit_to_search}."),
                color = discord.Color.purple(),
                timestamp = datetime.utcnow()
            )
            embedReddit.add_field(name = "***Título***", value = f'{memes["data"]["children"][pick_random]["data"]["title"]}', inline = True)
            embedReddit.add_field(name = "***Autor***", value = f'{memes["data"]["children"][pick_random]["data"]["author"]}', inline = True)
            embedReddit.add_field(name = "***Likes***", value = f'{memes["data"]["children"][pick_random]["data"]["score"]}', inline = True)
            embedReddit.set_image(url=memes["data"]["children"][pick_random]["data"]["url"])
            embedReddit.set_footer(icon_url = ctx.author.avatar_url, text = f"Meme para {ctx.author.name}")
            await typing_sleep(ctx)
            await ctx.send(embed = embedReddit)
            print(f'cmdRedditMeme||         Meme enviado  {ctx.author.name} a las {current_hour}')

#---->Juegos gratis epic <----
@bot.command()
async def juegos_gratis(ctx, platform=None):
    """Comando que muestra los juegos gratis de la Epic Store por defecto. Uplay y mas plataformas por venir"""
    if platform != None:
        await ctx.send(f"{ctx.author.name} actualmente el comando esta en desarrollo y solo es soportada la plataforma de epic games...")

    elif platform == None:
        platform = 'epic'
        epic_json = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
        epic_free_games_web = 'https://www.epicgames.com/store/es-ES/free-games'

        req = requests.get(epic_json).json()
        title1 = req['data']['Catalog']['searchStore']['elements'][0]['title']  # str
        seller1 = req['data']['Catalog']['searchStore']['elements'][0]['seller']['name']  # str 
        price1 = req['data']['Catalog']['searchStore']['elements'][0]['price']['totalPrice']['fmtPrice']['originalPrice']  # str
        thumbnail1 = req['data']['Catalog']['searchStore']['elements'][0]['keyImages'][2]['url']  # str 
        try:
            effectiveDate1 = f"Desde: {str(req['data']['Catalog']['searchStore']['elements'][0]['effectiveDate'])[:10]}, hasta: {str(req['data']['Catalog']['searchStore']['elements'][0]['price']['lineOffers'][0]['appliedRules'][0]['endDate'])[:10]}"
        except IndexError:
            effectiveDate1 = f"Fecha de validez desconocida :("

        title2 =  req['data']['Catalog']['searchStore']['elements'][1]['title']
        title3 =  req['data']['Catalog']['searchStore']['elements'][2]['title']
        title4 =  req['data']['Catalog']['searchStore']['elements'][3]['title']
        embedGame1 = discord.Embed(
                title = f'**Juegos gratis actuales en {platform}**',
                description = f'[Reclamar juego]({epic_free_games_web})',
                color = discord.Color.purple(),
                timestamp = datetime.utcnow()
            )
        embedGame1.add_field(name = "***Título***", value = title1, inline = False)
        embedGame1.add_field(name = "***Desarrolladora***", value = seller1, inline = True)
        embedGame1.add_field(name = "***Precio original***", value = f"{price1}USD, consultar #dolar", inline = False)
        embedGame1.add_field(name = "***Vigencia***", value = effectiveDate1, inline = True)
        embedGame1.set_image(url=thumbnail1)
        embedGame1.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")

        embedGame2 = discord.Embed(title="Proximos juegos gratuitos",color=discord.Color.purple())
        embedGame2.add_field(name = f"Luego de {title1}:", value = f"{title2}")
        embedGame2.add_field(name = f"Luego de {title2}:", value = f"{title3}")
        embedGame2.add_field(name = f"Luego de {title3}:", value = f"{title4}")
        await typing_sleep(ctx)
        await ctx.send(embed = embedGame1)
        await ctx.send(embed = embedGame2)
        await ctx.send(f"Eso es todo por ahora {ctx.author.name}!")
        print(f'cmdJuegosGratis||         Juego gratis por {ctx.author.name} a las {current_hour}')


#--> videos out of context willy <--
@bot.command()
async def willy(ctx):
    '''videos del willy out of context, un cago de risa...'''
    await typing_sleep(ctx)
    await ctx.send(random.choice(listas.willyooc))
    print(f'cmdWilly||      Willy OOC enviado a {ctx.author.name} a las {current_hour}')

#----> campeones del LoL 10<-----
@bot.command()
async def randomchamp(ctx):
    '''Campeon random de lol, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
    await ctx.send("3...")
    await asyncio.sleep(0.5)
    await ctx.send("2...")
    await asyncio.sleep(0.5)
    await ctx.send("1...")
    await asyncio.sleep(0.5)

    embed3 = discord.Embed(color = discord.Colour.orange(), timestamp=datetime.utcnow())
    randomChamp = random.choice(listas.campeones)
    embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/797965087767396442/lol-icon.png")
    embed3.add_field(name= f"Campeón Aleatorio:", value=f"{randomChamp}")
    embed3.set_footer(icon_url = ctx.author.avatar_url, text = f"Le tocó a {ctx.author}") 
    
    await typing_sleep(ctx)
    await ctx.send(embed=embed3)
    print(f"cmdRandomChamp|| Campeón aleatorio enviado, a día de hoy en la lista hay: {str(len(listas.campeones))}")

#----> Brawlers randoms de BS<-----
@bot.command()
async def randombrawl(ctx):
    '''Brawler random, recomendado primero jugar al #ppt (piedra papel o tijeras) si se requiere turnarse'''
    await ctx.send("3...")
    await asyncio.sleep(0.5)
    await ctx.send("2...")
    await asyncio.sleep(0.5)
    await ctx.send("1...")
    await asyncio.sleep(0.5)
    
    embed = discord.Embed(color = discord.Colour.orange(), timestamp=datetime.utcnow())
    randomBrawl = random.choice(listas.brawlers)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/793309880861458473/797964925980246066/c849eb95e858ce12cdc86cb6d4ecb36b00bbdfaa96d9973852d1421661f5aec5200.png")
    embed.add_field(name= "Brawler Aleatorio: ", value=f"{randomBrawl}")
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Le tocó a {ctx.author}")
    
    await typing_sleep(ctx)
    await ctx.send(embed=embed)
    print(f"cmdRandomBrawl|| Brawler aleatorio enviado, hoy {current_hour} en la lista hay: {str(len(listas.brawlers))}")


#--------> buscar vids de yt 3<-------
@bot.command()
async def youtube(ctx, *, search):
    '''Busca un video de youtube y miralo, en discord android / ios se abre la app youtube'''
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall('/watch\?v=(.{11})', html_content.read().decode())
    #print(search_results)
    await typing_sleep(ctx)
    await ctx.send('https://youtube.com/watch?v=' + search_results[0])
    print(f'cmdYoutube|| {ctx.author.name} buscó el video {search} en yt')

@youtube.error
async def youtube_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Seguido del comando debes introducir el nomber del video a buscar")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")

#------> buscar en wikipedia <------
@bot.command()
async def wiki(ctx, lang:str='es', *, search):
    """
    Busca en wikipedia, lenguaje español por defecto. 
    para buscar en un lenguaje especifico introduce las iniciales del lenguaje
    ejemplo sintaxis: #wiki <lang> <tu busqueda>
    ejemplo 2: #wiki elon musk (al ignorar el 2do parametro "lang", busca por defecto en español)
    ejemplo 3: #wiki fr google (fr buscara en frances...)
    """
    wikipedia.set_lang(f"{lang}")
    result = wikipedia.summary(f"{search}")   
    if len(result) <= 2000:
        await typing_sleep(ctx)
        await ctx.send(f"```{result}```")
        print(f"cmdWikipedia||   {ctx.author.name} buscó en wikipedia: {search} el {current_hour}")
        print(f" longitud de result : {len(result)} ")

    else:
        wikipedia.set_lang(f"{lang}")
        result = wikipedia.summary(f"{search}")
        result = result[:1996] + "..."
        await typing_sleep(ctx)
        await ctx.send(f"```{result}```")
        print(f"cmdWikipedia||   {ctx.author.name} buscó en wikipedia: {search} el {current_hour}\nlongitud de result: {len(result)}\n lenguaje: {lang}\n---")

@wiki.error
async def wiki_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Para una búsqueda correcta debes seguir la sintaxis **#wiki <lenguaje> <tu_busqueda>**. Para buscar en inglés -> en | Para buscar en español -> es | (símbolo del lenguaje)")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        print(f"cmdWiki||     {ctx.author.name} falló al buscar en wikipedia por falta de argumentos")

#----> Descargar YT Videos <-----
@bot.command()
async def descarga(ctx, url=None):   
    '''Introduce una url de un video de YT y se te redirigirá
    a otra pagina para descargar tal video en .mp3 o .mp4...
    '''
    if url != None:
        id = extract.video_id(url)
        downl_url = f"https://www.y2mate.com/es/convert-youtube/{id}"
        await typing_sleep(ctx)
        await ctx.send(f"Aqui esta el video listo para ser descargado: {downl_url}")
        print(f"cmdDescarga||            {ctx.author.name} descargo un video...")                
    else:
        await typing_sleep(ctx)
        await ctx.send("No se pudo convertir con exito el video...")
        print(f"cmdDescarga||            {ctx.author.name} no pudo descargar un video...")     

###------------- Comandos de conversiones Inicio ---------->>>>

#----> Convertir de binario a decimal <----
#https://parzibyte.me/blog/2020/12/05/python-convertir-binario-decimal/
@bot.command()
async def bin_a_dec(ctx, binary: str):
    '''Convierte un binario dado, a decimal'''
    posicion = 0
    decimal = 0
    # Invertir la cadena porque debemos recorrerla de derecha a izquierda
    binario = binary[::-1]
    for digito in binario:
        # Elevar 2 a la posición actual
        multiplicador = 2**posicion
        decimal += int(digito) * multiplicador
        posicion += 1
    await typing_sleep(ctx)    
    await ctx.send(f"El binario: {binary} en decimal es: {decimal}")


# ---> Convertir de decimal a binario <---
# from geeksforgeeks
@bot.command()
async def dec_a_bin(ctx, decimal: int):
    '''Convierte un decimal dado, a binario'''
    bin_result = bin(decimal).replace("0b", "")
    bin_result2 = bin(decimal)[2:]
    print(bin_result2)
    await typing_sleep(ctx)
    await ctx.send(f"El decimal {decimal} en binario es: {bin_result}")


# ----> Convertir de HEX a decimal <----
# from geeks for geeks
@bot.command()
async def hex_a_dec(ctx, hex: str):
    '''Convierte un Hexadecimal dado, a decimal'''
    dec_result = int(hex, 16) 
    dec_result = str(dec_result)
    await typing_sleep(ctx)
    await ctx.send(f"El hexadecimal {hex} en decimal es: {dec_result}")


# ---> Convertir de decimal a HEX <---
@bot.command()
async def dec_a_hex(ctx, decimal: int):
    '''Convierte un decimal dado, a hexadecimal'''
    hex_result = hex(int(decimal))[2:].upper()
    await typing_sleep(ctx)
    await ctx.send(f"El decimal {decimal} en hexadecimal es: {hex_result}")


# ---> Convertir decimal a romano <----
# from a spanish youtube channel, ep 751 i remember...
@bot.command()
async def num_a_rom(ctx, numero: int):
    '''
    Convierte numeros enteros a numerales romanos
    el numero debe ser menor a 4000, caso contrario 
    mostrara resultados no validos...
    '''

    numero_inicial = numero

    numeros = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerales = ['M', 'CM', 'D', 
                'CD', 'C', 'XC', 
                'L', 'XL', 'X', 
                'IX', 'V', 'IV', 'I']

    numeral = ''
    i = 0

    if numero > 3999:
        await typing_sleep(ctx)
        await ctx.send("Actualmente no es posible convertir numeros mayores a 3999\npara esto se requieren caracteres especiales :(")
    
    elif numero <= 3999:
        while numero > 0:
            for _ in range(numero // numeros[i]):
                numeral += numerales[i]
                numero -= numeros[i]
            i += 1

    await typing_sleep(ctx)
    await ctx.send(f"El numero {numero_inicial} en romano es {numeral}")

###------------- Comandos de conversiones Final ------------>>>>
################################################################
###-------------- Operaciones Matemáticas inicio------------>>>>
#---------> suma <---------
@bot.command()
async def suma(ctx, num1: int, num2: int):
    '''Suma dos numeros que introduzcas, deben estar separados
    a modo de ejemplo: #suma 1 5 -----> 6
    '''
    sumResult = num1 + num2
    await typing_sleep(ctx)
    await ctx.send("Resultado de la suma: ```{}``` " .format(sumResult))
    print(f'cmdSuma||   {ctx.author.name} sumó {num1} con {num2} ---> {sumResult} a las {current_hour}')

#---------> Resta no hay jaja <---------
@bot.command()
async def resta(ctx, num1: int, num2: int):
    '''Resta dos numeros, deben estar separados
    a modo de ejemplo: #resta 20 15
    '''
    await typing_sleep(ctx)
    await ctx.send(random.choice(listas.intentoResta))
    print(f'cmdResta||  {ctx.author.name} intentó restar jaja')

#----> multiplicacion  <----
@bot.command()
async def mult(ctx, num1: int, num2: int):
    '''Multiplica dos numeros que introduzcas'''
    multResult = num1 * num2
    await typing_sleep(ctx)
    await ctx.send(" Resultado del producto: ```{}``` " .format(multResult))
    print(f'cmdMult||   {ctx.author.name} multiplicó {num1} y {num2} ---> {multResult} a las {current_hour}')

#----> division <----
@bot.command()
async def division(ctx, num1: int, num2: int):
    '''Divide dos numeros que introduzcas'''
    divQuotient = (num1 // num2)
    divRemain = (num1 % num2)
    await typing_sleep(ctx)
    await ctx.send(f"El cociente da {divQuotient} y el resto queda {divRemain}")
    print(f'cmdDivision|| {ctx.author.name} dividió {num1} sobre {num2} ---> {divQuotient} | {divRemain} a las {current_hour}')

#----> potenciación y radicación  <----
@bot.command()
async def pot(ctx, num1: int, num2: int):
    '''El 1er numero que introduzcas a la potencia del 2do
    ejemplo: #pot 3 3 ----> 3 al cubo ---> 27
    '''
    potResult = num1 ** num2
    await typing_sleep(ctx)
    await ctx.send("Resultado: ```{}``` " .format(potResult))
    print(f'cmdPot||    {ctx.author.name} potenció/radicó {num1} a la {num2} ---> {potResult} a las {current_hour}')

#----> BASKARA <----
@bot.command()
async def bask(ctx, numOne: float, numTwo: float, numThree: float):
    '''Introduce los coeficientes de la funcion con su respectivo signo!
    ejemplo de sintaxis con la siguiente ecuacion ---> 5X² - 20X +15
    #bask +5 -20 +15 ----> x1 = 3, x2 = 1 
    '''
    # Formula----------------->>> complexBaskEcuation = int((numTwo**2)-4*numOne*numThree) 
    # Formula----------------->>> realBaskEcuation = str(f"{numOne}x^2 {numTwo}x {numThree}"   
    if ((numTwo**2)-4*numOne*numThree) < 0:
        complexBaskEcuation = int((numTwo**2)-4*numOne*numThree)
        await typing_sleep(ctx)
        await ctx.send("La solución de la ecuación es con numeros complejos :(")
        print(f'La ecuación de {ctx.author.name} es compleja: "{complexBaskEcuation}"')
        
    else:
        realBaskEcuation = str(f"{numOne}x^2 {numTwo}x {numThree}")
        root1 = ((-numTwo)+(numTwo**2-(4*numOne*numThree))**0.5)/(2*numOne)   # Raíz positiva
        root2 = ((-numTwo)-(numTwo**2-(4*numOne*numThree))**0.5)/(2*numOne)   # Raíz negativa
        await typing_sleep(ctx)
        await ctx.send(" Parte positiva: ```{}``` " .format(root1))
        await ctx.send(" Parte negativa: ```{}``` " .format(root2))
        print(f'cmdBask||       {ctx.author.name} halló raices con éxito para la ecuación {realBaskEcuation} ----> {root1} y {root2} a las {current_hour}')

@bask.error
async def bask_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Debes seguir la sintáxis #bask <coeficiente cuadratico> <coeficiente lineal> <termino independiente> \ncon sus respectivos signos...")
        await ctx.send('https://cdn.discordapp.com/attachments/793309880861458473/804126063880830996/how_to_bask.png')
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
        print(f"cmdBask||     {ctx.author.name} quiso baskarear el {current_hour}")

#-------> Raíz cuadrada <-------
@bot.command()
async def raiz(ctx, num1: int): 
    '''La raiz cuadrada de un numero que introduzcas'''  
    sqrtResult = np.sqrt(num1)   
    await typing_sleep(ctx)
    await ctx.send("Resultado de la raíz: ```{}``` " .format(sqrtResult))
    print(f'cmdSqrt|| {ctx.author.name} halló la raíz cuadrada de {num1}, ---> {sqrtResult} a las {current_hour}')


##-------> Seno de un ángulo <-------
@bot.command()
async def seno(ctx, num1: int):
    '''El seno de un grado que introduzcas'''
    sinResult = math.sin(math.radians(num1)) 
    await typing_sleep(ctx)
    await ctx.send("Resultado: ```{}``` " .format(sinResult))
    print(f'cmdPot||    {ctx.author.name} halló el seno de {num1} ---> {sinResult} a las {current_hour}')

#-------> Coseno de un ángulo <-------
@bot.command()
async def coseno(ctx, num1: int):
    '''El coseno de un grado que introduzcas'''
    cosResult = math.cos(math.radians(num1)) 
    await typing_sleep(ctx)
    await ctx.send("Resultado: ```{}``` " .format(cosResult))
    print(f'cmdPot||    {ctx.author.name} halló el coseno de {num1} ---> {cosResult} a las {current_hour}')

 #----> Tangente de un ángulo <----

#------> Tangente de un ángulo <------
@bot.command()
async def tangente(ctx, num1: int):
    '''La tangente de un grado que introduzcas'''
    tanResult = math.tan(math.radians(num1)) 
    await typing_sleep(ctx)
    await ctx.send("Resultado: ```{}``` " .format(tanResult))
    print(f'cmdPot||    {ctx.author.name} halló la tangente de {num1} ---> {tanResult} a las {current_hour}')

#------> Hipotenusa de dos catetos <------
@bot.command()
async def hipotenusa(ctx, num1: int, num2: int):
    '''Calcula la hipotenusa de dos numeros que introduzcas'''
    hipResult = math.hypot(num1, num2) 
    await typing_sleep(ctx)
    await ctx.send("Resultado: ```{}``` " .format(hipResult))
    print(f'cmdPot||    {ctx.author.name} halló la tangente de {num1} ---> {hipResult} a las {current_hour}')


#-----> Límites <----
@bot.command()
async def limite(ctx, function=None, var=None, point=None):
    '''Halla el limite de una funcion cuando tiende a un punto dado
    escribe el comando a secas para ver un ejemplo mas a detalle!
    '''
    if function != None and var != None and point != None:
        function:str 
        var:str
        point:int
        limitResult = limit(function, var, point)
        await typing_sleep(ctx)
        await ctx.channel.send(f"El límite cuando {function} tiende a {point} es: {limitResult}")
        print(f"{ctx.author.name} halló el límite de {function} ---> {limitResult} a las {current_hour}")
    
    else:
        await typing_sleep(ctx)
        await ctx.channel.send(f"Debes seguir la sintaxis #limite[funcion], [variable], [punto] ")
        await ctx.channel.send(f"{ctx.author.name} mira este ejemplo con *x²-8x+5*")
        await ctx.channel.send(f"La entrada debe ser escrita así: ``` x**2-8*x+5 x 10 ```")
        await ctx.channel.send(f"Ignora el formateo de texto automatico de discord, en cuanto escribes esa funcion se te convertirá en ``` x*2-8x+5 x 10 ```")
        await ctx.channel.send(f"Esto no es posible de evitar debido a que está implementado de manera predeterminada en discord pero el bot aun asi te dará el resultado correcto :thumbsup:")
        await ctx.channel.send(f"Por ultimo recordar que esto no pasa solo en esta funcion, ocurre cuando un texto esta encerrado con asteriscos (se convierte en cursiva)")
        embed = discord.Embed()
        embed.set_image(url="https://cdn.discordapp.com/attachments/793309880861458473/797301871374237766/teoriadelimites.jpg")
        #embed.set_image(url="attachment://teoriadelimites.jpg")   #estas 2 lineas seran necesarias
        #image = discord.File("teoriadelimites.jpg")               #si se quiere usar archivo local
        await ctx.send(embed=embed)                               #embed no necesario por el momento
        await ctx.channel.send(f"Salida: ``` 25 ```")
        print(f"{ctx.author.name} falló al querer calcular un límite a las {current_hour}")
    

#----> Derivadas <----
@bot.command()
async def derivada(ctx, function=None):
    '''Halla la derivada de una funcion escribe el
    comando a secas para ver un ejemplo mas a detalle!
    '''
    if function != None:
        fx = str(function)
        x = Symbol('x')
        ddxResult = simplify(diff(fx, x))
        await typing_sleep(ctx)
        await ctx.channel.send(f"La derivada de {function} es: ```{ddxResult}```")
        print(f"{ctx.author.name} halló la derivada de {function} ---> {ddxResult} a las {current_hour}")
    
    else:
        await typing_sleep(ctx)
        await ctx.channel.send(f"Debes seguir la sintaxis #derivada[funcion]")
        await ctx.channel.send(f"{ctx.author.name} mira este ejemplo con *x²-10x")
        await ctx.channel.send(f"Entrada x²-10x: Debe ser ingresada así ``` x**2-10*x ```")
        await ctx.channel.send(f"Ignora el formateo de texto automatico de discord, en cuanto escribes esa funcion se te convertirá en ``` x*2-10x ```, tu solo dale enter por mas que se haya cambiado")
        await ctx.channel.send(f"Esto no es posible de evitar debido a que está implementado de manera predeterminada en discord pero el bot aun asi te dará el resultado correcto :thumbsup:")
        await ctx.channel.send(f"Por ultimo recordar que esto no pasa solo en esta funcion, ocurre en cualquier texto encerrado con asteriscos (se convierte en cursiva)")
        await ctx.channel.send(f"Salida: ``` 2*x-10 ```")
        print(f"{ctx.author.name} falló al querer calcular una derivada a las {current_hour}")

#----> Integrales <----
@bot.command()
async def integral(ctx, function=None, dif1=None, dif2=None):
    '''Halla la integral de una funcion, sintaxis #integral <funcion>. Recuerda que para multiplicar debe usarse * y para elevar (potencias) debe usarse **'''
    if function != None and dif1 == None and dif2 == None:
        fx = str(function)
        x = Symbol('x')
        intResult = Integral(fx, x).doit()
        await typing_sleep(ctx)
        await ctx.channel.send(f"La integral indefinida de {function} es:")
        await ctx.channel.send(f"``` {intResult} ```")
        print(f"{ctx.author.name} halló la integral indef. de {function} ---> {intResult} a las {current_hour}")
    
    elif function != None and dif1 != None and dif2 != None:
        fx = str(function)
        x = Symbol('x')
        a = int(dif1)
        b = int(dif2)
        intResult = Integral(fx, (x, a, b)).doit()
        await typing_sleep(ctx)
        await ctx.channel.send(f"La integral definida de {function} es:")
        await ctx.channel.send(f"``` {intResult} ```")
        print(f"{ctx.author.name} halló la integral def. de {function} ---> {intResult} a las {current_hour}")

    else:
        async with ctx.typing():    
            await asyncio.sleep(type_time)
            await ctx.channel.send(f"Debes seguir la sintaxis #integral[funcion]")
            await ctx.channel.send(f"{ctx.author.name} mira este ejemplo con x³-6x indefinido")
            await ctx.channel.send(f"Entrada x³-6x: Debe ser ingresada así ``` x**3-6*x ```")
            await ctx.channel.send(f"Ignora el formateo de texto automatico de discord, en cuanto escribes esa funcion se te convertirá en x*3-6x, tu solo dale enter por mas que se haya cambiado")
            await ctx.channel.send(f"Esto no es posible de evitar debido a que está implementado de manera predeterminada en discord pero el bot aun asi te dará el resultado correcto :thumbsup:")
            await ctx.channel.send(f"Por ultimo recordar que esto no pasa solo en esta funcion, ocurre en cualquier texto encerrado con asteriscos (se convierte en cursiva)")
            await ctx.channel.send(f"Salida (x⁴/4)-(3x²): ``` (x**4)/4-(3*x**2) ```")
            embedIndef = discord.Embed()
            embedIndef.set_image(url="https://cdn.discordapp.com/attachments/793309880861458473/798420481828585504/how_to_int_indef.png")
            await ctx.send(embed=embedIndef)        
            await ctx.channel.send(f"-------------->")
            
            await ctx.channel.send(f"Ahora va un ejemplo con x³-6x definido de 0 a 3")
            await ctx.channel.send(f"Entrada x³-6x: Debe ser ingresada así ``` x**3-6*x 0 3```")
            await ctx.channel.send(f"Salida: ``` -27/4 ```")
            embedDef = discord.Embed()
            embedDef.set_image(url="https://cdn.discordapp.com/attachments/793309880861458473/798420477713973269/how_to_int_def.png")
            await ctx.send(embed=embedDef)                               
            print(f"{ctx.author.name} falló al querer calcular una derivada a las {current_hour}")

#----> Fibonacci <-----
@bot.command()
async def fib(ctx, number: int):
    '''Encuentra el enésimo numero de fibonacci'''
    if number == None:
        await typing_sleep(ctx)
        await ctx.send("Debes ingresar un numero")
    
    elif number != None:
        await typing_sleep(ctx)
        result = functions.fibonacci(number)
        await ctx.send(f"El enesimo numero {number} en la sucesion de fibonacci es: {result}")
        print(f"{ctx.author.name} encontro el {number}esimo numero de fibonacci: {result}")


#------------------------------------------>>>>>
###-------------- Operaciones Matemáticas final ------------>>>>

#------> Slow Mode command <------
@bot.command()
@commands.has_permissions(kick_members=True)
async def setdelay(ctx, seconds: int):
    '''Define el modo lento a una cantidad determinada, debes tener permisos suficientes (kick permissions required)'''
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
async def dm(ctx, member: discord.Member, *, args=None):
    '''Envia un MD a un @usuario, solo funciona con @menciones...'''
    if member != None or args != None:
        try:
            await member.send(args)
            await typing_sleep(ctx)
            await ctx.channel.send(f"Le enviaste un md con éxito a: {member.name}")
            print(f"cmdMD||    {ctx.author.name} le envió un md a {member.name} diciendole: {args} a las {current_hour}")
        except:
            await typing_sleep(ctx)
            await ctx.channel.send("No se pudo enviar el dm, este comando funcion con @Mención y no con ID")       
    else:
        await typing_sleep(ctx)
        await ctx.channel.send("Debes @mencionar un usuario, seguido del mensaje a enviar!")
        print(f"cmdMD||     {ctx.author.name} falló al enviar un md")


#---> Mensajes a canales con el bot 13<---
@bot.command()
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

@bot.command()
async def tunear(ctx, order: int, *, args=None,):
    '''Tunea un texto, la sintaxis es #tunear <orden> <el_texto_que_quieras_tunear>, siendo el orden un numero del 1 al 7 (distintas fuentes)'''
    if args != None and order == 1:
        myThiccString = tuning.tunear1(args.replace("#tunear", ""))
        await typing_sleep(ctx)
        await ctx.send(myThiccString)
        print(f"cmdTunear1||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 2:
        myThiccString = tuning.tunear2(args.replace("#tunear", ""))
        await typing_sleep(ctx)
        await ctx.send(myThiccString)
        print(f"cmdTunear2||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 3:
        await typing_sleep(ctx)
        myThiccString = tuning.tunear3(args.replace("#tunear", ""))
        await ctx.send(myThiccString)
        print(f"cmdTunear3||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 4:
        await typing_sleep(ctx)
        myThiccString = tuning.tunear4(args.replace("#tunear", ""))
        await ctx.send(myThiccString)
        print(f"cmdTunear4||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 5:
        await typing_sleep(ctx)
        myThiccString = tuning.tunear5(args.replace("#tunear", ""))
        await ctx.send(myThiccString)
        print(f"cmdTunear5||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 6:
        await typing_sleep(ctx)
        myThiccString = tuning.tunear6(args.replace("#tunear", ""))
        await ctx.send(myThiccString)
        print(f"cmdTunear6||        {ctx.author.name} tuneó un texto el {current_hour}")

    elif args != None and order == 7:
        await typing_sleep(ctx)
        myThiccString = tuning.tunear7(args.replace("#tunear", ""))
        await ctx.send(myThiccString)
        print(f"cmdTunear6||        {ctx.author.name} tuneó un texto el {current_hour}")

    #else:
    elif args == None and order == None:
        await typing_sleep(ctx)
        #args == None and order == None        
        await ctx.send("Seguido del comando debes introducir un orden (1 a 6) seguido del texto a tunear")
        await ctx.send("A modo de ejemplo: **#tunear 4 textodepruebacopipedro**")
        print(f"cmdTunear||        {ctx.author.name} falló al tunear un texto el {current_hour}")

@tunear.error
async def tunear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Debes seguir la sintáxis #tunear <orden> <texto a tunear> siendo el orden un número del 1 al 7")
        await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** y\npara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")

#----------> Kick Command <---------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    '''Kick a un usuario, requiere permisos'''

    async with ctx.typing():    
        await asyncio.sleep(type_time)
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
                title=f"Kickeado porque {random.choice(listas.frases)}",
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
    async with ctx.typing():    
        await asyncio.sleep(type_time)
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
                title=f"Baneado porque {random.choice(listas.frases)}",
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


#------------>  interaccion con el bot 2  <---------------
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
    if message.author == bot.user: #bot.user: changed from "client.user:"
        return
    if msg.startswith('#che'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    if msg.startswith('#bot'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    if msg.startswith('#bigobot'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    if msg.startswith('#copibot'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#ey'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#tevenin'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#capo'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#claudia'):
        await message.channel.send("{}".format(random.choice(listas.lacla)))
    elif msg.startswith('#flaco'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#ruben'):
        await message.channel.send("{}".format(random.choice(listas.rubenes)))
    elif msg.startswith('#pibe'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#rubén'):
        await message.channel.send("{}".format(random.choice(listas.rubenes)))
    elif msg.startswith('#nico'):
        await message.channel.send("{}".format(random.choice(listas.nicolas)))
    elif msg.startswith('#seki'):
        await message.channel.send("{}".format(random.choice(listas.sekiam)))
    elif msg.startswith('#franc'):
        await message.channel.send("{}".format(random.choice(listas.sekiam)))
    elif msg.startswith('#franki'):
        await message.channel.send("{}".format(random.choice(listas.sekiam)))
    elif msg.startswith('#copi'):
        await message.channel.send('pedro')
    elif msg.startswith('#hola'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#Hola'):
        await message.channel.send("{}".format(random.choice(listas.botCall)))
    elif msg.startswith('#claudio'):
        await message.channel.send('ese está en plaza huincul')
    elif msg.startswith('#hentai'):
        await message.channel.send('sos pajin eh :alien:')
    elif msg.startswith('#mato'):
        await message.channel.send("{}".format(random.choice(listas.matote)))
    elif msg.startswith('#matu'):
        await message.channel.send("{}".format(random.choice(listas.matote)))
    elif msg.startswith('#Mato'):
        await message.channel.send("{}".format(random.choice(listas.matote)))
    elif msg.startswith('#lezca'):
        await message.channel.send("{}".format(random.choice(listas.inválido)))
    elif msg.startswith('#lesca'):
        await message.channel.send("{}".format(random.choice(listas.inválido)))
    elif msg.startswith('#firu'):
        await message.channel.send("wof wof xd")
    elif msg.startswith('#ursula'):
        await message.channel.send('gorda mala leche como dijeron <@!343963045682216960> y <@!343971450644070410>') #primero el tambo segundo el nico
    elif msg.startswith('-monsa'):
        await message.channel.send('mi creador')
    elif msg.startswith('#menem'):
        await message.channel.send('se movió a la bolocco ese un capo')
    elif msg.startswith('-Monsa'):
        await message.channel.send('un distinto')
    elif msg.startswith('-tadeo'):
        await message.channel.send('gordo puto, por cierto, con "#tadeo" pones el video ( ͡° ͜ʖ ͡°) 🚴‍♂️')
    elif msg.startswith('#costi'):
        await message.channel.send('un carnasa 🐕')
    elif msg.startswith('#pela'):
        await message.channel.send('un capo')
    elif msg.startswith('#tambo'):
        await message.channel.send("{}".format(random.choice(listas.tamborindegui)))
    elif msg.startswith('#tobo'):
        await message.channel.send("{}".format(random.choice(listas.tamborindegui)))
    elif msg.startswith('#pepo'):
        await message.channel.send('ese tambien es puto')
    elif msg.startswith('#puto'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#tonto'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#trolo'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#gil'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#forro'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#bigote'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#tuma'):
        await message.channel.send("{}".format(random.choice(listas.bardeo)))
    elif msg.startswith('#jose'):
        await message.channel.send("{}".format(random.choice(listas.jopiyo)))
    elif msg.startswith('#jopi'):
        await message.channel.send("{}".format(random.choice(listas.jopiyo)))
    elif msg.startswith('#Jopi'):
        await message.channel.send("{}".format(random.choice(listas.jopiyo)))
    elif msg.startswith('#Nico'): 
        await message.channel.send("{}".format(random.choice(listas.nicolas)))
    elif msg.startswith('#reteke'): 
        await message.channel.send("{}".format(random.choice(listas.aquitocartes)))
    elif msg.startswith('#rtk'): 
        await message.channel.send("{}".format(random.choice(listas.aquitocartes)))
    elif msg.startswith('#aquito'): 
        await message.channel.send("{}".format(random.choice(listas.aquitocartes)))
    elif msg.startswith('#wens'): 
        await message.channel.send("{}".format(random.choice(listas.nicolas)))  
    elif msg.startswith('#ecla'): 
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#beje'): 
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#sofi'): 
        await message.channel.send("{}".format(random.choice(listas.sofia)))
    elif msg.startswith('#araragi'):
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#dante'):
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#masilo'):
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#sousken'):
        await message.channel.send("{}".format(random.choice(listas.asociados)))
    elif msg.startswith('#among'):
        await message.channel.send("{}".format(random.choice(listas.amongo)))
    elif msg.startswith('#waif'):
        await message.channel.send("{}".format(random.choice(listas.waifu)))   
    elif msg.startswith('#pecetote'): 
        await message.channel.send("rey de reyes")
        return

    if msg.startswith('#copipedro'):
        channel = message.channel
        await channel.send('<:copi:770818273217609758>')
        return

    '''
    spamsentences = ["#meme", "copipedro"]
    for i in range(len(spamsentences)):
        if spamsentences[i] in message.content:
            await asyncio.sleep(15) 
            for j in range(5):
                await message.channel.send("Bajá un cambio amigo no spam que se enoja el tambo...")
    '''


#-----------------> Clima comando <-----------------

# openweathermap api key sensible stored in .env 
api_key = os.getenv('OWM_API_KEY')
@bot.command()
async def clima(ctx, *, location: str=None):
    '''Clima de la ubicacion que introduzcas'''
    if location == None:
        await ctx.send('Debes seguir la sintaxis #clima <ubicacion>')
    elif location != None:
        location = str(location.lower())
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric' # change metric for imperial if u prefer degrees in farenheit
        try:
            weather_json = requests.get(weather_url).json() 
            await typing_sleep(ctx)
            embed_weather = discord.Embed(
                    title=f'Clima en {location} ',
                    description=f'Asi esta el clima en {location}.',
                    color=discord.Colour.gold(),
                    timestamp = datetime.utcnow())
            if weather_json['weather'][0]['main'] == 'Clouds':
                    actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835639669030942/cloudy.png"
                    weather_traduction = "Nubes."
            elif weather_json['weather'][0]['main'] == 'Clear':
                    actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835642999046144/soleado.png"
                    weather_traduction = "Despejado."
            elif weather_json['weather'][0]['main'] == 'Rain':
                actual_state = "https://cdn.discordapp.com/attachments/793309880861458473/804835641904726016/lluvia.png"
                weather_traduction = "Lluvia."
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
            await ctx.send(embed=embed_weather)
            print(f'cmdClima||        {ctx.author.name} solicito el clima en {location} a las {current_hora}')

        except KeyError:
            await typing_sleep(ctx)
            error_embed = discord.Embed(title='Hubo un error', description=f'No fue posible encontrar el clima para {location}...')
            await ctx.send(embed=error_embed)
            print(f'cmdClima||        {ctx.author.name} fallo al solicitar el clima de {location}')

#---------> juego command <--------
@bot.command()
async def juego(ctx):
    '''ta te ti y otros juegos (otros juegos estan por venir)'''
    await game.LoadGames(ctx, bot)    

@bot.command()
async def ppt(ctx, member : discord.Member=None):
    '''Piedra papel o tijeras contra jugador que menciones'''
    try:
        await game.ppt(ctx, bot, member=member)
    except AttributeError as e:
        await typing_sleep(ctx)
        await ctx.send("An exception occurred :disappointed:")
        await ctx.send(f"```{e.args}```")
        print("An attribute error seems to have appeared but just ignore it and continue! :)")
#-------> juego command end <------

@bot.command()
async def qr(ctx, *, qrstring: str=None):
    '''ES: Crea y devuelve el QR de un texto, puede ser un texto cualquiera, URL, etc. No 
    funciona con imagenes y otro tipo de archivos
    EN: Creates and returns a QR code of any text, images are not supported...'''
    if qrstring == None:
        await typing_sleep(ctx)
        await ctx.send(f'{ctx.author.mention} debes seguir la sintaxis #qr <texto a convertir> \n Solo funciona con textos, ej: urls, links, etc., no con numeros...')
        await asyncio.sleep(15)
        await ctx.channel.purge(limit=2)  # elimina los 2 mensajes anteriores...
    
    elif qrstring != None:
        url = pyqrcode.create(qrstring)
        url.png('images/qr.png', scale=6)  # saves qr image
        await typing_sleep(ctx)
        await ctx.send(f'{ctx.author.mention} aca esta tu QR', file=discord.File('images/qr.png'))
        #await ctx.send(file=discord.File('images/qr.png'))
            
# ---------> Purge messages of a mentioned user <--------
@bot.command()
async def borrar(ctx, limit=10, member: discord.Member=None):
    '''
    Borra una cantidad determinada de mensajes, por defecto 10 mensajes pero puedes establecer una 
    cantidad. El argumento <member> pemite borrar especificamente los mensajes de dicho miembro @mencionado
    Por ejemplo: #borrar <cantidad_de_mensajes_que_deseas_borrar> <usuario_de_quien_borrar_mensajes>
    #borrar a secas causara una eliminacion de 40 mensajes, #borrar 10 @usuario_c causara una eliminacion
    de los ultimos 10 mensajes del usuario_c....
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
            return await ctx.send(f"{limit} mensajes borrados", delete_after=12)
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await typing_sleep(ctx)
        await ctx.send(f"{limit} mensajes borrados de {member.mention}", delete_after=12)
    
    except errors.CommandInvokeError:
        await typing_sleep(ctx)
        await ctx.send(f"{ctx.author.name} solo es posible borrar mensajes con menos de 14 dias de antiguedad...")


# cog loader cmd
bot_developer_id = '485259816399536128'
@bot.command()
async def load(ctx, extension):
    '''Loads an specific cog, developer only!'''
    id = str(ctx.author.id)
    if id == f'{bot_developer_id}':
        bot.load_extension(f'cogs.{extension}')
        await typing_sleep(ctx)
        await ctx.send(f"{ctx.author.name} cargaste el cog {extension} con exito")
        print(f'cmdLoad||     {ctx.author.name} cargo un cogs')
    else:
        await typing_sleep(ctx)
        await ctx.send("Solo el desarrollador puede cargar/habilitar los cogs del bot")

# cog unloader cmdf
@bot.command()
async def unload(ctx, extension):
    '''Unloads an specific cog, developer only!'''
    id = str(ctx.author.id)
    if id == f'{bot_developer_id}':
        bot.unload_extension(f'cogs.{extension}')
        await typing_sleep(ctx)
        await ctx.send(f"{ctx.author.name} descargaste el cog {extension} con exito")
        print(f'cmdUnload||   {ctx.author.name} descargo un cogs')
    else:
        await typing_sleep(ctx)
        await ctx.send("Solo el desarrollador puede cargar/habilitar los cogs del bot")


# ---> ping con latencia  4<----
@bot.command()
async def ping(ctx, arg=None):
    '''Muestra tu ping con respecto al bot'''
    if arg == "pong":
        await typing_sleep(ctx)
        await ctx.send("ah chistoso")
    else:
        await typing_sleep(ctx)
        await ctx.send(f"Tu ping es: {round(bot.latency * 1000)}ms\nEste ping es con respecto a mí, no con respecto a los servidores de discord!!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.getenv('TOKEN'))
