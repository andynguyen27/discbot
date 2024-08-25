import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import requests


load_dotenv(override=True)

MOLEBOTTOKEN = os.getenv('MOLEBOTTOKEN')
DADJOKEAPI = os.getenv('DADJOKEAPI')

intents = discord.Intents.all()
molebot = commands.Bot(command_prefix = '!',intents=intents)


@molebot.event 
async def on_ready():
    print("bot is ready") 
    print("-----------------------------")


@molebot.command()
async def hello(ctx):
    await ctx.send("Mom, Dad, I missed you")

@molebot.command()
async def on_member_join(member):
    channel = molebot.get_channel(1275719939587706954)
    await channel.sent("Welcome")

@molebot.command()
async def on_member_remove(member):
    channel = molebot.get_channel(1275719939587706954)
    await channel.send("Goodbye")


@molebot.command()
async def dadjoke(ctx):
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    joke = response.json().get("joke")
    channel = molebot.get_channel(1275719939587706954)
    await channel.send(joke)



molebot.run(MOLEBOTTOKEN)

if __name__ == "__main__":
    main()