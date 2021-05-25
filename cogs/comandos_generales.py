# Original author AlexFlipnote / discord_bot.py
# Repo: https://github.com/AlexFlipnote/discord_bot.py

import discord

from io import BytesIO
from apis import default
from discord.ext import commands
from time import strftime
import json

from functions import (bro_birthdays_check,  # required by usuario command
                        typing_sleep,
                        printt,
                      )


class Comandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.Cog.listener()
    async def on_ready(self):
        printt('cog de comandos listo')


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
        await ctx.send(embed=embed)


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


def setup(bot):
    bot.add_cog(Comandos(bot))