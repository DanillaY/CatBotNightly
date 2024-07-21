import asyncio
from datetime import datetime
import os
import random

import discord
import yt_dlp
from cogs import a_discord_client
from database.models.radio import Radio
from discord.ext import commands

from database.models.radio_jsr import Radio_JSR
from database.sqlite import find_jet_set_radio_station, find_radio_by_id, get_radio_db_info, get_radios_by_country, get_radios_jsr_by_station, get_random_radio, get_random_radio_jsr, get_stations_jsr
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
        #list of radio transitions before the song, dont store that in the database
        self.bumps:tuple[str] = ('https://jetsetradio.live/radio/stations/bumps/bump2.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/bump3.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/DJK1.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/DJK2.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/Donkey%20Kong%20Bumper.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/Jet%20Set%20Radio%20Bumper%202.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/Sega%20Tape%20Bumper.mp3',
                                 'https://jetsetradio.live/radio/stations/bumps/bump10.mp3' )
        
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
        
        if ctx.author.voice != None and self.discord_cog.yt_playing == False and self.discord_cog.radio_playing == False and self.discord_cog.radio_jsr_playing == False and find_radio_by_id(radio_id) == True:
            await play_radio(self,ctx,f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3','radio')
        
        elif find_radio_by_id(radio_id) == False:
            await ctx.channel.send('Radio with that id does not exist')
            return
        
        elif self.discord_cog.radio_playing != False:
            await ctx.channel.send('Another radiostation is already playing, please use !stop')
            return
       
        elif self.discord_cog.radio_jsr_playing != False:
            await ctx.channel.send('JSR station is already playing, please use !stop')
            return
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')
            return

    @commands.command()
    async def jsr(self,ctx, station:str = '') -> None:
        try:
            does_station_exist = find_jet_set_radio_station(station)

            if station != '' and does_station_exist:
                await send_station_logo(ctx,station)
                radio:Radio_JSR = random.choice(get_radios_jsr_by_station(station))

            elif station != '' and does_station_exist == False:
                await ctx.send('This radiostation doesnt exist')
                return
            
            else: 
                radio:Radio_JSR = get_random_radio_jsr()
            
            if ctx.author.voice != None and self.discord_cog.radio_jsr_playing == False and self.discord_cog.yt_playing == False and self.discord_cog.radio_playing == False and self.discord_cog.is_audio_stopping == False:    
                await play_filler_or_music(self,ctx,radio,station)
                await print_message_async(message=f'Playing jsr station',came_from='Radio_Client')
            else:
                await ctx.channel.send('You are not in the voice channel or the bot is already playing something, use !stop')

        except BaseException as e:
            await print_message_async(message='Could not stream music from jsr.live',error=str(e), came_from='Radio_Client')
    
    @commands.command()
    async def jsr_stations(self,ctx):
        tup_stations: tuple[str] = get_stations_jsr()
        message = ''
        for station in tup_stations:
            message += station[0] + ', '
        await ctx.send('```'+message[:-2]+'```')

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
                await ctx.channel.send('Bot is streaming a radiostation, use !stop and !yt to play youtube links')

            elif self.discord_cog.yt_playing == True:
                await ctx.channel.send('Bot is playing a youtube queue, use !stop and !radio_random or !radio to play radiostations')
                
            else:
                await ctx.channel.send('You are not in the voice channel or the bot playing a radiostation, use !stop to play yt links or a radiostation')
        except BaseException as e:
            await print_message_async(message='Error while starting new radio', error=str(e),came_from='Radio_Client')
    
    async def set_radio_playing_status(self,ctx,status:bool,field_specified:str, station:str = '') -> None:

        if self.discord_cog != None and field_specified == 'radio':
            self.discord_cog.radio_playing = status

        elif self.discord_cog != None and field_specified == 'radio_jsr':
            self.discord_cog.radio_jsr_playing = status
            if status == False:
                radio:Radio_JSR = random.choice(get_radios_jsr_by_station(station)) if station != '' else get_random_radio_jsr()
                await play_filler_or_music(self,ctx,radio,station)
        else:
            await print_message_async(message='Cant set the radio playing status',error='discord cog is empty',came_from='Radio_Client')

async def play_radio(self:Radio_Client,ctx,link:str, field_specified:str, station:str = '') -> None:

    if link == '' or link == None:
        await print_message_async(message='The link is empty',came_from='Radio_Client', error='error')
        return
    
    if self.discord_cog.is_audio_stopping == True:
        return
    
    try:
        channel: discord.VoiceChannel = ctx.author.voice.channel
        connection: discord.VoiceClient = await a_discord_client.connect_bot_to_channel_if_not_other_cog(self,channel)

        if connection.is_playing() == False and self.discord_cog.yt_playing == False and self.discord_cog.voice_client != None:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(link, download=False)
                URL = info['formats'][0]['url']

                audio = discord.FFmpegPCMAudio(source=URL, **self.FFMPEG_OPTIONS)
                connection.play(audio, after= lambda e: asyncio.run_coroutine_threadsafe(self.set_radio_playing_status(ctx,False,field_specified, station),self.bot.loop))

                await print_message_async(message='Streaming radio',came_from='Radio_Client')
                await self.set_radio_playing_status(ctx,True,field_specified, station)

    except BaseException as e:
        await print_message_async(message='Could not stream that radio', error=str(e),came_from='Radio_Client')
        await ctx.send('Could not stream that radio. Sorry :(')
        await self.audio_cog.stop(ctx)

async def send_station_logo(ctx, station:str) -> None:
    for jsr_station in get_stations_jsr():
        if station in jsr_station:
            await ctx.send(f'Started streaming station {station} from jetsetradio.live, enjoy those groovy beats 📼🎶', file = discord.File(f'jsr_station_logo/{station}.png'))

def join_radio_info(radios:list[Radio]) -> str:
    message=''
    for radio in radios:
        if len(message)+150 < 2000:
            message += radio.id + ' | ' + radio.title + ' | ' + radio.country + '\n'
    return message
    
#could play a bump or static before radio music for full radio immersion | 10% for static, 20% for bump and 70% for the music
async def play_filler_or_music(self: Radio_JSR,ctx, radio:Radio_JSR,station:str) -> None:
    random.seed(datetime.now().second)
    radio_determinant = random.randint(1,10)
    
    if radio_determinant <= 2 :
        await play_radio(self,ctx,random.choice(self.bumps),'radio_jsr',station)
    elif radio_determinant == 1:
        await play_radio(self,ctx,'https://jetsetradio.live/radio/stations/static.mp3','radio_jsr',station)
    else:
        await play_radio(self,ctx,radio.song_link,'radio_jsr',station)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Radio_Client(client))