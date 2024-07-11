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
game_id = os.getenv('TWITCH_GAME_ID')
game_tags = os.getenv('TWITCH_GAME_TAGS').split(',')
ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')
channel_id = os.getenv('TEXT_CHANNEL_ID')

async def send_discord_notification(json_channels,streamer: Streamer,channel) -> None:
    for channels in json_channels['data']:
        #check if it is not the same stream

        if channels['id'] == str(streamer.id) and streamer.start_stream != str(channels['started_at']) and channel != None:
            insert_stream_start_data(channels['started_at'], str(streamer.id))
            await channel.send(f'@here YOOO {streamer.query.upper()} IS LIVE CHECKOUT {streamer.stream_link}')

async def print_message(message:str) -> None:
    c = datetime.now()
    time = c.strftime('%H:%M:%S')
    print(f'[{time}] {message}')

async def play_radio(self,ctx,radio_id):

    try:
        channel: discord.VoiceChannel = ctx.author.voice.channel
        connection: discord.VoiceClient = self.bot.voice_clients
        if len(self.bot.voice_clients) == 0:
            connection = await channel.connect()

        if connection.is_playing() == False:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(f'http://radio.garden/api/ara/content/listen/{radio_id}/channel.mp3', download=False)
                URL = info['formats'][0]['url']

                audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source=URL)
                connection.play(audio)
    except:
        await ctx.send('Could not stream that radio. Sorry :(')
        await connection.disconnect()
    
    
def join_radio_info(radios:list[Radio]) -> str:
    message=''
    for radio in radios:
        if len(message)+150 < 2000:
            message += radio.id + '|' + radio.title + '|' + radio.country + '\n'
    return message

def make_api_call_twitch(link) -> dict:
    req = urllib.request.Request(link)
    req.add_header('Authorization', twitch_access)
    req.add_header('Client-Id', client_id)
                    
    content = urllib.request.urlopen(req).read()
    return json.loads(content)

