import asyncio
import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv
import urllib.request

import requests

from cogs.discord_client import Discord_Client

load_dotenv()
secret = os.getenv('BOT_SECRET')
ban_words = os.getenv('BANNED_WORDS').split(',')
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('!test'):
        if message.author.voice != None:
            channel: discord.VoiceChannel = message.author.voice.channel
            connection: discord.VoiceClient = await channel.connect()
            #await urllib.request.urlretrieve('http://radio.garden/api/ara/content/listen/vbFsCngB/channel.mp3','radio.mp3')

            audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source='radio.mp3')
            connection.play(audio, after=lambda e: connection.disconnect()) 
        else:
            await message.channel.send('You should be in the voice channel to use that command')
    
    for word in ban_words:
        if word in message.content:
            message.delete()
'''
async def cog_load(client : commands.Bot):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
    await cog_load(client)
    await client.start(secret)

asyncio.run(main())
#curl -L -v http://radio.garden/api/ara/content/listen/vbFsCngB/channel.mp3 -A "Mozilla/5.0 (compatible;  MSIE 7.01; Windows NT 5.0)" --output mis.mp3