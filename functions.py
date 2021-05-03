"""Useful functions for a main.py cleaner"""
# 1st function |Printt| ==> 
from sys import stdout
from time import sleep

# 2nd function |Get_Dolar| ==> 
import requests

# 3rd function Bro_Birthdays_Check| ==>
from listas import brosId

# 4th function || ==>
import json
from dotenv import load_dotenv
import os
load_dotenv()

# 5th function || ==>
from asyncio import sleep as asyncsleep
from random import uniform

# 6th function || ==>
# 7th function || ==>



# ====== Variables ======
type_time = uniform(0.5, 2)




# 1st Function
def printt(string, delay=0.005):
    '''
    Print a string or f-string with delay between its characters.
    Argument delay float expected recommended 0.005 <= delay <= 0.2
    delay 5ms between every character by default
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
            'compraOfiSolid': str(float(dolar_json[0]['casa']['compra'][:-1].replace(",", ".")) * 1.65)[:6],
            'ventaOfiSolid': str(float(dolar_json[0]['casa']['venta'][:-1].replace(",", ".")) * 1.65)[:6],
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
        print(f"Ocurrio un error con la cotizacion del dolar, error: {e.message}, args: {e.args}")

# 3rd function
def bro_birthdays_check(member: int):
    '''ES: La funcion solo recibe el member.id (int)...
    EN: Function expects member.id integer type...'''
    if member == None:
        fecha_Cumple = "Fecha desconocida..."

    elif member == brosId['Nico']:
        fecha_Cumple = broBdays.nicoBday
        return fecha_Cumple
    elif member == brosId['Reteke']: #rtk
        fecha_Cumple = broBdays.rtkBday
        return fecha_Cumple
    elif member == brosId['Souskenin']: #ssk
        fecha_Cumple = broBdays.sskBday
        return fecha_Cumple
    elif member == brosId['Sofi']: #sofi
        fecha_Cumple = broBdays.sofiBday
        return fecha_Cumple
    elif member == brosId['Tambo']: #tambo
        fecha_Cumple = broBdays.tamboBday
        return fecha_Cumple
    elif member == brosId['Jose']: #jose
        fecha_Cumple = broBdays.jopiBday
        return fecha_Cumple
    elif member == brosId['Coppi']: #copi
        fecha_Cumple = broBdays.copiBday
        return fecha_Cumple
    elif member == brosId['Mato']: #mato
        fecha_Cumple = broBdays.matoBday
        return fecha_Cumple
    elif member == brosId['Seki']: #seki
        fecha_Cumple = broBdays.sekiBday
        return fecha_Cumple    
    elif member == brosId['Monsa']: #yo
       fecha_Cumple = broBdays.juliBday
       return fecha_Cumple
    elif member == brosId['Lezcano']: #lezca
        fecha_Cumple = broBdays.lezcBday
        return fecha_Cumple  
    elif member == brosId['Bigobot']:  #bot 
        fecha_Cumple = broBdays.botBday
        return fecha_Cumple
    elif member == brosId['Stalker']: #stalk
        fecha_Cumple = broBdays.stalkerBday
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
    """ Used in cogs/Apex.py, expects two arguments(platform and user)"""
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

# 8th function

# 9th function

# 10th function
