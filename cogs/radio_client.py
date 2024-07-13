from datetime import datetime
import os

import discord
import yt_dlp
from database.radio import Radio
from discord.ext import commands

from database.sqlite import does_radio_db_exist, get_radio_db_info, get_radios_by_country, get_random_radio

ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

class Radio_Client(commands.Cog):
    
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.voice_client:discord.voice_client.VoiceClient = None
        self.voice_channel:discord.VoiceChannel = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.5"'}
    
    #shows first few records of radios in database (because of the 2000 chars limit per message)
    @commands.command()
    async def radio_available_dump(self,ctx) -> None:
        message = join_radio_info(get_radio_db_info())
        await ctx.send('```'+message+'```')
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message('Radio cog started working')
    
    @commands.command()
    async def radio(self,ctx, radio_id) -> None:
        if ctx.author.voice != None and len(self.bot.get_cog('Discord_Client').youtube_queue) == 0:
            await print_message('Started playing radio')
            await play_radio(self,ctx,radio_id)
        elif does_radio_db_exist(radio_id) == False:
            await ctx.channel.send('Radio with that id does not exist')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @commands.command()
    async def radio_search_by_country(self,ctx,country) -> None:
        radios = get_radios_by_country(country)
        if len(radios) == 0:
            await ctx.send('Nothing was found in that country')
        else:
            await print_message('Bot is searching radios by country')
            message = join_radio_info(get_radios_by_country(country))
            await ctx.send('```'+message+'```')
    
    async def print_message(message:str) -> None:
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[{time}] {message}')
    
    async def close(self):
        await self.async_cleanup()
        await super().close()
    
    @commands.command()
    async def radio_random(self,ctx) -> None:
        if ctx.author.voice != None and len(self.bot.get_cog('Discord_Client').youtube_queue) == 0:
            radio:Radio = get_random_radio()
            await play_radio(self,ctx,radio.id)
            await ctx.channel.send(f'Right now playing {radio.title}, country {radio.country}, id {radio.id}')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

async def connect_bot_to_channel_if_not(self:Radio_Client,channel:discord.VoiceChannel) -> discord.VoiceClient:
    if self.voice_client == None or self.voice_channel == None:
            connection = await channel.connect()
            self.voice_client = connection
            self.voice_channel = channel
            return connection
    else:
        return self.voice_client
    
async def play_radio(self:Radio_Client,ctx,radio_id) -> None:

    try:
        channel: discord.VoiceChannel = ctx.author.voice.channel
        connection: discord.VoiceClient = await connect_bot_to_channel_if_not(self,channel)

        if connection.is_playing() == False:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3', download=False)
                URL = info['formats'][0]['url']

                audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source=URL, **self.FFMPEG_OPTIONS)
                connection.play(audio)
    except:
        await ctx.send('Could not stream that radio. Sorry :(')
        await connection.disconnect()

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Radio_Client(client))

def join_radio_info(radios:list[Radio]) -> str:
    message=''
    for radio in radios:
        if len(message)+150 < 2000:
            message += radio.id + '|' + radio.title + '|' + radio.country + '\n'
    return message

async def print_message(message:str) -> None:
    c = datetime.now()
    time = c.strftime('%H:%M:%S')
    print(f'[{time}] {message}')