"""
Monsa's custom functions
~~~~~~~~~~~~~~~~~~~~~~~~

Useful functions for a main.py cleaner
"""
# 1st function |Printt()| ==> 
from sys import stdout
from time import sleep

# 2nd function |Get_Dolar()| ==> 
import requests

# 3rd function |Bro_Birthdays_Check()| ==>
from apis.listas import brosId
import apis.broBdays

# 4th function |fibonacci()| ==>

# 5th function |get_apex_data()|
# Already imported requests library !!!
# dotenv required by tracker.gg API
from dotenv import load_dotenv
import os
load_dotenv()

# 6th function |typing_sleep()| ==>
from asyncio import sleep as asyncsleep
from random import uniform

# 7th function |degrees_to_cardinal()| ==>
# No libraries required.

# 8th function |word_to_emoji()| ==>
# No libraries required.

# 9th, 10th and 11th functions, required by json_level.py
# No libraries required.

# 12th function || ==>


# ====== Variables ======
type_time = uniform(0, 2)



# ====== Funciones ======
# 1st Function
def printt(string, delay=0.002):
    '''
    Print a string or f-string with delay between its characters.
    Argument delay float expected recommended 0.001 <= delay <= 0.2
    delay 2ms between every character by default
    Author: Lorenzo Campos, forked from his snake.py repl ...
    '''
    for character in string:
	    stdout.write(character)
	    stdout.flush()
	    sleep(delay)
    print("")


# 2nd function
def get_dolar(key):
    """Used in dolar cmd""" 
    DOLAR_URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    dolar_json = requests.get(DOLAR_URL).json()

    try:
        final_dict = {
            'compraOfi': dolar_json[0]['casa']['compra'][:-1],
            'ventaOfi': dolar_json[0]['casa']['venta'][:-1],
            'varOfi': dolar_json[0]['casa']['variacion'][:-1],
            'compraOfiSolid': str(float(dolar_json[0]['casa']['compra'][:-1]) * 1.65).replace(",", ".")[:6], # .replace() moved to outer str() instead of inner float
            'ventaOfiSolid': str(float(dolar_json[0]['casa']['venta'][:-1]) * 1.65).replace(",", ".")[:6], # .replace() moved to outer str() instead of inner float
            'compraBlue': dolar_json[1]['casa']['compra'][:-1],
            'ventaBlue': dolar_json[1]['casa']['venta'][:-1], 
            'varBlue': dolar_json[1]['casa']['variacion'][:-1],
            'compraCcl': dolar_json[3]['casa']['compra'][:-1],
            'ventaCcl': dolar_json[3]['casa']['venta'][:-1],
            'varCcl': dolar_json[3]['casa']['variacion'][:-1],
            'compraBolsa': dolar_json[4]['casa']['compra'][:-1],
            'ventaBolsa': dolar_json[4]['casa']['venta'][:-1],
            'varBolsa': dolar_json[4]['casa']['variacion'][:-1],
        }
        print("-----Cotizacion del dolar funcionando-------")
        return final_dict[key]

    except Exception as e:
        print(f"Ocurrio un error con la cotizacion del dolar, error: {e}, args: {e.args}")


