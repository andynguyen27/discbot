import discord
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from discord.ext import commands
from temp import tempconvert
from epoch import eptime


SERVER_ID = os.getenv('DISCSERVERID')

class SlashCommands(commands.Cog):
    def __init__(self, molebot):
        self.molebot = molebot
    
    @commands.Cog.listener()
    async def on_ready(self):
         print("Molebot SlashCommands is online")

    @app_commands.command(name="timeconv", description="time converter")
    @app_commands.describe(hour="hours", minute="minutes")
    @app_commands.choices(
        hour=[app_commands.Choice(name=str(h), value=h) for h in range(1,13)],
        am_pm=[app_commands.Choice(name="AM", value="AM"),
               app_commands.Choice(name="PM", value="PM")])
    async def timeconv(self, interaction: discord.Interaction, hour: int, minute: int, am_pm: str):
        epoch_time = eptime(hour, minute, am_pm)
        await interaction.response.send_message(f"{epoch_time} \nchange x to: \nt for short time e.g. X:XX _M\nT for X:XX:XX _M\n ", ephemeral=True)
        print("eptime is supposed to run")
        # try:
        #       epoch_time = self.eptime(hour, minute, am_pm)
        #       await interaction.response.send_message(f"Epoch time: {epoch_time}", ephemeral=True)
        # except ValueError as e:
        #     await interaction.response.send_message(f"Error: {e}")

    @app_commands.command(name="tempconv", description="temperature conversion")
    @app_commands.describe(unit="Select C for Celsius or F for Fahrenheit", temperature="Temperature to convert")
    @app_commands.choices(unit=[
        app_commands.Choice(name="C", value="C"),
        app_commands.Choice(name="F", value="F"),
    ])
    async def tempconv(self, interaction: discord.Interaction, unit: app_commands.Choice[str], temperature: int):
        result = tempconvert(unit.value, temperature)
        print("tempconv is supposed to run")
        await interaction.response.send_message(f"Converted temperature: {result}", ephemeral=True)

async def setup(molebot):
        await molebot.add_cog(SlashCommands(molebot))