import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs import *
from database.sqlite import database_sqlite_init_speedrun

load_dotenv()
secret = os.getenv('BOT_SECRET')
ban_words = os.getenv('BANNED_WORDS').split(',')

async def on_message(message):
    for word in ban_words:
        if word in message.content:
            await message.delete()

async def cog_load(client : commands.Bot):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
    await cog_load(client)
    client.add_listener(on_message,'on_message')
    await client.start(secret)

asyncio.run(main())

#asyncio.run(radio_sqlite_init()) update radio database every week