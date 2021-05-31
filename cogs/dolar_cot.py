import typing
import discord
from discord.colour import Color
from discord.ext import commands
import requests
from apis.functions import printt, typing_sleep

DOLAR_URL = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
DOLAR_THUMBNAIL = "https://cdn.discordapp.com/attachments/793309880861458473/801587601474715648/dollar.png"

class DolarCotizacion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        printt("cog de cotizacion del dolar funcionando")

    @commands.command()
    async def dolar(self, ctx):
        ''' Cotizacion del dolar argentino en diversas variantes '''
        try:
            dolar_request = requests.get(DOLAR_URL)
        except Exception as e:
            await ctx.send(f"Ocurrio un error al obtener las cotizaciones. ```**Info detallada***:{e}\n**Razon**:{e.args}```")
            printt(f"====| Ocurrio un error al extraer el json del dolar. Exc:{e}\nArgs:{e.args}")

        if dolar_request.status_code == 200: 
            dolar_json = dolar_request.json()
            
            compraOfi = dolar_json[0]['casa']['compra'][:-1]
            ventaOfi = dolar_json[0]['casa']['venta'][:-1]
            varOfi = dolar_json[0]['casa']['variacion'][:-1]
            dolarSolid = str(float(dolar_json[0]['casa']['venta'][:-1].replace(",", ".")[:4]) * 1.65)
            compraBlue = dolar_json[1]['casa']['compra'][:-1]
            ventaBlue = dolar_json[1]['casa']['venta'][:-1]
            varBlue = dolar_json[1]['casa']['variacion'][:-1]
            compraCcl = dolar_json[3]['casa']['compra'][:-1]
            ventaCcl = dolar_json[3]['casa']['venta'][:-1]
            varCcl = dolar_json[3]['casa']['variacion'][:-1]
            compraBolsa = dolar_json[4]['casa']['compra'][:-1]
            ventaBolsa = dolar_json[4]['casa']['venta'][:-1]
            varBolsa = dolar_json[4]['casa']['variacion'][:-1]
            precioBitcoin = str(dolar_json[5]['casa']['venta'])[:-2]

            embedDolar = discord.Embed(
                Title = "Cotización del dolar",
                color = discord.Colour.green())
            embedDolar.set_thumbnail(url=DOLAR_THUMBNAIL)  
            embedDolar.add_field(name=':blue_circle:  Blue:', value=f"Compra: {compraBlue} | Venta: {ventaBlue} | Var. 24h: {varBlue}", inline=False)
            embedDolar.add_field(name=':green_circle:  Oficial:', value=f"Compra: {compraOfi} | Venta: {ventaOfi} | Var. 24h: {varOfi}", inline=False)
            embedDolar.add_field(name=':green_circle:  Oficial con impuestos (El que importa):', value=f"Valor aproximado de: {dolarSolid}", inline=False)
            embedDolar.add_field(name=':yellow_circle:  Bolsa:', value=f"Compra: {compraBolsa} | Venta: {ventaBolsa} | Var. 24h: {varBolsa}", inline=False)
            embedDolar.add_field(name=':orange_circle:  Contado con liqui:', value=f"Compra: {compraCcl} | Venta: {ventaCcl} | Var. 24h: {varCcl}", inline=False)
            embedDolar.add_field(name=':orange_circle:  Precio del Bitcoin:', value=f"Valor aproximado medio: {precioBitcoin}", inline=False)
            
            
            await typing_sleep(ctx)
            await ctx.send(embed=embedDolar)
            print(f"cmdDolar||            {ctx.author.name} solicitó la cot. del dolar")


    @commands.command()
    async def calculardolar(self, ctx, amount):
        """ Comando para convertir pesos a dolares """
        try:
            dolar_req = requests.get(DOLAR_URL)
        except Exception as e:
            await typing_sleep(ctx)
            await ctx.send(f"Ocurrio un error al obtener las cotizaciones. ```**Info detallada***:{e}\n**Razon**:{e.args}\n**Traceback**:{e.with_traceback}```")

        if dolar_req.status_code == 200:
            
            dolarJson = dolar_req.json()
            dolarSolid = float(dolarJson[0]['casa']['venta'][:-1].replace(",", ".")[:6]) * 1.65
            final = float(amount) * dolarSolid

            embed=discord.Embed(
                title=":repeat: Conversion de pesos a dolares", 
                description=f" :dollar: | **{amount}** ARS valen **{final}** USD", 
                Color= discord.Colour.green()
            )
            embed.set_thumbnail(url=DOLAR_THUMBNAIL)
            embed.set_footer(text=f"Considerando 1USD / {str(dolarSolid)[:-2]}ARS")

            await typing_sleep(ctx)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(DolarCotizacion(bot))
