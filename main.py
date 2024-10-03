import discord
import os
import re
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import requests
from temp import tempconvert
import logging
import hashlib
import aiohttp
import json
import asyncio
from cogs.commands import Commands
from cogs.slashcommands import SlashCommands

load_dotenv(override=True)

MOLEBOTTOKEN = os.getenv('MOLEBOTTOKEN')
DADJOKEAPI = os.getenv('DADJOKEAPIKEY')
VIRUSTOTALAPI = os.getenv('VIRUSTOTALAPIKEY')
CHANNEL_ID = os.getenv('DISCCHANNELID')
SERVER_ID = os.getenv('DISCSERVERID')
LOG = logging.getLogger(__name__)

intents = discord.Intents.all()
molebot = commands.Bot(command_prefix = '!',intents=intents)
delete_message = False # configure this 


# def load():
#     for filename in os.listdir('./cogs'):
#         if filename.endswith('.py'):
#             try:
#                 # await molebot.add_cog(Commands(molebot))
#                 molebot.load_extension(f'cogs.{filename[:-3]}')
#                 print(f"Loading: {filename}")
#             except Exception as e:
#                 print(f"Failed to load extension {filename}: {e}")

@molebot.event 
async def on_ready():
    # await molebot.tree.sync(guild=discord.Object(id=SERVER_ID))
    try:
        synced_commands = await molebot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occurred: ", e)
    print("bot is ready") 
    print("-----------------------------")


# @molebot.command()
# async def hello(ctx):
#     await ctx.send("Mom, Dad, I missed you")


@molebot.event
async def on_member_join(member):
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send("Welcome")


@molebot.event
async def on_member_remove(member):
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send("Goodbye")


@molebot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to run this command")


# @molebot.command()
# async def sfw(ctx):
#     sfwlink = 'https://cdn.discordapp.com/attachments/1285702416096039005/1285702797622378571/dugj2lh6f6051.png?ex=66eb3b8a&is=66e9ea0a&hm=18e720217950d34ad1382990f4dc8f4940a694888c244a452f210812a540b732&'
#     await ctx.send(sfwlink)


# @molebot.command()
# async def dadjoke(ctx):
#     url = "https://icanhazdadjoke.com/"
#     myheaders = {"Accept": "application/json"}
#     response = requests.get(url, headers=myheaders)

#     if not response.ok:
#         print(response)
#         LOG.error(f"There was an error: {response.reason}")

#     joke = response.json().get("joke")
#     await ctx.send(joke)


# @molebot.tree.command(name="tempconv", description="temperature conversion", guild=discord.Object(id=SERVER_ID))
# @app_commands.describe(unit="Select C for Celsius or F for Fahrenheit", temperature="Temperature to convert")
# @app_commands.choices(unit=[
#     app_commands.Choice(name="C", value="C"),
#     app_commands.Choice(name="F", value="F"),
# ])
# async def tempconv(interaction: discord.Interaction, unit: app_commands.Choice[str], temperature: int):
#     result = tempconvert(unit.value, temperature)
#     await interaction.response.send_message(f"Converted temperature: {result}", ephemeral=True)
# @app_commands.describe()

# tempconv.autocomplete = @app_commands.Choice(
#     name="scale",
#     choices=[
#         app_commands.Choice(name="Celsius", value="C"),
#         app_commands.Choice(name="Fahrenheit", value="F")
#     ]
# )


# @molebot.command()
# async def test(ctx):
#     giflink = 'https://tenor.com/view/football-gif-22736897'
#     await ctx.send(f"Man getting hit by football\n {giflink}")