# 3rd function
def bro_birthdays_check(member: int):
    '''ES: La funcion solo recibe el member.id (int)...
    EN: Function expects member.id integer type...'''
    if member == None:
        fecha_Cumple = "Fecha desconocida..."

    elif member == brosId['Nico']:
        fecha_Cumple = apis.broBdays.nicoBday
        return fecha_Cumple
    elif member == brosId['Reteke']: #rtk
        fecha_Cumple = apis.broBdays.rtkBday
        return fecha_Cumple
    elif member == brosId['Souskenin']: #ssk
        fecha_Cumple = apis.broBdays.sskBday
        return fecha_Cumple
    elif member == brosId['Sofi']: #sofi
        fecha_Cumple = apis.broBdays.sofiBday
        return fecha_Cumple
    elif member == brosId['Tambo']: #tambo
        fecha_Cumple = apis.broBdays.tamboBday
        return fecha_Cumple
    elif member == brosId['Jose']: #jose
        fecha_Cumple = apis.broBdays.jopiBday
        return fecha_Cumple
    elif member == brosId['Coppi']: #copi
        fecha_Cumple = apis.broBdays.copiBday
        return fecha_Cumple
    elif member == brosId['Mato']: #mato
        fecha_Cumple = apis.broBdays.matoBday
        return fecha_Cumple
    elif member == brosId['Seki']: #seki
        fecha_Cumple = apis.broBdays.sekiBday
        return fecha_Cumple    
    elif member == brosId['Monsa']: #yo
       fecha_Cumple = apis.broBdays.juliBday
       return fecha_Cumple
    elif member == brosId['Lezcano']: #lezca
        fecha_Cumple = apis.broBdays.lezcBday
        return fecha_Cumple  
    elif member == brosId['Bigobot']:  #bot 
        fecha_Cumple = apis.broBdays.botBday
        return fecha_Cumple
    elif member == brosId['Stalker']: #stalk
        fecha_Cumple = apis.broBdays.stalkerBday
        return fecha_Cumple 


# 4th function
def fibonacci(n: int):
    '''devuelve el enesimo numero de fibonacci'''
    a = 0
    b = 1
    
    for _ in range(n):
        c = b+a
        a = b
        b = c
        
    return str(a)


# 5th function
def get_apex_data(platform: str, username: str):
    """Used in cogs/Apex.py, expects two arguments(platform and user). API from tracker.gg"""
    tail = f'profile/{platform}/{username}'
    apex_req = requests.get(
        f"https://public-api.tracker.gg/v2/apex/standard/{tail}", 
        headers={"TRN-Api-Key": os.getenv('TRN-API-KEY')}
    )
    apex_json = apex_req.json()
    return apex_json, apex_req.ok


# 6th function
async def typing_sleep(ctx):
    """Async Function to avoid re-coding the typing and the sleep code once and once again"""
    async with ctx.typing():    
        await asyncsleep(type_time)


# 7th function
def degrees_to_cardinal(d: int):
    '''
    Converts a degree between 0 and 360 into cardinal point.
    Source: https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
    '''
    dirs = ['N - Norte', 
    'NNE - Nornoreste', 
    'NE - Noreste', 
    'ENE - Estenoreste', 
    'E - Este', 
    'ESE - Estesureste', 
    'SE - Sureste', 
    'SSE - Sursureste', 
    'S - Sur', 
    'SSO - Sursuroeste', 
    'SO - Suroeste', 
    'OSO - Oestesuroeste', 
    'O - Oeste', 
    'ONO - Oestenoroeste', 
    'NO - Noroeste', 
    'NNO - Nornoroeste']
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]


# 8th function
def word_to_emoji(word:str):
    """Converts a word:str into various letters discord emojis e.g: (:regional_indicator_x:)""" 
    word_list = []
    for letter in word:
        word_list.append(f":regional_indicator_{letter}:")
    return "".join(word_list)

# 9th function
async def update_data(users, user, server):
    """Required by json_level.py"""
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1

# 10th function
async def add_experience(users, user, exp, server):
    """Required by json_level.py"""
    users[str(user.guild.id)][str(user.id)]['experience'] += exp

#11th function
async def level_up(users, user, channel, server):
    """Required by json_level.py"""
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1/4))
    if str(user.guild.id) != 'pepe':
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
            users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

# 12th function
async def throw_error(ctx, e: Exception):
    """ 
    A custom function to easily send exceptions info 
    Recommended when: `Except Exception as e:`
    """
    await ctx.send(f":exclamation:  Hubo un error al ejecutar el comando. Info detallada:")
    await ctx.send(f"`Excepcion: {e}`\n`Razon: {e.args}`\n`Traceback: {e.with_traceback}`")