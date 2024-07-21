import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from cogs import a_discord_client
from cogs import b_speedrun_client
from cogs import b_youtube_client
from cogs import c_audio_client
from cogs import c_radio_client
from database.sqlite import speedrun_sqlite_init

load_dotenv()
secret = os.getenv('BOT_SECRET')
ban_words = os.getenv('BANNED_WORDS').split(',')

async def on_message(message):
    for word in ban_words:
        if word in message.content:
            await message.delete()

async def main():
    client = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all())
    
    await client.add_cog(a_discord_client.Discord_Client(client))
    await client.add_cog(b_speedrun_client.Speedrun_Client(client))
    await client.add_cog(b_youtube_client.Youtube_Client(client))
    await client.add_cog(c_audio_client.Audio_Client(client))
    await client.add_cog(c_radio_client.Radio_Client(client))
    
    client.add_listener(on_message,'on_message')
    await client.start(secret)

asyncio.run(main())

#asyncio.run(radio_sqlite_init()) update radio database every week