async def download_file(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_name, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    return file
# async def check_virus_link(message_link):
    
#     url = "https://www.virustotal.com/api/v3/urls"

#     payload = { "url": message_link }
#     headers = {
#         "accept": "application/json",
#         "content-type": "application/x-www-form-urlencoded",
#         "x-apikey": VIRUSTOTALAPI
#     }

#     response = requests.post(url, data=payload, headers=headers)
#     response.data.links.self
#     return response.text    
# @molebot.event 
# async def on_message(message):
#     if message.author == molebot.user:
#         return #ignore messages from the bot itself
    
#     url_pattern = r'(https?://\S+)'
#     match = re.search(url_pattern, message.content)
#     print(match)

#     if match:
#         link = match.group(1)
#         result = await check_virus_link(link)
#         await message.channel.send(result)
#     else:   
#         await molebot.process_commands(message)

async def check_virus_link(message_link):
    url = "https://www.virustotal.com/api/v3/urls"

    payload = { "url": message_link }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "x-apikey": VIRUSTOTALAPI
    }

    response = requests.post(url, data=payload, headers=headers)

    if response:
        bot_message = "The royal link is clean, your highness"
        response_json = response.json()
        response_2 = requests.get(url=response_json['data']['links']['self'], headers=headers)
        stats = response_json.get('data', {}).get('attributes', {}).get('stats', {})
        # Load the JSON response from the result variable
        response = json.loads(response_2.text)

        # Extract the stats
        stats = response['data']['attributes']['stats']
        # Return the stats in the form of a dictionary
        stats_dict = {
            "malicious": stats['malicious'],
            "suspicious": stats['suspicious'],
            "undetected": stats['undetected'],
            "harmless": stats['harmless'],
            "timeout": stats['timeout']
        }

        if int(stats_dict["malicious"])>0 or int(stats_dict["suspicious"]>0):
            print("i'm ugly")
            bot_message = (f"Potentially malicious link. Here are the results of your scan:\n"
               f"```Malicious: {stats['malicious']}\n"
               f"Suspicious: {stats['suspicious']}\n"
               f"Undetected: {stats['undetected']}\n"
               f"Harmless: {stats['harmless']}\n"
               f"Timeout: {stats['timeout']}```")
        return bot_message        
    else: 
        return 'balls'

    
async def check_virus(file):
    # with open(file_path, 'rb') as file:
    #     file_bytes = file.read()
    #     file_hash = hashlib.sha256(file_bytes).hexdigest()
    url = "https://www.virustotal.com/api/v3/files"
    print("Typeof File: ", type(file))
    payload = { "file" : file }
    # headers = {'apikey' : VIRUSTOTALAPI, 'resource': file_hash}
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "x-apikey": VIRUSTOTALAPI
    }
    print("peepee")
    response = requests.post(url, data=payload, headers=headers)
    print("Response.text: ",response.text)
    if response.status_code == 200:
        response_json = response.json()
        response_2 = requests.get(url=response_json['data']['links']['self'], headers=headers)
        stats = response_json.get('data', {}).get('attributes', {}).get('stats', {})
        # Load the JSON response from the result variable
        print("response_2.text:", response_2.text)
        print("stats: ", stats)
        response = json.loads(response_2.text)
        json_response = response.json()
        print("json_response.txt json_response.text")
        # if json_response['response_code'] == 1:
        #     positives = json_response['positives']
        #     total = json_response['total']
        #     return positives > 0, f"{positives}/{total} threat detected in this file."
        # return False, "Error occurred while scanning."


@molebot.event
async def on_message(message):
    # if message.author == molebot.user:
    #     return
    # print(f'it\'s like kissing a peanut - ${message}')
    # print(f"Message content: {message.content}")
    # print(f"Author: {message.author.name}#{message.author.discriminator}")
    # print(f"Channel: {message.channel.name}")
    # if message.content:
    #     result = await check_virus_link(message.content)
    #     print(result)
    #     return
    if message.author == molebot.user:
        return #ignore messages from the bot itself
    url_pattern = r'(https?://\S+)'
    match = re.search(url_pattern, message.content)

    if match:
        link = match.group(1)
        result = await check_virus_link(link)
        await message.channel.send(result)
    else:   
        await molebot.process_commands(message)

    # for attachment in message.attachments:
    #     if attachment.content_type.startswith('image/'):
    #         return
        
    if message.attachments is not None:
        for attachment in message.attachments:
            print('jollibee')
            file_name = attachment.filename
            file_url = attachment.url
            print(f'${file_name} ${file_url}')
            file = await download_file(file_url, file_name)
            is_infected, result = await check_virus(file)
            if is_infected:
                delete_message = True
                await message.channel.send(f"<@{message.author.id}> Virus scan detected. {result}")
            else:
                await message.channel.send(f"<@{message.author.id}> File is clean. {result}")
            os.remove(file_name)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await molebot.load_extension(f"cogs.{filename[:-3]}")
            print(f"loading {filename[:-3]}")


async def main():
    async with molebot:
        await load()
        await molebot.start(MOLEBOTTOKEN)
    # if delete_message:
    #     await message.delete()
asyncio.run(main())
# asyncio.run(main())
if __name__ == "__main__":
    main()
    # uvicorn.run(app, port=8000, host="0.0.0.0")