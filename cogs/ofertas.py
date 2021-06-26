import discord
from discord.colour import Color
from discord.ext import commands
import requests
import json
from datetime import datetime

from apis.functions import printt, typing_sleep


EPIC_JSON = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=US&allowCountries=US"
EPIC_FREE_GAMES_WEB = "https://www.epicgames.com/store/es-ES/free-games"
STEAM_SALES = "https://www.cheapshark.com/api/1.0/deals?storeID=1&onSale=1"
UPLAY_SALES = "https://www.cheapshark.com/api/1.0/deals?storeID=13&upperPrice=15&onSale=1"
HUMBLE_SALES = "https://www.cheapshark.com/api/1.0/deals?storeID=11&upperPrice=15&onSale=1"
ORIGIN_SALES = "https://www.cheapshark.com/api/1.0/deals?storeID=8&upperPrice=20&onSale=1"


#def get_cheapshark_info()


class OfertasJuegos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        printt("cog de ofertas de juegos listo")

    
    @commands.command()
    async def ofertas(self, ctx, platform:str=None, amount:int=6):
        """
        Comando que muestra ofertas de juegos de distintas plataformas.
        Argumento 1 platform: steam, epic, uplay, entre otras...
        Argumento 2 amount: cantidad de ofertas a enviar, por defecto 5.
        Ejemplo de comando ------>  `#ofertas steam`
        Ejemplo 2 -------------->  `#ofertas epic`
        Plataformas soportadas:
            • Steam.
            • Epic.
            • Uplay.
            • Origin.
            • Humble Store.
            • Mas en el futuro...
        """
        if platform is None:
            await ctx.send(f"{ctx.author.name} actualmente el comando esta en desarrollo y pueden haber errores. Utiliza #help ofertas")

        # here goes the whole epic command
        elif platform.lower() == 'epic':
            platform = 'epic'

            req = requests.get(EPIC_JSON).json()
            title1 = req['data']['Catalog']['searchStore']['elements'][0]['title']  # str

            if title1 == "Mistery Game":
                seller1 = req['data']['Catalog']['searchStore']['elements'][2]['seller']['name']  # str 
                price1 = req['data']['Catalog']['searchStore']['elements'][2]['price']['totalPrice']['fmtPrice']['originalPrice']  # str
            else:
                seller1 = req['data']['Catalog']['searchStore']['elements'][0]['seller']['name']  # str 
                price1 = req['data']['Catalog']['searchStore']['elements'][0]['price']['totalPrice']['fmtPrice']['originalPrice']  # str

            try:
                thumbnail1 = req['data']['Catalog']['searchStore']['elements'][0]['keyImages'][2]['url']  # str 
            except IndexError:
                thumbnail1 =  req['data']['Catalog']['searchStore']['elements'][0]['keyImages'][0]['url']  # str    

            try:
                effectiveDate1 = f"Desde: {str(req['data']['Catalog']['searchStore']['elements'][0]['effectiveDate'])[:10]}, hasta: {str(req['data']['Catalog']['searchStore']['elements'][0]['price']['lineOffers'][0]['appliedRules'][0]['endDate'])[:10]}"
            except IndexError:
                effectiveDate1 = f"Fecha de validez desconocida :("

            try:
                title2 =  req['data']['Catalog']['searchStore']['elements'][1]['title']
            except IndexError:
                title2 = ":exclamation: No pude encontrar el proximo juego gratis"
            try:
                title3 =  req['data']['Catalog']['searchStore']['elements'][2]['title']
            except IndexError:
                title3 = ":exclamation: No pude encontrar el proximo juego gratis"
            try:
                title4 =  req['data']['Catalog']['searchStore']['elements'][3]['title']
            except IndexError:
                title4 = ":exclamation: No pude encontrar el proximo juego gratis"

            embedGame1 = discord.Embed(
                    title = f'**Juegos gratis actuales en {platform}**',
                    description = f'[Reclamar juego]({EPIC_FREE_GAMES_WEB})',
                    color = discord.Color.purple(),
                    timestamp = datetime.utcnow()
                )
            embedGame1.add_field(name = "***Título***", value = title1, inline = False)
            embedGame1.add_field(name = "***Desarrolladora***", value = seller1, inline = True)
            embedGame1.add_field(name = "***Precio original***", value = f"{price1}USD, consultar #dolar", inline = False)
            embedGame1.add_field(name = "***Vigencia***", value = effectiveDate1, inline = True)
            embedGame1.set_image(url=thumbnail1)
            embedGame1.set_footer(icon_url = ctx.author.avatar_url, text = f"Peticion de {ctx.author.name}")

            embedGame2 = discord.Embed(title="Proximos juegos gratuitos",color=discord.Color.purple())
            embedGame2.add_field(name = f"Luego de {title1}:", value = f"{title2}")
            embedGame2.add_field(name = f"Luego de {title2}:", value = f"{title3}")
            embedGame2.add_field(name = f"Luego de {title3}:", value = f"{title4}")

            await ctx.message.delete()
            await typing_sleep(ctx)
            await ctx.send(embed = embedGame1, delete_after=420.0)
            await ctx.send(embed = embedGame2, delete_after=420.0)
            await ctx.send(f"Eso es todo por ahora {ctx.author.name}!", delete_after=360.0)
            print(f'cmdJuegosGratis||         Juego gratis para {ctx.author.name}')


        # here goes the whole steam command
        elif platform.lower() == 'steam':
            await ctx.message.delete()
            steam_json = requests.request("GET", STEAM_SALES, headers={}, data={}).json()
            
            for i in range(amount):
                game_title = steam_json[i]["title"]
                price_saved = f'Precio con descuento: {steam_json[i]["salePrice"]} USD, ahorras un {str(steam_json[i]["savings"])[:2]}%'
                rating = f'{steam_json[i]["steamRatingCount"]} personas reseñaron este juego y tiene una valoracion de {steam_json[i]["steamRatingPercent"]}'
                game_thumb = steam_json[i]["thumb"]
                embed = discord.Embed(title=game_title,Color=discord.Color.dark_blue())
                embed.add_field(name="Oferta",value=price_saved)
                embed.add_field(name="Valoracion",value=rating)
                embed.set_thumbnail(url=game_thumb)

                await ctx.send(f"Mostrando oferta {i} de {amount}", delete_after=360.0)
                await ctx.send(embed=embed, delete_after=360.0)

            await ctx.send("Estas fueron algunas de las ofertas de steam.")


        elif platform.lower() == 'uplay':
            await ctx.message.delete()
            uplay_json = requests.request("GET", UPLAY_SALES, headers={}, data={}).json()
             
            for i in range(amount):
                game_title = uplay_json[i]["title"]
                price_saved = f'Precio con descuento: {uplay_json[i]["salePrice"]} USD, ahorras un {str(uplay_json[i]["savings"])[:2]}%'
                rating = f'{uplay_json[i]["steamRatingCount"]} personas reseñaron este juego y tiene una valoracion de {uplay_json[i]["steamRatingPercent"]}'
                game_thumb = uplay_json[i]["thumb"]
                embed = discord.Embed(title=game_title,Color=discord.Color.dark_blue())
                embed.add_field(name="Oferta",value=price_saved)
                embed.add_field(name="Valoracion",value=rating)
                embed.set_thumbnail(url=game_thumb)

                await ctx.send(f"Mostrando oferta {i} de {amount}", delete_after=300.0)
                await ctx.send(embed=embed, delete_after=300.0)

            await ctx.send("Estas fueron algunas de las ofertas de Uplay.")


        elif 'humble' in platform.lower():
            await ctx.message.delete()
            humble_json = requests.request("GET", HUMBLE_SALES, headers={}, data={}).json()
             
            for i in range(amount):
                game_title = humble_json[i]["title"]
                price_saved = f'Precio con descuento: {humble_json[i]["salePrice"]} USD, ahorras un {str(humble_json[i]["savings"])[:2]}%'
                rating = f'{humble_json[i]["steamRatingCount"]} personas reseñaron este juego y tiene una valoracion de {humble_json[i]["steamRatingPercent"]}'
                game_thumb = humble_json[i]["thumb"]
                embed = discord.Embed(title=game_title,Color=discord.Color.dark_blue())
                embed.add_field(name="Oferta",value=price_saved)
                embed.add_field(name="Valoracion",value=rating)
                embed.set_thumbnail(url=game_thumb)

                await ctx.send(f"Mostrando oferta {i} de {amount}", delete_after=300.0)
                await ctx.send(embed=embed, delete_after=300.0)

            await ctx.send("Estas fueron algunas de las ofertas de la Humble Store")


        elif platform.lower() == 'origin':
            await ctx.message.delete()
            origin_json = requests.request("GET", ORIGIN_SALES, headers={}, data={}).json()
            lines = [i for i in origin_json[i]]
             
            for i in range(len(lines)):
                game_title = origin_json[i]["title"]
                price_saved = f'Precio con descuento: {origin_json[i]["salePrice"]} USD, ahorras un {str(origin_json[i]["savings"])[:2]}%'
                rating = f'{origin_json[i]["steamRatingCount"]} personas reseñaron este juego y tiene una valoracion de {origin_json[i]["steamRatingPercent"]}%'
                game_thumb = origin_json[i]["thumb"]
                embed = discord.Embed(title=game_title,Color=discord.Color.dark_blue())
                embed.add_field(name="Oferta",value=price_saved)
                embed.add_field(name="Valoracion",value=rating)
                embed.set_thumbnail(url=game_thumb)

                await ctx.send(f"Mostrando oferta {i} de 10", delete_after=300.0)
                await ctx.send(embed=embed, delete_after=300.0)

            await ctx.send("Estas fueron algunas de las ofertas de la Humble Store")

        else:
            pass


def setup(bot):
    bot.add_cog(OfertasJuegos(bot))
