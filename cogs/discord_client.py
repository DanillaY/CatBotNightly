import asyncio
from datetime import datetime
import json
import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
import urllib.request

import discord.ext
import yt_dlp
from database.radio import Radio
from database.sqlite import does_radio_db_exist, get_radio_db_info, get_radios_by_country, get_random_radio, get_twitch_db_streamers, insert_stream_start_data, twitch_sqlite_init
from database.streamer import Streamer

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
twitch_secret = os.getenv('TWITCH_BOT_SECRET')
twitch_access = os.getenv('TWITCH_ACCESS_TOKEN')
ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')
channel_id = os.getenv('TEXT_CHANNEL_ID')

async def send_discord_notification(json_channels,streamer: Streamer,channel):
    for channels in json_channels['data']:
        #check if it is not the same stream
        if channels['id'] == str(streamer.id) and streamer.start_stream != channels['started_at'] and channel != None:
            insert_stream_start_data(channels['started_at'],streamer.id)
            await channel.send(f'@here YOOO {streamer.query.upper()} IS LIVE CHECKOUT {streamer.streamer_link}')

async def play_radio(self,ctx,radio_id):

    try:
        channel: discord.VoiceChannel = ctx.author.voice.channel
        connection: discord.VoiceClient = self.bot.voice_clients
        
        if len(self.bot.voice_clients) == 0:
                connection = await channel.connect() 

        if connection.is_playing() == False:
            with yt_dlp.YoutubeDL(params={}) as ydl:
                info = ydl.extract_info(f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3', download=False)
                URL = info['formats'][0]['url']
    except:
        await ctx.send('Could not stream that radio. Sorry :(')
        await connection.disconnect()
    
    audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source=URL)
    connection.play(audio)

def join_radio_info(radios:list[Radio]):
    message=''
    for radio in radios:
        if len(message)+150 < 2000:
            message += radio.id + '|' + radio.title + '|' + radio.country + '\n'
    return message

class Discord_Client(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        twitch_sqlite_init()
        self.counter = 0
        self.listen_for_twitch_channels.start()
        self.bot = bot
        self.FFMPEG_OPT = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[{time}] Bot started working')
    
    @tasks.loop(minutes=10)
    async def listen_for_twitch_channels(self):
        try:
            time = datetime.now().strftime('%H:%M:%S')
            print(f'[{time}] Sending requests to twitch api')

            for streamer in get_twitch_db_streamers():
                if len(get_twitch_db_streamers()) > 0:
                    req = urllib.request.Request('https://api.twitch.tv/helix/search/channels?live_only=true&query='+streamer.query) 
                    req.add_header('Authorization', twitch_access)
                    req.add_header('Client-Id', client_id)
                    
                    content = urllib.request.urlopen(req).read()
                    json_channels = json.loads(content)
                    ch = await self.bot.fetch_channel(channel_id)
                    
                    await send_discord_notification(json_channels,streamer,ch)
        except BaseException as e:
            print('Could not notify about streams\n', e)
    
    @commands.command()
    async def catbot_help(self,ctx):
        message = 'Bot commands: \n'\
        '-----------------------------------\n'\
        '!cat_pic - this command will send you 🐱\n\n'\
        '!cat_fact - this command will send you an interesting fact about 🐱\n\n'\
        '!radio - accepts radio id and plays it (example: !radio F8t6xJ3p) 🎵\n\n'\
        '!radio_available_dump - this command will send you information about some radios that you could listen 📻\n\n'\
        '!radio_search_by_country - accepts country name and shows available radiostations 🏴 (example: !radio_search_by_country united kingdom)\n\n'\
        '!radio_random - this command will play a random radiostation from the world 🌍\n\n'\
        'also this bot is listening for some twitch channels so you will get notification when they will start streaming'
        await ctx.send('```'+message+'```')

    @commands.command()
    async def cat_pic(self,ctx) -> None:
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[{time}] Sending a cat picture')
        await ctx.send(file = discord.File('cats/cat.jpg'))
        await ctx.send.add_reaction('🐱')

    @commands.command()
    async def cat_fact(self,ctx) -> None:
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await ctx.send(json_object['fact'])

    #shows first few records of radios in database (because of the 2000 chars limit per message)
    @commands.command()
    async def radio_available_dump(self,ctx) -> None:
        message = join_radio_info(get_radio_db_info())
        await ctx.send('```'+message+'```')

    @commands.command()
    async def radio_search_by_country(self,ctx,country) -> None:
        radios = get_radios_by_country(country)
        if len(radios) == 0:
            await ctx.send('Nothing was found in that country')
        else:
            message = join_radio_info(get_radios_by_country(country))
            await ctx.send('```'+message+'```')

    @commands.command()
    async def radio(self,ctx, radio_id):
        if ctx.author.voice != None:
            await play_radio(self,ctx,radio_id)
        elif does_radio_db_exist(radio_id) == False:
            await ctx.channel.send('Radio with that id does not exist')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')
        '''
        if ctx.author.voice != None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            connection: discord.VoiceClient = self.bot.voice_clients

            if len(self.bot.voice_clients) == 0:
                connection = await channel.connect() 

            if connection.is_playing() == False:
                with yt_dlp.YoutubeDL(params={}) as ydl:
                    info = ydl.extract_info(f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3', download=False)
                    URL = info['formats'][0]['url']

                audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source=URL)
                connection.play(audio) 
        '''
    @commands.command()
    async def radio_random(self,ctx):
        if ctx.author.voice != None:
            radio:Radio = get_random_radio()
            await play_radio(self,ctx,radio.id)
            await ctx.channel.send(f'Right now playing {radio.title}, country {radio.country}, id {radio.id}')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @commands.command()
    async def yt(self,ctx,link) -> None:
        if ctx.author.voice != None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            connection: discord.VoiceClient = await channel.connect()

            try:
                print('TO DO download mp3 and rewrite it to tmp file')
            except BaseException as e:
                print('Could not play yt video', e)
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @radio.error
    async def info_error(ctx, error) -> None:
        if isinstance(error, commands.BadArgument):
            await ctx.send('Error?...' + str(error))
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Discord_Client(client))

#TO DO this method locks the whole program, in order to make bot leade after playing the source need to figure out how to use that method
def after_voice_msg_done(channel:discord.VoiceChannel, client:discord.voice_client) -> None:
    coro = channel.send('Song is done!')
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
    fut.result()
    client.disconnect()