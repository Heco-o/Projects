import sys
sys.path.insert(0, 'discord.py-self')
sys.path.insert(0, 'discord.py-self_embed')

import re
import pytesseract
from PIL import Image
import requests
import discord
from discord.ext import commands
import discord_self_embed
import json

with open('config.json', 'r') as file:
	config = json.load(file)

token = config['token']
prefix = config['prefix']

bot = commands.Bot(command_prefix=prefix, self_bot=False)
running = False
text = []

@bot.event
async def on_message(message):
	user = str(message.author)
	if len(message.embeds) > 0 and user == "Poké-Name#2116" and message.embeds[0].image.url != None:
		global running, text
		running = False
		image = Image.open(requests.get(message.embeds[0].image.url, stream=True).raw)
		text = pytesseract.image_to_string(image)
		print(text)
		text = re.sub(r'[^a-zA-Z ]', '', text).split(" ")
		print(text)
		await message.channel.send(f"<@716390085896962058> catch {text[0]}")
	elif user == "Poké-Name#2116" and message.content == "That is the wrong pokémon!" and len(text) > 1:
		await message.channel.send(f"<@716390085896962058> catch {text[0]} {text[1]}")
	
	if message.content == "Heco!" and user == "heco.#0":
		await message.channel.send("Hi everyone my name is Heco and i was made by heco.#0 hehe")
	
	if message.content == "Heco?" and user == "heco.#0":
		await message.channel.send("Nah")
	
	if message.content == "Start" and user == "heco.#0":
		for i in range(40): await message.channel.send("E")
	
	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(bot.latency * 1000 / 1000)}ms')

@bot.command()
async def spam(ctx, amount=20, *, message="E"):
	if str(ctx.author) == "heco.#0":
		for i in range(amount): await ctx.channel.send(message)

@bot.command()
async def start(ctx, *, message="E"):
	if str(ctx.author) == "heco.#0":
		global running
		running = not(running)
		while running:
			await ctx.channel.send(message)

bot.run(token)