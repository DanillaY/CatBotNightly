import os
import discord
from discord.ext import commands

from cogs.a_discord_client import *
from logger import print_message, print_message_async

'''
    Use this cog to only interact with audio related class,
    dont edit the name of the class,
    dont move any files from cogs folder
'''

ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

class Audio_Client(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.discord_cog = bot.get_cog('Discord_Client')
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.5"'}

    @commands.command()
    async def stop(self,ctx) -> None:
        channel: discord.VoiceChannel = ctx.author.voice.channel if self.discord_cog.voice_channel == None else self.discord_cog.voice_channel
        connection: discord.VoiceClient = await connect_bot_to_channel_if_not_other_cog(self,channel)
        
        if ctx.author.voice != None and connection != None:
           await connection.disconnect(force=True)
           await print_message_async('Bot is stopped')
           self.discord_cog.voice_channel = None
           self.discord_cog.voice_client = None
           self.youtube_queue.clear()
        else:
            await ctx.channel.send('This song is unstoppable')

    @commands.command()
    async def pause(self,ctx) -> None:
        connection: discord.VoiceClient = self.discord_cog.voice_client
        if ctx.author.voice != None and connection.is_playing() and connection != None:
           connection.pause()
           await print_message_async('Bot is paused')
        else:
            await ctx.channel.send('Cant pause current song')

    @commands.command()
    async def resume(self,ctx) -> None:
        connection: discord.VoiceClient = self.discord_cog.voice_client
        if ctx.author.voice != None and connection.is_paused() and connection != None:
           connection.resume()
        else:
            await ctx.channel.send('Cant resume current song')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Audio_Client(client))