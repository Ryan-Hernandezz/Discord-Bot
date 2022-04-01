import datetime
import discord
import random
import os
from discord.ext import commands
from django.test import Client
from dotenv import load_dotenv
from matplotlib.pyplot import title
from urllib import parse, request
from googlesearch import search
import re

#loads token key from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='$')

#ping command
@bot.command(name = "ping")
async def ping(ctx):
    await ctx.send('pong')

#sum of numbers
@bot.command(name="sum")
async def add(ctx, numOne: int, numTwo: int):
    await ctx.channel.send(numOne + numTwo)

#product of numbers
@bot.command(name="product")
async def multiply(ctx, numOne: int, numTwo: int):
    await ctx.channel.send(numOne * numTwo)

#square function
@bot.command()
async def sq(ctx, arg):
    await ctx.send(int(arg) ** 2)

#square root function
@bot.command()
async def sqrt(ctx, arg):
    await ctx.send(int(arg) ** (1/2))

#random number
@bot.command()
async def rand(ctx):
    await ctx.send(random.randrange(1, 20, 1))

#guild info
@bot.command()
async def info(ctx):
    embed = discord.Embed(title = f"{ctx.guild.name}", description = "idk", timestamp = datetime.datetime.utcnow(), color = discord.Color.blue())
    embed.add_field(name = "Server Creation: ", value = f"{ctx.guild.created_at}")
    embed.add_field(name = "Server Owner: ", value = f"{ctx.guild.owner}")
    embed.add_field(name = "Server Region: ", value = f"{ctx.guild.region}")
    embed.add_field(name = "Server ID: ", value = f"{ctx.guild.id}")
    await ctx.send(embed = embed)


@bot.command(name = "youtube")
async def yt(ctx, *, search):
    queryString = parse.urlencode({'search_query': search})
    htmlContent = request.urlopen('http://www.youtube.com/results?' + queryString)
    results = re.findall(r"watch\?v=(\S{11})", htmlContent.read().decode())
    await ctx.send('https://www.youtube.com/watch?v=' + results[0])


@bot.event
async def new_member(member):
    x = member.server.default_channel
    await bot.send_message(x, '{} is in this hoe!'.format(member.name))

@bot.event
async def on_ready():
    guild_count = 0
    #loops through all guilds and increments counter
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    print("Alfred is in " + str(guild_count) + " guilds.")
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members: \n - {members}')


@bot.event
#responds to hello messages in discord 
async def on_message(message):
    #make sure bot doesn't respond to itself
    if message.author == bot.user:
        return

    if message.content == "alfred":
        await message.channel.send(f'What {message.author}!')

    if message.content.startswith('google'):
        search_content = ""
        text = str(message.content).split(' ')
        for i in range(2, len(text)):
            search_content = search_content + text[i]
        for j in search(search_content, tld = "co.in", num = 1, stop = 3, pause = 2):
            await message.channel.send(j)

bot.run(DISCORD_TOKEN)
