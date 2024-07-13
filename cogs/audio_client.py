
import os
import discord
from discord.ext import commands

from logger import print_message

ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

#TO DO fix calling commands
class Audio_Client(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.discord_cog = bot.get_cog('Discord_Client')
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.5"'}

#TODO stop method doesnt work with radio player
    @commands.command()
    async def stop(self,ctx) -> None:
        print(self.discord_cog.voice_client, ctx.author.voice)
        connection: discord.VoiceClient = self.discord_cog.voice_client
        if ctx.author.voice != None and connection != None:
           await connection.disconnect(force=True)
           await print_message('Bot is stopped')
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
           await print_message('Bot is paused')
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