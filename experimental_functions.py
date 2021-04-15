import json

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageOps



#from facebook_scraper import get_posts

# this gets the last posts from the epet 14 page 
#for post in get_posts('EPET-14-Institucional-312214785790856', pages=10, extra_info=True):
    #print(post['text'][:50])
    #print("<---------------->")
#print(*post)



def get_json(url: str, json_name: str, indent=2):
    '''saves a json of a url with an specified name and indent(default 2)'''
    j = requests.get(url).json()
    with open(f'json_files/{json_name}.json', 'w') as f:
        json.dump(j, f, indent=indent)
    print(f'json: {json_name} saved succesfully')

get_json('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US', 'pepe2', 2)

#print("----------------------------------------------------------------")

def print_json(file_path: str, indent=2):
    '''Prints a json, takes filepath and indent arguments'''
    with open(f'{file_path}') as temp:
        data = json.loads(temp.read())
        print(json.dumps(data, indent=indent))

#print("----------------------------------------------------------------")

'''
print("Hi what would you like to calculate?\n")
print("Press 1 for Coulombs' law: ")
print("Press 2 for other thing")
option = int(input()
if option is 1:
    print("you choosen 1 succesfully")
elif option is 2:
    print("you choosen 2 succesfully")
'''

'''
# calcula fuerza resutlante de 2 cargas 
def fuerza(q1:float,q2:float,r:float) -> float:
    k = (8.99)*(10**9)                      # constante de coulomb 
    resultant_force = (k*q1*q1)/(r**2)      # calcula la fuerza resultante
    if resultant_force < 0:
        resultant_state = 'Atraccion'
    elif resultant_force > 0:
        resultant_state = 'Repulsion'
    return [resultant_force, resultant_state]      
q1   = float(input("Ingrese el valor de la primera carga\n"))
q2   = float(input("Ingrese el valor de la segunda carga\n"))
r = float(input("Ingrese el valor de la distancia ente ambas cargas\n"))
print("El valor de la fuerza entre las dos cargas es: " + str(fuerza(q1,q2,r)[0]))
print('La fuerza que se experimento fue de ' + fuerza(q1,q2,r)[1])
#############
###### ARREGLAR LA ENTRADA NO LA TOMA CON EXPONENTES!!!!!!!!!!!
'''


#------------------------------------------------------->>>>>>
# THIS ONE WORKED BUT NOT AT 100%
# THE PIC SAVES WEEIIIIIIIIRD
# Open the input image as numpy array, convert to RGB

#img=Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\avatar_save.jpg").convert("RGB")
#npImage=np.array(img)
#h,w=img.size

# Create same size alpha layer with circle
#alpha = Image.new('L', img.size,0)
#draw = ImageDraw.Draw(alpha)
#draw.pieslice([0,0,h,w],0,360,fill=255)

# Convert alpha Image to numpy array
#npAlpha=np.array(alpha)

# Add alpha layer to RGB
#npImage=np.dstack((npImage,npAlpha))

# Save with alpha
#Image.fromarray(npImage).save('result2.png')

#portada = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\demo_city.png")

#idraw = ImageDraw.Draw(portada)

#avataravatar = Image.open('result2.png')
#portada.paste(avataravatar, (40, 30))
#portada.save("images/profile_saveprueba.png")
#------------------------------------------------------->>>>>>


#---------------------------------------------------------------->>>>>>>>>>
#----->>> THIS ONE WORKS TOO BUT PRINTS WEIRD AGAIN JUST LIKE THE ONE ABOVE WITH NUMPY
#THIS IS TO MAKE THE IMGUSER CIRCULAR BUT NOT WORKING
# ALSO THIS ONE HAS BETTER QUALITY 
#imguser=Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\avatar_save.jpg")
#bigsize = (imguser.size[0] * 3, imguser.size[1] * 3)
#mask = Image.new('L', bigsize, 0)
#draw = ImageDraw.Draw(mask) 
#draw.ellipse((0, 0) + bigsize, fill=255)
#mask = mask.resize(imguser.size, Image.ANTIALIAS)
#imguser.putalpha(mask)
#output = ImageOps.fit(imguser, mask.size)#, centering=(0.5, 0.5))
#output.putalpha(mask)
#output.save('images/output222.png') 

