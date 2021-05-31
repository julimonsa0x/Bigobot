# Author: Some commands with their respective owners, others written by me.

import discord
from discord.ext import commands
from random import choice
from numpy import sqrt as numpy_sqrt
import math
from sympy import (Derivative, Integral, Limit, S, Symbol, diff, integrate,
                   limit, simplify)

from functions import printt, typing_sleep, fibonacci
from listas import intentoResta


class MateComandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready():
        printt("Cog de matecomandos listo")


    @commands.command()
    async def matecomandos(self, ctx):
        '''Comandos sobre matematicas'''
        embedMates = discord.Embed(
            color=discord.Colour.dark_blue(),
            title="Estas son las matemáticas que conoce el bot"
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

        await typing_sleep(ctx)
        await ctx.send(embed=embedMates)
        print(f"{ctx.author.name} solicitó los comandos matemáticos")


    #----> Convertir de binario a decimal <----
    #https://parzibyte.me/blog/2020/12/05/python-convertir-binario-decimal/
    @commands.command()
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
        await ctx.send(f"El binario: **{binary}** en decimal es: **{decimal}**")


    # ---> Convertir de decimal a binario <---
    # from geeksforgeeks
    @commands.command()
    async def dec_a_bin(ctx, decimal: int):
        '''Convierte un decimal dado, a binario'''
        bin_result = bin(decimal).replace("0b", "")
        bin_result2 = bin(decimal)[2:]
        print(bin_result2)
        await typing_sleep(ctx)
        await ctx.send(f"El decimal **{decimal}** en binario es: **{bin_result}**")


    # ----> Convertir de HEX a decimal <----
    # from geeks for geeks
    @commands.command()
    async def hex_a_dec(ctx, hex: str):
        '''Convierte un Hexadecimal dado, a decimal'''
        dec_result = int(hex, 16) 
        dec_result = str(dec_result)
        await typing_sleep(ctx)
        await ctx.send(f"El hexadecimal **{hex}** en decimal es: **{dec_result}**")


    # ---> Convertir de decimal a HEX <---
    @commands.command()
    async def dec_a_hex(ctx, decimal: int):
        '''Convierte un decimal dado, a hexadecimal'''
        hex_result = hex(int(decimal))[2:].upper()
        await typing_sleep(ctx)
        await ctx.send(f"El decimal **{decimal}** en hexadecimal es: **{hex_result}**")


    # ---> Convertir decimal a romano <----
    # from a spanish youtube channel, ep 751 i remember...
    @commands.command()
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
        await ctx.send(f"El numero **{numero_inicial}** en romano es **{numeral}**")
    ###------------- Comandos de conversiones Final ------------>>>>
    
    ################################################################
    
    ###-------------- Operaciones Matemáticas inicio------------>>>>
    @commands.command()
    async def suma(ctx, num1: int, num2: int):
        '''Suma dos numeros que introduzcas, deben estar separados
        a modo de ejemplo: #suma 1 5 -----> 6
        '''
        sumResult = num1 + num2
        await typing_sleep(ctx)
        await ctx.send("Resultado de la suma: ```{}``` " .format(sumResult))
        print(f'cmdSuma||   {ctx.author.name} sumó {num1} con {num2} ---> {sumResult}')

    @commands.command()
    async def resta(ctx, num1: int, num2: int):
        '''Resta dos numeros, deben estar separados
        a modo de ejemplo: #resta 20 15
        '''
        await typing_sleep(ctx)
        await ctx.send(choice(intentoResta))
        print(f'cmdResta||  {ctx.author.name} intentó restar jaja')

    @commands.command()
    async def mult(ctx, num1: int, num2: int):
        '''Multiplica dos numeros que introduzcas'''
        multResult = num1 * num2
        await typing_sleep(ctx)
        await ctx.send(" Resultado del producto: ```{}``` " .format(multResult))
        print(f'cmdMult||   {ctx.author.name} multiplicó dos numeros')

    @commands.command()
    async def division(ctx, num1: int, num2: int):
        '''Divide dos numeros que introduzcas'''
        divQuotient = (num1 // num2)
        divRemain = (num1 % num2)
        await typing_sleep(ctx)
        await ctx.send(f"El cociente da {divQuotient} y el resto queda {divRemain}")
        print(f'cmdDivision|| {ctx.author.name} dividió {num1} sobre {num2} ---> {divQuotient} | {divRemain}')

    @commands.command(aliases=['potencia','elevar'])
    async def pot(ctx, num1: int, num2: int):
        '''
        El 1er numero que introduzcas a la potencia del 2do
        ejemplo: #pot 3 3 ----> 3 al cubo ---> 27
        ejemplo 2 #pot 3 0.1
        '''
        potResult = num1 ** num2
        await typing_sleep(ctx)
        await ctx.send("Resultado: ```{}``` " .format(potResult))
        print(f'cmdPot||    {ctx.author.name} potenció un numero')

    @commands.command(aliases=['baskara','bascara'])
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
            await ctx.send(":exclamation: La solución de la ecuación es con numeros complejos :(")
            print(f'cmdBaskara||    La ecuación de {ctx.author.name} es compleja :(')
            
        else:
            try:
                realBaskEcuation = str(f"{numOne}x^2 {numTwo}x {numThree}")
                root1 = ((-numTwo)+(numTwo**2-(4*numOne*numThree))**0.5)/(2*numOne)   # Raíz positiva
                root2 = ((-numTwo)-(numTwo**2-(4*numOne*numThree))**0.5)/(2*numOne)   # Raíz negativa
                await typing_sleep(ctx)
                await ctx.send(" Parte positiva: ```{}``` " .format(root1))
                await ctx.send(" Parte negativa: ```{}``` " .format(root2))
                print(f'cmdBask||       {ctx.author.name} halló raices con éxito para la ecuación {realBaskEcuation} ----> {root1} y {root2}')
            except Exception as e:
                if isinstance(e, commands.MissingRequiredArgument):
                    await ctx.send("Debes seguir la sintáxis #bask <coeficiente cuadratico> <coeficiente lineal> <termino independiente> con sus respectivos signos...")
                    await ctx.send('https://cdn.discordapp.com/attachments/793309880861458473/804126063880830996/how_to_bask.png')
                    await ctx.send("Recuerda que si quieres ver la sintaxis especfica de un comando puedes recurrir a **#help <#comando>** ypara ver todos los comandos puedes recurrir a **#help** o **#ayuda** / **#comandos**")
                    print(f"cmdBask||     {ctx.author.name} quiso baskarear")

    @commands.command()
    async def raiz(ctx, num1: int): 
        '''La raiz cuadrada de un numero que introduzcas'''  
        sqrtResult = numpy_sqrt(num1)   
        await typing_sleep(ctx)
        await ctx.send("Resultado de la raíz: ```{}``` " .format(sqrtResult))
        print(f'cmdSqrt|| {ctx.author.name} halló la raíz cuadrada de {num1}, ---> {sqrtResult}')

    @commands.command()
    async def seno(ctx, num1: int):
        '''El seno de un grado que introduzcas'''
        sinResult = math.sin(math.radians(num1)) 
        await typing_sleep(ctx)
        await ctx.send("Resultado: ```{}``` " .format(sinResult))
        print(f'cmdPot||    {ctx.author.name} halló el seno de {num1} ---> {sinResult}')

    @commands.command()
    async def coseno(ctx, num1: int):
        '''El coseno de un grado que introduzcas'''
        cosResult = math.cos(math.radians(num1)) 
        await typing_sleep(ctx)
        await ctx.send("Resultado: ```{}``` " .format(cosResult))
        print(f'cmdPot||    {ctx.author.name} halló el coseno de {num1} ---> {cosResult}')

    @commands.command()
    async def tangente(ctx, num1: int):
        '''La tangente de un grado que introduzcas'''
        tanResult = math.tan(math.radians(num1)) 
        await typing_sleep(ctx)
        await ctx.send("Resultado: ```{}``` " .format(tanResult))
        print(f'cmdPot||    {ctx.author.name} halló la tangente de {num1} ---> {tanResult}')

    @commands.command()
    async def hipotenusa(ctx, num1: int, num2: int):
        '''Calcula la hipotenusa de dos numeros que introduzcas'''
        hipResult = math.hypot(num1, num2) 
        await typing_sleep(ctx)
        await ctx.send("Resultado: ```{}``` " .format(hipResult))
        print(f'cmdPot||    {ctx.author.name} halló la tangente de {num1} ---> {hipResult}')


    @commands.command()
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
            print(f"{ctx.author.name} halló el límite de {function} ---> {limitResult}")
        
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
            print(f"{ctx.author.name} falló al querer calcular un límite")
        

    @commands.command()
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
            print(f"{ctx.author.name} halló la derivada de {function} ---> {ddxResult}")
        
        else:
            await typing_sleep(ctx)
            await ctx.channel.send(f"Debes seguir la sintaxis #derivada[funcion]")
            await ctx.channel.send(f"{ctx.author.name} mira este ejemplo con *x²-10x")
            await ctx.channel.send(f"Entrada x²-10x: Debe ser ingresada así ``` x**2-10*x ```")
            await ctx.channel.send(f"Ignora el formateo de texto automatico de discord, en cuanto escribes esa funcion se te convertirá en ``` x*2-10x ```, tu solo dale enter por mas que se haya cambiado")
            await ctx.channel.send(f"Esto no es posible de evitar debido a que está implementado de manera predeterminada en discord pero el bot aun asi te dará el resultado correcto :thumbsup:")
            await ctx.channel.send(f"Por ultimo recordar que esto no pasa solo en esta funcion, ocurre en cualquier texto encerrado con asteriscos (se convierte en cursiva)")
            await ctx.channel.send(f"Salida: ``` 2*x-10 ```")
            print(f"{ctx.author.name} falló al querer calcular una derivada")


    @commands.command()
    async def integral(ctx, function=None, dif1=None, dif2=None):
        '''Halla la integral de una funcion, sintaxis #integral <funcion>. Recuerda que para multiplicar debe usarse * y para elevar (potencias) debe usarse **'''
        if function != None and dif1 == None and dif2 == None:
            fx = str(function)
            x = Symbol('x')
            intResult = Integral(fx, x).doit()
            await typing_sleep(ctx)
            await ctx.channel.send(f"La integral indefinida de {function} es:")
            await ctx.channel.send(f"``` {intResult} ```")
            print(f"{ctx.author.name} halló la integral indef. de {function} ---> {intResult}")
        
        elif function != None and dif1 != None and dif2 != None:
            fx = str(function)
            x = Symbol('x')
            a = int(dif1)
            b = int(dif2)
            intResult = Integral(fx, (x, a, b)).doit()
            await typing_sleep(ctx)
            await ctx.channel.send(f"La integral definida de {function} es:")
            await ctx.channel.send(f"``` {intResult} ```")
            print(f"{ctx.author.name} halló la integral def. de {function} ---> {intResult}")

        else:
            await typing_sleep(ctx)
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
            print(f"{ctx.author.name} falló al querer calcular una derivada")


    @commands.command()
    async def fib(ctx, number: int):
        '''Encuentra el enésimo numero de fibonacci'''
        if number == None:
            await typing_sleep(ctx)
            await ctx.send("Debes ingresar un numero")

        elif number != None:
            await typing_sleep(ctx)
            result = fibonacci(number)
            await ctx.send(f"El enesimo numero {number} en la sucesion de fibonacci es: {result}")
            print(f"{ctx.author.name} encontro el {number}esimo numero de fibonacci: {result}")


def setup(bot):
    bot.add_cog(MateComandos(bot))
