from datetime import datetime, timedelta
from random import choice

import discord.colour
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions

#from ..db import db


numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")


class Reactions(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.polls = []
		self.giveaways = []
	
		
	@Cog.listener()
	async def on_ready(self):
		print("cog de reacciones listo")
	
	
	@command(name="createpoll", aliases=['encuesta'])
	@has_permissions(manage_guild=True)
	async def mkpoll(self, ctx, question: str=None, *options):
		'''Crea una encuesta, seguido de las opciones que introduzcas (max. 10 opc.).
		Sigue '''
		if question == None or options == None:
			await ctx.send('Para crear una encuesta debes seguir la sintaxis #encuesta <"**titulo** de tu encuesta" (si el titulo contiene mas de 1 palabra debe ir en comillas)> <opciones>')
			await ctx.send('el **titulo** debe estar entre comillas ---> "" y pueden haber hasta 10 opciones, no mas.')
			
		elif len(options) > 10:
			await ctx.send("Solo pueden haber 10 opciones en la encuesta!")

		# instead of numbers reaction, yes or not reaction!
		elif len(options) == 2:
			embed = Embed(title=question, 
						  #description=question,
						  colour = discord.Colour.red(),
						  timestamp=datetime.utcnow())

			fields = [("Decide", "\n".join([f"{numbers[idx]} ---> {option}" for idx, option in enumerate(options)]), False),
					  ("Instrucciones", "Votar si o no", False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			message = await ctx.send(embed=embed)

			await message.add_reaction('✅')
			await message.add_reaction("🚫")

			print(f"cmdEncuesta||     {ctx.author.name}#{ctx.author.discriminator} creo una encuesta con exito")

		# numbers reaction to vote
		else:
			embed = Embed(title=question, 
						  #description=question,
						  colour = discord.Colour.red(),
						  timestamp=datetime.utcnow())

			fields = [("Opciones", "\n".join([f"{numbers[idx]} ---> {option}" for idx, option in enumerate(options)]), False),
					  ("Instrucciones", "Reacciona la opcion que consideras...", False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			message = await ctx.send(embed=embed)

			for emoji in numbers[:len(options)]:
				await message.add_reaction(emoji)

			print(f"cmdEncuesta||     {ctx.author.name}#{ctx.author.discriminator} creo una encuesta con exito")

	@command(name="giveaway", aliases =['sorteo'])
	@has_permissions(manage_guild=True)
	async def mkgaw(self, ctx, mins: int, *, description: str):
		'''Crea un sorteo, seguido de una cuenta atras (en mins) y una descripcion que introduzcas'''
		embed = Embed(title="Sorteo",
					  description=description,
					  colour=ctx.author.colour,
					  timestamp=datetime.utcnow())

		fields = [("Termina en", f"{datetime.utcnow()+timedelta(seconds=mins*60)} UTC", False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline=inline)

		message = await ctx.send(embed=embed)
		await message.add_reaction("✅")

		self.giveaways.append((message.channel.id, message.id))

		self.bot.scheduler.add_job(self.complete_giveaway, "date", run_date=datetime.now()+timedelta(seconds=mins),
								   args=[message.channel.id, message.id])

	async def complete_poll(self, channel_id, message_id):
		message = await self.bot.get_channel(channel_id).fetch_message(message_id)

		most_voted = max(message.reactions, key=lambda r: r.count)

		await message.channel.send(f"Los resultados ya están y la opción {most_voted.emoji} fue la más popular con {most_voted.count-1:,} votos!")
		self.polls.remove((message.channel.id, message.id))

	async def complete_giveaway(self, channel_id, message_id):
		message = await self.bot.get_channel(channel_id).fetch_message(message_id)

		if len((entrants := [u for u in await message.reactions[0].users().flatten() if not u.bot])) > 0:
			winner = choice(entrants)
			await message.channel.send(f"Enhorabuena {winner.mention} - has ganado el sorteo!")
			self.giveaways.remove((message.channel.id, message.id))

		else:
			await message.channel.send("Sorteo finalizado - nadie entró!")
			self.giveaways.remove((message.channel.id, message.id))

	'''@Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if self.bot.ready and payload.message_id == self.reaction_message.id:
			current_colours = filter(lambda r: r in self.colours.values(), payload.member.roles)
			await payload.member.remove_roles(*current_colours, reason="Colour role reaction.")
			await payload.member.add_roles(self.colours[payload.emoji.name], reason="Colour role reaction.")
			await self.reaction_message.remove_reaction(payload.emoji, payload.member)

		elif payload.message_id in (poll[1] for poll in self.polls):
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

			for reaction in message.reactions:
				if (not payload.member.bot
					and payload.member in await reaction.users().flatten()
					and reaction.emoji != payload.emoji.name):
					await message.remove_reaction(reaction.emoji, payload.member)

		elif payload.emoji.name == "⭐":
			message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)

			if not message.author.bot and payload.member.id != message.author.id:
				msg_id, stars = db.record("SELECT StarMessageID, Stars FROM starboard WHERE RootMessageID = ?",
										  message.id) or (None, 0)

				embed = Embed(title="Starred message",
							  colour=message.author.colour,
							  timestamp=datetime.utcnow())

				fields = [("Author", message.author.mention, False),
						  ("Content", message.content or "See attachment", False),
						  ("Stars", stars+1, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				if len(message.attachments):
					embed.set_image(url=message.attachments[0].url)

				if not stars:
					star_message = await self.starboard_channel.send(embed=embed)
					db.execute("INSERT INTO starboard (RootMessageID, StarMessageID) VALUES (?, ?)",
							   message.id, star_message.id)

				else:
					star_message = await self.starboard_channel.fetch_message(msg_id)
					await star_message.edit(embed=embed)
					db.execute("UPDATE starboard SET Stars = Stars + 1 WHERE RootMessageID = ?", message.id)

			else:
				await message.remove_reaction(payload.emoji, payload.member)

		elif AttributeError:
			print("error acerca de las reacciones (poll n gaws")'''

def setup(bot):
	bot.add_cog(Reactions(bot))