#avatar222 =  Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\output222.png") 

#portada222 = Image.open(r"C:\Users\Juli\Desktop\Python Code\Prueba2\images\demo_city.png")
#portada222.paste(avatar222, (120, 90))
#portada222.save("images/profile_saveprueba222.png")
#---------------------------------------------------------------->>>>>>>>>>

'''
# A LEVEL SYSTEM WITH .JSON!!
@bot.event
async def on_message(message):
    if not message.author.bot:
        print('function load')
        with open('level.json','r') as f:
            users = json.load(f)
            print('file load')
        await update_data(users, message.author,message.guild)
        await add_experience(users, message.author, 4, message.guild)
        await level_up(users, message.author,message.channel, message.guild)

        with open('level.json','w') as f:
            json.dump(users, f)
    await bot.process_commands(message)

async def update_data(users, user,server):
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

async def add_experience(users, user, exp, server):
  users[str(user.guild.id)][str(user.id)]['experience'] += exp

async def level_up(users, user, channel, server):
  experience = users[str(user.guild.id)][str(user.id)]['experience']
  lvl_start = users[str(user.guild.id)][str(user.id)]['level']
  lvl_end = int(experience ** (1/4))
  if str(user.guild.id) != '559592087054450690':
    if lvl_start < lvl_end:
      await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
      users[str(user.guild.id)][str(user.id)]['level'] = lvl_end

@bot.command(aliases = ['rank','lvl'])
async def level(ctx,member: discord.Member = None):

    if not member:
        user = ctx.message.author
        with open('level.json','r') as f:
            users = json.load(f)
        lvl = users[str(ctx.guild.id)][str(user.id)]['level']
        exp = users[str(ctx.guild.id)][str(user.id)]['experience']

        embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP " ,color = discord.Color.green())
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)
    else:
      with open('level.json','r') as f:
          users = json.load(f)
      lvl = users[str(ctx.guild.id)][str(member.id)]['level']
      exp = users[str(ctx.guild.id)][str(member.id)]['experience']
      embed = discord.Embed(title = 'Level {}'.format(lvl), description = f"{exp} XP" ,color = discord.Color.green())
      embed.set_author(name = member, icon_url = member.avatar_url)

      await ctx.send(embed = embed)
'''


# direccion del viento 
def degrees_to_cardinal(d):
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
#dedede = int(input("please enter a degree to convert it into a cardinal point"))
#print(degrees_to_cardinal(dedede))

# borra los espacios
def del_spacebar(text: str):
    return ("".join(text.split()))

#print(del_spacebar(input()))

########################################
def fib(n: int):
    try:
        a = 0
        b = 1
        
        for _ in range(n):
            c = b+a
            #print(c)
            a = b
            #print(a)
            b = c
            #print(b)
            
        return str(a)

    except ValueError:
        print("you must enter an integer")


#your_num = int(input("enter a number to test fib func: "))
#print(f"result is: {fib(your_num)}")

########################################

def find_words(text: str):
    words = []
    split_text = text.split()
    for i in split_text:
        if i[-1] == 's':
            words.append(i)
    return "_".join(words)

pepe = input()
#print(find_words(pepe))

#########################################

def camel_to_snake(word: str):
    '''this functions prints, doesn't return...'''
    final_word = word[0].lower()
    for i in word[1:]:
        if i.isupper(): 
            final_word += "_"
        final_word += i.lower()
    print(final_word)
#camel_to_snake("")

#########################################

def dec_to_hex(decimal: int):
    return hex(int(decimal))[2:].upper()

def hex_to_dec(hex: str):
    return str(int(hex, 16))

def num_to_roman(entero: int):
    numeros = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerales = ['M', 'CM', 'D', 
                'CD', 'C', 'XC', 
                'L', 'XL', 'X', 
                'IX', 'V', 'IV', 
                'I']

    numeral = ''
    i = 0

    if entero > 3999:
        print("It's not possible to convert integers greater than 3999\nspecial grammar is required...")
    elif entero <= 3999:
        while entero > 0:
            for _ in range(entero // numeros[i]):
                numeral += numerales[i]
                entero -= numeros[i]
            i += 1

    return numeral

print("Exiting :)")
exit()
