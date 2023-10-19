import discord
import json
import os
import time
from discord.ext import commands
#from keep_alive import keep_alive

with open("/data/data/com.termux/files/home/TOKEN.json", "r") as File:
	token = json.loads(File.read())
with open("pokename.json", "r") as File:
	pokename = json.loads(File.read())
with open("config.json", "r") as File:
	config = json.loads(File.read())

bot = commands.Bot(command_prefix="!", self_bot=True)
running = False
delay = 1.6

@bot.event
async def on_ready():
	print("Bot ready!")
	channel = bot.get_channel(config["channel_id"])
	await channel.send("!catch")

@bot.event
async def on_message(message):
	if message.channel.id == config["channel_id"]:
		global text, running, sleep
		user = str(message.author)
		if len(message.embeds) == 1 and user == "Pokétwo#8236" and message.embeds[0].image.url != None:
			running = False
			await message.channel.send("<@716390085896962058> hint")

		elif user == "Pokétwo#8236" and message.content.startswith("The pokémon is "):
			name = message.content.replace("\\", "")[15:-1]
			size = len(name)
			temp = pokename[str(size)]
			names = []
			for i in temp:
				key0 = False
				for j in range(size):
					if name[j] == "_":
						continue
					elif name[j] != i[j]:
						key0 = True
						break
				if key0:
					continue
				names.append(i)

			for i in names:
				await message.channel.send(f"<@716390085896962058> catch {i}")
				time.sleep(delay)

		elif user == "Pokétwo#8236" and message.content.startswith(f"Congratulations <@{config['alt_account_id']}>! You caught a "):
			print(message.content)
			await message.channel.send("!catch")

		if message.author.id == config["main_account_id"]:
			if message.content == "!bot":
				if running:
					running = False
				else:
					await message.channel.send("!catch")
			elif message.content == "!ping":
				await message.channel.send("!ping")
			elif message.content.startswith("!do "):
				await message.channel.send(message.content[4:])

		await bot.process_commands(message)

@bot.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(bot.latency * 1000 / 1000)}ms')

@bot.command()
async def spam(ctx, amount=20, *, message="E"):
	for i in range(amount):
		await ctx.channel.send(message)
		time.sleep(delay)

@bot.command()
async def catch(ctx, *, message="E"):
	global running
	running = not(running)
	while running:
		time.sleep(delay)
		await ctx.channel.send(message)

#keep_alive()
bot.run(token["T"])