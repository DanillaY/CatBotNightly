import os
import discord
from discord.ext import commands

from cogs.a_discord_client import *
from cogs.b_youtube_client import *
from logger import print_message_async, print_message

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
        self.youtube_cog = bot.get_cog('Youtube_Client')
        
        if self.discord_cog == None or self.youtube_cog == None :
            print_message(message='Could not get discord or youtube cog)',error='error',came_from='Audio_Client')

    @commands.command()
    async def stop(self,ctx) -> None:
        try:
            connection: discord.VoiceClient = self.discord_cog.voice_client
            
            if ctx.author.voice != None and connection != None:
                self.discord_cog.radio_jsr_playing = False
                self.discord_cog.yt_playing = False
                self.discord_cog.radio_playing = False
                self.youtube_cog.youtube_queue.clear()
                await connection.disconnect(force=True)
                await print_message_async(message='Bot is stopped',came_from='Audio_Client')
                self.discord_cog.voice_channel = None
                self.discord_cog.voice_client = None
            else:
                await ctx.channel.send('Could not get voice channel connection')
        except BaseException as e:
            await print_message_async(message='Error while stoping the audio',error=str(e),came_from='Audio_Client')
        

    @commands.command()
    async def pause(self,ctx) -> None:
        connection: discord.VoiceClient = self.discord_cog.voice_client
        if ctx.author.voice != None and connection.is_playing() and connection != None:
           connection.pause()
           await print_message_async(message='Bot is paused',came_from='Audio_Client')
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