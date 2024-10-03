import discord
import requests
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, molebot):
        self.molebot = molebot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Molebot !Commands is online.....")

    @commands.command()
    async def hello(self, ctx):
        print("!hello is supposed to run")
        await ctx.send("Mom, Dad, I missed you")

    @commands.command()
    async def doh(self, ctx):
        print("!doh is supposed to run")
        await ctx.send("b'oh")

    @commands.command()
    async def sfw(self, ctx):
        sfwlink = 'https://cdn.discordapp.com/attachments/1285702416096039005/1285702797622378571/dugj2lh6f6051.png?ex=66eb3b8a&is=66e9ea0a&hm=18e720217950d34ad1382990f4dc8f4940a694888c244a452f210812a540b732&'
        print("!sfw is supposed to run")
        await ctx.send(sfwlink)

    @commands.command()
    async def test(self, ctx):
        giflink = 'https://tenor.com/view/football-gif-22736897'
        print("!test is supposed to run")
        await ctx.send(f"Man getting hit by football\n {giflink}")

    @commands.command()
    async def dadjoke(self, ctx):
        url = "https://icanhazdadjoke.com/"
        myheaders = {"Accept": "application/json"}
        response = requests.get(url, headers=myheaders)
        print("!dadjoke is supposed to run")

        if not response.ok:
            print(response)
            LOG.error(f"There was an error: {response.reason}")

        joke = response.json().get("joke")
        await ctx.send(joke)

async def setup(molebot):
        await molebot.add_cog(Commands(molebot))