class Discord_Client(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        twitch_sqlite_init()
        self.listen_for_twitch_channels.start()
        self.listen_for_twitch_channels_specific.start()
        self.bot = bot
        self.youtube_queue = []

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message('Bot started working')
    
    @tasks.loop(minutes=20)
    async def listen_for_twitch_channels(self):
        try:
            await print_message('Sending requests to twitch api (folowed channles)')

            for streamer in get_twitch_db_streamers():
                if len(get_twitch_db_streamers()) > 0:
                    json_channels = make_api_call_twitch('https://api.twitch.tv/helix/search/channels?live_only=true&query='+streamer.query)   
                    ch = await self.bot.fetch_channel(channel_id)
                    
                    await send_discord_notification(json_channels,streamer,ch)
        except BaseException as e:
            print('Could not notify about streams\n', e)
    
    @tasks.loop(minutes=10)
    async def listen_for_twitch_channels_specific(self):
        try:
            await print_message('Sending requests to twitch api (specified game)')
            ch = await self.bot.fetch_channel(channel_id)
            
            streams = make_api_call_twitch('https://api.twitch.tv/helix/streams?type=live&game_id='+game_id)
            for stream in streams['data']:
                streamer = Streamer(stream['user_id'],stream['user_login'],'https://www.twitch.tv/'+stream['user_login'],stream['started_at'])

                if(len(game_tags) == 0):
                    await ch.send('Thers no tags in .env file, without tag filter you will get too much notifications so please add some (you could add multiple tags by separating tags with commas)')
                else:
                    for tag_stream in stream['tags']:
                        for tag_search in game_tags:
                            if (str.lower(tag_search) == str.lower(tag_stream)) or (tag_search in stream['title']):
                                await ch.send(f'@here YOOO {streamer.query.upper()} IS LIVE CHECKOUT {streamer.stream_link}')
            

        except BaseException as e:
            print('Could not notify about streams\n', e)
    
    @commands.command()
    async def catbot_help(self,ctx):
        message = '\t\t\t\tBot commands\n'\
        '----------------------------------------------\n'\
        '!cat_pic - this command will send you 🐱\n\n'\
        '!cat_fact - this command will send you an interesting fact about 🐱\n\n'\
        '!yt - this command accepts a youtube link and plays it (example: !yt https://youtu.be/dQw4w9WgXcQ?si=hlZB26WckCCtv2Ua)\n\n'\
        '!radio - accepts radio id and plays it (example: !radio F8t6xJ3p) 🎵\n\n'\
        '!radio_available_dump - this command will send you information about some radios that you could listen 📻\n\n'\
        '!radio_search_by_country - accepts country name and shows available radiostations 🏴 (example: !radio_search_by_country united kingdom)\n\n'\
        '!radio_random - this command will play a random radiostation from the world 🌍\n\n'\
        '!stop - this command will force the bot to leave the voice channel even if he is playing (please you this command after you are done using the bot) ⛔\n\n'\
        '!pause - this command will pause whatever song is playing right now\n\n'\
        '!resume - this command will resume the paused song\n\n'\
        '!status - this command will show current status of the bot\n\n'\
        'also this bot is listening for some twitch channels so you will get notification when they will start streaming'
        await ctx.send('```'+message+'```')

    @commands.command()
    async def cat_pic(self,ctx) -> None:
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        await print_message('Sending a cat picture')
        await ctx.send(file = discord.File('cats/cat.jpg'))
        await ctx.send.add_reaction('🐱')

    @commands.command()
    async def cat_fact(self,ctx) -> None:
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await print_message('Sending a cat fact')
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
            await print_message('Bot is searching radios by country')
            message = join_radio_info(get_radios_by_country(country))
            await ctx.send('```'+message+'```')

    @commands.command()
    async def stop(self,ctx) -> None:
        connection: discord.VoiceClient = self.bot.voice_clients[0]
        if ctx.author.voice != None and connection != None:
           await connection.disconnect(force=True)
           await print_message('Bot is stopped')
        else:
            await ctx.channel.send('This song is unstoppable')
    
    @commands.command()
    async def pause(self,ctx) -> None:
        connection: discord.VoiceClient = self.bot.voice_clients[0]
        if ctx.author.voice != None and connection.is_playing():
           connection.pause()
           await print_message('Bot is paused')
        else:
            await ctx.channel.send('Cant pause current song')

    @commands.command()
    async def resume(self,ctx) -> None:
        connection: discord.VoiceClient = self.bot.voice_clients[0]
        if ctx.author.voice != None and connection.is_paused():
           connection.resume()
        else:
            await ctx.channel.send('Cant resume current song')

    @commands.command()
    async def radio(self,ctx, radio_id) -> None:
        if ctx.author.voice != None and len(self.youtube_queue) == 0:
            await print_message('Started playing radio')
            await play_radio(self,ctx,radio_id)
        elif does_radio_db_exist(radio_id) == False:
            await ctx.channel.send('Radio with that id does not exist')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @commands.command()
    async def radio_random(self,ctx) -> None:
        if ctx.author.voice != None and len(self.youtube_queue) == 0:
            radio:Radio = get_random_radio()
            await play_radio(self,ctx,radio.id)
            await ctx.channel.send(f'Right now playing {radio.title}, country {radio.country}, id {radio.id}')
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')
    
    @commands.command()
    async def status(self,ctx) -> None:
        connection = self.bot.voice_clients
        await print_message('Sending bot status')
        if len(self.bot.voice_clients) == 0:
            await ctx.channel.send('The bot is chilling 😎')
        else:
            if connection[0].is_paused():
                await ctx.channel.send('The bot is paused')
            elif connection[0].is_playing():
                await ctx.channel.send('The bot is playing music')
            elif connection[0].is_connected():
                await ctx.channel.send('The bot is in the channel (please use !stop command)')
                
    @commands.command()
    async def yt(self,ctx,link) -> None:
        if ctx.author.voice != None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            connection: discord.VoiceClient = self.bot.voice_clients

            if len(self.bot.voice_clients) == 0:
                connection = await channel.connect()

            try:
                if connection.is_playing() == False and connection.is_paused() == False:

                    with yt_dlp.YoutubeDL({'options': '-vn'}) as ydl:
                        FFMPEG_OPTIONS = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M', 'options': '-vn' }
                        info = ydl.extract_info(link, download=False)
                        URL = info['requested_formats'][1]['url']
                        self.youtube_queue.append(URL)

                audio = discord.FFmpegPCMAudio(source=URL, **FFMPEG_OPTIONS, executable=ffmpeg_exe_path)
                connection.play(source=audio)
            except BaseException as e:
                print_message('Could not play yt video', e)
                connection.disconnect(force=True)
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @radio.error
    async def info_error(ctx, error) -> None:
        if isinstance(error, commands.BadArgument):
            await ctx.send('Error?...' + str(error))
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Discord_Client(client))