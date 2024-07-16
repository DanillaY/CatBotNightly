from datetime import datetime
import os

import discord
import yt_dlp
from cogs.a_discord_client import *
from cogs.b_youtube_client import *
from cogs.c_audio_client import *
from database.radio import Radio
from discord.ext import commands

from database.radio_jsr import Radio_JSR
from database.sqlite import does_radio_db_exist, get_radio_db_info, get_radios_by_country, get_random_radio, get_random_radio_jsr
from logger import print_message, print_message_async

'''
    Use this cog to only interact with radio related class,
    dont edit the name of the class,
    dont move any files from cogs folder 
    dont use radio client if youtube client or discord client is not working
'''

ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

class Radio_Client(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.discord_cog: discord.Cog = bot.get_cog('Discord_Client')
        self.youtube_cog: discord.Cog = bot.get_cog('Youtube_Client')
        self.audio_cog: discord.Cog = bot.get_cog('Audio_Client')
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 15','options': '-vn -filter:a "volume=0.5"'}
        
        if self.discord_cog == None or self.youtube_cog == None:
            print_message(message='Could not get discord or youtube cog', error='error', came_from='Radio_Client')
    
    #shows first few records of radios in database (because of the 2000 chars limit per message)
    @commands.command()
    async def radio_available_dump(self,ctx) -> None:
        message = join_radio_info(get_radio_db_info())
        await ctx.send('```'+message+'```')
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message_async(message='Radio cog started working', came_from='Radio_Client')
    
    @commands.command()
    async def radio(self,ctx, radio_id) -> None:
        if ctx.author.voice != None and len(self.youtube_cog.youtube_queue) == 0 and self.discord_cog.radio_playing == False:
            await play_radio(self,ctx,f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3','radio')
        elif does_radio_db_exist(radio_id) == False:
            await ctx.channel.send('Radio with that id does not exist')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @commands.command()
    async def jsr(self,ctx):
        try:
            if ctx.author.voice != None and self.discord_cog.yt_playing == False and self.discord_cog.radio_playing == False or self.discord_cog.voice_client == None:            
                radio:Radio_JSR = get_random_radio_jsr()
                self.discord_cog.radio_jsr_playing = True

                await play_radio(self,ctx,radio.song_link,'radio_jsr')
                await ctx.channel.send(f'Right now playing JetSetRadio.live! Song: {radio.song_name}, station: {radio.station}, from the game {radio.game_title}')
            else:
                await ctx.channel.send('You are not in the voice channel or the bot is playing youtube videos, use !stop')

        except BaseException as e:
            await print_message_async(message='Could not stream music from jsr.live',error=str(e), came_from='Radio_Client')

    @commands.command()
    async def radio_search_by_country(self,ctx) -> None:
        try:
            country:str = ctx.message.content.split('radio_search_by_country')[1].strip()
            radios = get_radios_by_country(country)
            if len(radios) == 0:
                await ctx.send('Nothing was found in that country')
            else:
                await print_message_async(message='Bot is searching radios by country',came_from='Radio_Client')
                message = join_radio_info(get_radios_by_country(country))
                await ctx.send('```'+message+'```')
        except BaseException as e:
            await print_message_async(message='Error while getting coutries from database',error= str(e),came_from='Radio_Client')
    
    async def close(self):
        await self.async_cleanup()
        await super().close()
    
    @commands.command()
    async def radio_random(self,ctx) -> None:
        try:
            if ctx.author.voice != None and self.discord_cog.yt_playing == False and self.discord_cog.voice_client == None:
                radio:Radio = get_random_radio()
                await play_radio(self,ctx,f'http://radio.garden/api/ara/content/listen/{radio.id}/channel.mp3','radio')
                await ctx.channel.send(f'Right now playing {radio.title}, country {radio.country}, id {radio.id}')

            elif self.discord_cog.radio_playing == True:
                await ctx.channel.send('Bot is streaming a radiostation, use !stop and !yt to play yt links')

            elif self.discord_cog.yt_playing == True:
                await ctx.channel.send('Bot is playing a youtube queue, use !stop and !radio_random or !radio to play radiostations')
                
            else:
                await ctx.channel.send('You are not in the voice channel or the bot playing radiostation, use !stop to play yt links')
        except BaseException as e:
            await print_message_async(message='Error while starting new radio', error=str(e),came_from='Radio_Client')
    
    async def set_radio_playing_status(self,ctx,status:bool,field_specified:str) -> None:
        if self.discord_cog != None and field_specified == 'radio':
            self.discord_cog.radio_playing = status

        elif self.discord_cog != None and field_specified == 'radio_jsr':
            self.discord_cog.radio_jsr_playing = status
            if status == False:
                asyncio.run_coroutine_threadsafe(self.jsr(ctx),self.bot.loop)
        else:
            await print_message_async(message='Cant set the radio playing status',error='discord cog is empty',came_from='Radio_Client')

async def play_radio(self:Radio_Client,ctx,link:str, calling_from:str) -> None:
    if link == '' or link == None:
        await print_message_async(message='The link is empty',came_from='Radio_Client')
    try:
        channel: discord.VoiceChannel = ctx.author.voice.channel
        connection: discord.VoiceClient = await connect_bot_to_channel_if_not_other_cog(self,channel)

        if connection.is_playing() == False and self.discord_cog.yt_playing == False:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(link, download=False)
                URL = info['formats'][0]['url']

                audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source=URL, **self.FFMPEG_OPTIONS)
                connection.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(self.set_radio_playing_status(ctx,False,calling_from), self.bot.loop))

                await print_message_async(message='Started playing radio',came_from='Radio_Client')
                await self.set_radio_playing_status(ctx,True,calling_from)
    except BaseException as e:
        await print_message_async(message='Could not stream that radio', error=str(e),came_from='Radio_Client')
        await ctx.send('Could not stream that radio. Sorry :(')
        self.audio_cog.stop()

def join_radio_info(radios:list[Radio]) -> str:
    message=''
    for radio in radios:
        if len(message)+150 < 2000:
            message += radio.id + ' | ' + radio.title + ' | ' + radio.country + '\n'
    return message

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Radio_Client(client))