import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import requests
from temp import tempconvert
import logging
import hashlib
import aiohttp


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

@molebot.event 
async def on_ready():
    await molebot.tree.sync(guild=discord.Object(id=SERVER_ID))
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

@molebot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to run this command")




@molebot.command()
async def dadjoke(ctx):
    url = "https://icanhazdadjoke.com/"
    myheaders = {"Accept": "application/json"}
    response = requests.get(url, headers=myheaders)

    if not response.ok:
        LOG.error(f"There was an error: {response.reason}")

    joke = response.json().get("joke")
    channel = molebot.get_channel(CHANNEL_ID)
    await channel.send(joke)

@molebot.tree.command(name="tempconv", description="temperature conversion", guild=discord.Object(id=SERVER_ID))
async def tempconv(interaction: discord.Interaction, input:str):
    result = tempconvert(input)
    await interaction.response.send_message(result)

@molebot.command()
async def test(ctx):
    await ctx.send("Man getting hit by football")



async def download_file(url, file_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(file_name, 'wb') as file:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)

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
            
        print("First Response: ", response.text)
        response_json = response.json()
        response_2 = requests.get(url=response_json['data']['links']['self'], headers=headers)

        return response_2.text
    else: 
        return 'balls'

async def check_virus(file_path):
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

    params = {'apikey' : VIRUSTOTALAPI, 'resource': file_hash}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['response_code'] == 1:
            positives = json_response['positives']
            total = json_response['total']
            return positives > 0, f"{positives}/{total} threat detected in this file."
        return False, "Error occurred while scanning."


@molebot.event
async def on_message(message):
    # if message.author == molebot.user:
    #     return
    # print(f'it\'s like kissing a peanut - ${message}')
    # print(f"Message content: {message.content}")
    # print(f"Author: {message.author.name}#{message.author.discriminator}")
    # print(f"Channel: {message.channel.name}")
    if message.content:
        result = await check_virus_link(message.content)
        print(result)
        return

    for attachment in message.attachments:
        if attachment.content_type.startswith('image/'):
            return
        
    if message.attachments:
        print('let me out')
        for attachment in message.attachments:
            print('jollibee')
            file_name = attachment.filename
            file_url = attachment.url
            print(f'${file_name} ${file_url}')
            await download_file(file_url, file_name)
            is_infected, result = await check_virus(file_name)
            if is_infected:
                delete_message = True
                await message.channel.send(f"<@{message.author.id}> Virus scan detected. {result}")
            else:
                await message.channel.send(f"<@{message.author.id}> File is clean. {result}")
            os.remove(file_name)

    # if delete_message:
    #     await message.delete()

    await molebot.process_commands(message)

molebot.run(MOLEBOTTOKEN)

if __name__ == "__main__":
    main()