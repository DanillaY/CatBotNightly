import asyncio
import os

import discord
import yt_dlp
from discord.ext import commands

from cogs import a_discord_client
from cogs.a_discord_client import *
from cogs.c_audio_client import *
from logger import print_message_async, print_message

'''
    Use this cog to only interact with youtube related class,
    dont edit the name of the class,
    dont move any files from cogs folder,
    dont use youtube client if discord client is not working
'''

ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

class Youtube_Client(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.discord_cog = bot.get_cog('Discord_Client')
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 15','options': '-vn -filter:a "volume=0.5"'}
        
        if self.discord_cog == None:
            print_message(message='Could not get discord', error='error', came_from='Youtube_Client')

    @commands.command()
    async def skip_yt(self,ctx):
        if ctx.author.voice != None and self.discord_cog.yt_playing == True and self.discord_cog.voice_client.is_playing():
            self.discord_cog.voice_client.stop()
            self.discord_cog.yt_playing = False
            await self.yt(self.discord_cog.youtube_queue[0])
        else:
            await ctx.channel.send('Could not skip the song')

    @commands.command()
    async def queue(self,ctx):
        video_counter = len(self.discord_cog.youtube_queue)
        if video_counter == 1:
            await ctx.send(f'Right now {video_counter} video is in the queue')
        elif video_counter > 0:
            await ctx.send(f'Right now {video_counter} videos are in the queue')
        else:
            await ctx.send(f'Thers no videos in the queue')

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message_async(message='Youtube cog started working',came_from='Youtube_Client')

    async def play_next_yt(self, ctx):
        if len(self.discord_cog.youtube_queue) > 0:
            try:
                link = self.discord_cog.youtube_queue[0]
                await self.yt(ctx, link)
                self.discord_cog.youtube_queue.pop(0)
            except BaseException as e:
                await print_message_async(message='Could not play next song',error=str(e), came_from='Youtube_Client')
        else:
            await ctx.channel.send('Youtube queue has ended')
            #since the bot could be stopped at any time need to check the connection to not raise stop method twice 
            if self.discord_cog.voice_client != None and self.discord_cog.voice_channel != None:
                await self.bot.get_cog('Audio_Client').stop(ctx)

    async def add_to_yt_queue(self,ctx,link):
        await print_message_async(message='Added new song to the queue',came_from='Youtube_Client')
        self.discord_cog.youtube_queue.append(link)
    
    @commands.command()
    async def yt(self,ctx,link) -> None:

        if ctx.author.voice == None:
            await ctx.channel.send('You should be in the voice channel to use that command')
            return
        
        if link == None or link == '':
            await print_message_async(message='The link is empty',came_from='Youtube_Client')
            return
        
        if self.discord_cog.radio_playing == True or self.discord_cog.radio_jsr_playing == True:
            await ctx.channel.send('Cant play youtube video while radio is playing, please use !stop to stop streaming radio and try again')
            return

        try:
            channel: discord.VoiceChannel = ctx.author.voice.channel if self.discord_cog.voice_channel == None else self.discord_cog.voice_channel
            connection: discord.VoiceClient = await a_discord_client.connect_bot_to_channel_if_not_other_cog(self,channel)

            if self.discord_cog.voice_client.is_playing():
                await self.add_to_yt_queue(ctx,link)
                await ctx.channel.send('Song was added the queue')

            elif connection.is_connected():
                with yt_dlp.YoutubeDL({'options': '-vn'}) as ydl:
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
                    URL = info['requested_formats'][1]['url']

                    audio = discord.FFmpegPCMAudio(source=URL, **self.FFMPEG_OPTIONS)
                    play_next = lambda e: asyncio.run_coroutine_threadsafe(self.play_next_yt(ctx), self.bot.loop)
                    self.discord_cog.yt_playing = True
                    
                connection.play(source=audio, after=play_next)
   
        except BaseException as e:
            await print_message_async(message='Could not play yt video', error=str(e),came_from='Youtube_Client')
            await ctx.channel.send('Youtube queue has ended')

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Youtube_Client(client))