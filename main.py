import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
from temp import tempconvert

load_dotenv(override=True)

MOLEBOTTOKEN = os.getenv('MOLEBOTTOKEN')
DADJOKEAPI = os.getenv('DADJOKEAPI')
CHANNEL_ID = 1275719939587706954


intents = discord.Intents.all()
molebot = commands.Bot(command_prefix = '!',intents=intents)

@molebot.event 
async def on_ready():
    await molebot.tree.sync(guild=discord.Object(id=1192793808094638130))
    print("bot is ready") 
    print("-----------------------------")

@molebot.command()
async def hello(ctx):
    await ctx.send("Mom, Dad, I missed you")

@molebot.event
async def on_member_join(member):
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send("Welcome")

@molebot.event
async def on_member_remove(member):
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send("Goodbye")


@molebot.command()
async def dadjoke(ctx):
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    joke = response.json().get("joke")
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send(joke)

@molebot.tree.command(name="tempconv", description="temperature conversion", guild=discord.Object(id=1192793808094638130))
async def tempconv(interaction: discord.Interaction, input:str):
    result = tempconvert(input)
    await interaction.response.send_message(result)

@molebot.command()
async def test(ctx):
    await ctx.send("Man getting hit by football")

molebot.run(MOLEBOTTOKEN)

if __name__ == "__main__":
    main()