import discord
import json
import os
from dotenv import load_dotenv
import urllib.request

from sqlite import sqlite_init
from twitch_client import Twitch_Client

load_dotenv()
client = Twitch_Client(intents=discord.Intents.all())
secret = os.getenv('BOT_SECRET')
ban_words = os.getenv('BANNED_WORDS').split(',')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!cat_pic'):
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        await message.channel.send(file = discord.File('cats/cat.jpg'))
        await message.add_reaction('🐱')

    if message.content.startswith('!fact'):
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await message.channel.send(json_object['fact'])

    for word in ban_words:
        if word in message.content:
            await message.delete()
            
client.run(secret)