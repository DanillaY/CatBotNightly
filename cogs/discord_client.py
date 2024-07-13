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

class Discord_Client(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        twitch_sqlite_init()
        #self.listen_for_twitch_channels.start()
        self.listen_for_twitch_channels_specific.start()
        self.listen_if_bot_unused.start()
        self.bot = bot
        self.voice_client:discord.voice_client.VoiceClient = None
        self.voice_channel:discord.VoiceChannel = None
        self.youtube_queue: list[str] = []
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.5"'}

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message('Discord cog started working')
    
    @tasks.loop(minutes=30)
    async def listen_if_bot_unused(self):
        await print_message('Checking for bot unused state')
        
        if self.voice_client != None and self.voice_channel != None:
            print(len(self.voice_channel.members))
            if self.voice_client.is_connected() and len(self.voice_channel.members) == 1:
                await self.voice_client.disconnect(force=True)
                self.voice_channel = None
                self.voice_client = None
    
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

    @tasks.loop(minutes=20)
    async def listen_for_twitch_channels_specific(self):
        try:
            await print_message('Sending requests to twitch api (specified game)')
            ch = await self.bot.fetch_channel(channel_id)
            
            streams = make_api_call_twitch('https://api.twitch.tv/helix/streams?type=live&game_id='+game_id)
            for stream in streams['data']:
                streamer = Streamer(stream['user_id'],stream['user_login'],'https://www.twitch.tv/'+stream['user_login'],stream['started_at'])

                if(len(game_tags) > 0):
                    for tag_stream in stream['tags']:
                        for tag_search in game_tags:
                            if (str.lower(tag_search) == str.lower(tag_stream)) or (tag_search in stream['title']):
                                await ch.send(f'@here YOOO {streamer.query.upper()} IS LIVE CHECKOUT {streamer.stream_link}')
                else:
                    await ch.send('Thers no tags in .env file, without tag filter you will get too much notifications so please add some (you could add multiple tags by separating tags with commas)')
            

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
        '!stop - this command will force the bot to leave the voice channel even if he is playing (please use this command after you are done using the bot) ⛔\n\n'\
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

    #TODO stop method doesnt work with radio player
    @commands.command()
    async def stop(self,ctx) -> None:
        connection: discord.VoiceClient = self.voice_client
        if ctx.author.voice != None and connection != None:
           await connection.disconnect(force=True)
           await print_message('Bot is stopped')
           self.voice_channel = None
           self.voice_client = None
           self.youtube_queue.clear()
        else:
            await ctx.channel.send('This song is unstoppable')
    
    #TO DO fix skip method
    @commands.command()
    async def skip_yt(self,ctx):
        if ctx.author.voice != None or (self.voice_channel != None and self.voice_client != None) or len(self.youtube_queue)>0:
            if self.voice_client.is_playing():
                self.voice_client.stop()
                await self.play_next_yt(ctx)
        else:
            await ctx.channel.send('Could not skip the song')
    
    @commands.command()
    async def pause(self,ctx) -> None:
        connection: discord.VoiceClient = self.voice_client
        if ctx.author.voice != None and connection.is_playing() and connection != None:
           connection.pause()
           await print_message('Bot is paused')
        else:
            await ctx.channel.send('Cant pause current song')

    @commands.command()
    async def resume(self,ctx) -> None:
        connection: discord.VoiceClient = self.voice_client
        if ctx.author.voice != None and connection.is_paused() and connection != None:
           connection.resume()
        else:
            await ctx.channel.send('Cant resume current song')

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
    
    async def play_next_yt(self, ctx):

        if len(self.youtube_queue) > 0:
            self.youtube_queue.pop(0)
            try:
                await self.yt(ctx, self.youtube_queue[0] if len(self.youtube_queue) > 0 else None)
            except BaseException as e:
                await print_message(e)
            
        else:
            ctx.channel.send('Youtube queue has ended')
            await self.voice_client.disconnect()

    async def add_to_yt_queue(self,ctx,link):
        await print_message('Added new song to the queue')
        self.youtube_queue.append(link)

    @commands.command()
    async def yt(self,ctx,link) -> None:

        if ctx.author.voice == None:
            await ctx.channel.send('You should be in the voice channel to use that command')
            return

        try:
            channel: discord.VoiceChannel = ctx.author.voice.channel if self.voice_channel == None else self.voice_channel
            connection: discord.VoiceClient = await connect_bot_to_channel_if_not(self,channel)

            if self.voice_client.is_playing() and link != None:
                await self.add_to_yt_queue(ctx,link)
                await ctx.channel.send('Song was added the queue')
            else:
                with yt_dlp.YoutubeDL({'options': '-vn'}) as ydl:
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(None, lambda: ydl.extract_info(link, download=False))
                    URL = info['requested_formats'][1]['url']
                    self.youtube_queue.append(URL)

                    audio = discord.FFmpegPCMAudio(source=URL, **self.FFMPEG_OPTIONS, executable=ffmpeg_exe_path)
                    play_next = lambda e: asyncio.run_coroutine_threadsafe(self.play_next_yt(ctx), self.bot.loop)
                connection.play(source=audio, after=play_next)
   
        except BaseException as e:
            await print_message(f'Could not play yt video {e}')
            await connection.disconnect(force=True)

    async def async_cleanup(self):
        print_message('Closing the bot connection')

    async def close(self):
        await self.async_cleanup()
        await super().close()
        
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Discord_Client(client))

async def connect_bot_to_channel_if_not(self:Discord_Client,channel:discord.VoiceChannel) -> discord.VoiceClient:
    if self.voice_client == None or self.voice_channel == None:
            connection = await channel.connect()
            self.voice_client = connection
            self.voice_channel = channel
            return connection
    else:
        return self.voice_client

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