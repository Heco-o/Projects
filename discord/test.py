import discord
import os
import sympy
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ".", intents=discord.Intents.default())

@client.event
async def on_ready():
	print("Done as {0.user}".format(client))

@client.event
async def on_message(message):
	user = str(message.author)
	if message.content == "Heco!" and user == "heco.#0":
		await message.channel.send("Hi everyone my name is Heco and i was made by heco.#0 hehe")
	
	if message.content == "Heco?" and user == "heco.#0":
		await message.channel.send("Nah")
	
	if message.content == "Start" and user == "heco.#0":
		for i in range(40): await message.channel.send("E")
	
	await client.process_commands(message)

@client.command()
async def spam(ctx, amount=20, *, message="E"):
	if str(ctx.author) == "heco.#0":
		for i in range(amount): await ctx.channel.send(message)

@client.command()
async def math(ctx, t, *, prob):
	ans = None
	prob = "".join(prob.split())
	
	if t.lower() == "f" or t.lower() == "factor":
		ans = str(sympy.factor(prob)).replace("**", "^").replace("*", " * ")
	
	elif t.lower() == "e" or t.lower() == "expand":
		ans = str(sympy.expand(prob)).replace("**", "^").replace("*", " * ")
	
	elif t.lower() == "s" or t.lower() == "sympify":
		ans = str(sympy.sympify(prob, rational = True)).replace("**", "^").replace("*", " * ")
	
	if ans != None and len(ans) <= 2000:
		await ctx.channel.send(ans)

@client.command()
async def solve(ctx, *, x):
	if "=" in x:
		await ctx.channel.send(str(sympy.solve(x.replace("**", "^").replace(" ", "").replace("=", "-(") + ")")).replace("**", "^").replace("*", " * "))
	else:
		await ctx.channel.send(str(sympy.solve(x)).replace("**", "^").replace("*", " * "))

@client.command()
async def clear(ctx, amount=5):
	if str(ctx.author) == "heco.#0" or str(ctx.author) == "lane6775#0":
		await ctx.channel.purge(limit=amount)

@client.command()
async def dm(ctx, user: discord.User, *, message="Hi!"):
	embed = discord.Embed(title=f"Sent by {ctx.author}", description=message, color=0x000000)
	await user.send(embed=embed)
	await ctx.channel.send("Message sent!")

keep_alive()
client.run(os.environ['T'])