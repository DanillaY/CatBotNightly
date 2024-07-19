import json
import random
import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
import urllib.request

import discord.ext
from cogs.c_radio_client import Radio_Client
from cogs.b_youtube_client import Youtube_Client
from cogs.c_audio_client import Audio_Client
from database.sqlite import find_twitch_start_stream_by_id, get_twitch_db_streamers, insert_stream_start_data, database_sqlite_init_from_script, database_sqlite_init_speedrun
from database.models.streamer import Streamer
from logger import print_message_async

'''
    Use this cog to only interact with discord related class,
    dont edit the name of the class,
    dont move any files from cogs folder,
    this is a cog master, you should get vars like voice_client by calling connect_bot_to_channel_if_not_other_cog function,
    dont create new instances of the master fields in other cogs,
    letters before the client name means the order of which each cog should be load, so if you load some cog in other cog then it means that the parent cog should be above the child cog, 
    cogs should not reference each other because one of them wont be able to load
'''

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
twitch_secret = os.getenv('TWITCH_BOT_SECRET')
twitch_access = os.getenv('TWITCH_ACCESS_TOKEN')
game_id = os.getenv('TWITCH_GAME_ID')
game_tags = os.getenv('TWITCH_GAME_TAGS').split(',')
ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')
channel_id = os.getenv('TEXT_CHANNEL_ID')
followed_games_ids = os.getenv('SPEEDRUN_GAMES_ID_FOLLOW')

class Discord_Client(commands.Cog):

    def __init__(self, bot: commands.Bot):
        super().__init__()
        database_sqlite_init_from_script('twitch')
        database_sqlite_init_from_script('jet_set_radio')
        self.listen_for_twitch_channels.start()
        self.listen_for_twitch_channels_specific.start() #this method will add new streamers with tags that you specified in your twitch database
        self.listen_if_bot_unused.start()
        self.radio_jsr_playing: bool = False
        self.is_audio_stopping = False
        self.radio_playing: bool = False
        self.yt_playing: bool = False
        self.youtube_queue: list[str] = []
        self.bot = bot
        self.voice_client:discord.voice_client.VoiceClient = None
        self.voice_channel:discord.VoiceChannel = None
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 15','options': '-vn -filter:a "volume=0.5"'}

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        #await database_sqlite_init_speedrun(followed_games_ids)
        await print_message_async(message='Discord cog started working',came_from='Discord_Client')
    
    @tasks.loop(minutes=30)
    async def listen_if_bot_unused(self):
        await print_message_async(message='Checking for bot unused state', came_from='Discord_Client')
        
        if self.voice_client != None and self.voice_channel != None:
            if self.voice_client.is_connected() and (len(self.voice_channel.members) == 1 or self.voice_client.is_playing() == False):
                clear_all_voice_related_fields(self)
                await self.voice_client.disconnect(force=True)
    
    @tasks.loop(minutes=20)
    async def listen_for_twitch_channels(self):
        try:
            await print_message_async(message='Sending requests to twitch api (folowed channles)', came_from='Discord_Client')

            for streamer in get_twitch_db_streamers():
                if len(get_twitch_db_streamers()) > 0:
                    json_channels = make_api_call_twitch('https://api.twitch.tv/helix/search/channels?live_only=true&query='+streamer.query)   
                    ch = await self.bot.fetch_channel(channel_id)
                    
                    await send_discord_notification_search_request(json_channels,streamer,ch)
        except BaseException as e:
            await print_message_async(message='Could not notify about streams', error=str(e), came_from='Discord_Client')

    @tasks.loop(minutes=20)
    async def listen_for_twitch_channels_specific(self):
        try:
            if(len(game_tags) == 1):
                await ch.send('Thers no tags in .env file, without tag filter you will get too much notifications so please add some (you could add multiple tags by separating them with commas)')
                return
            
            ch = await self.bot.fetch_channel(channel_id)
            await print_message_async(message='Sending requests to twitch api (specified game)', came_from='Discord_Client')
            streams = make_api_call_twitch('https://api.twitch.tv/helix/streams?type=live&game_id='+game_id)

            for stream in streams['data']:
                streamer = Streamer(stream['user_id'],stream['user_login'],'https://www.twitch.tv/'+stream['user_login'],stream['started_at'])
                list(map(lambda x: x.lower(), stream['tags']))
                await send_discord_notification_helix_request(stream,streamer)
        
        except BaseException as e:
            await print_message_async('Could not notify about streams',came_from='Discord_Client')
        
    #thers a chance that bot will leave randomly if you play a lot of music in the background, this method allowes the bot to be used after he unpredictably leaves
    @tasks.loop(minutes=2)
    async def listen_for_bot_is_alive(self):
        if self.voice_client.is_connected() == False and (len(self.youtube_queue) > 0 or self.yt_playing == True or self.radio_jsr_playing == True or self.radio_playing ==True):
            clear_all_voice_related_fields(self)
            await print_message_async('The bot was resurrected',came_from='Discord_Client')
        
    @commands.command()
    async def catbot_help(self,ctx):
        message = '\t\t\t\tBot commands\n'\
        '!cat_pic - this command will send you 🐱\n\n'\
        '!cat_fact - this command will send you an interesting fact about 🐱\n\n'\
        '!yt - this command accepts a youtube link and plays it (example: !yt https://youtu.be/dQw4w9WgXcQ?si=hlZB26WckCCtv2Ua)\n\n'\
        '!radio - accepts radio id and plays it (example: !radio F8t6xJ3p) 🎵\n\n'\
        '!radio_available_dump - this command will send you information about some radios that you could listen 📻\n\n'\
        '!radio_search_by_country - accepts country name and shows available radiostations 🏴 (example: !radio_search_by_country united kingdom)\n\n'\
        '!radio_random - this command will play a random radiostation from the world 🌍\n\n'\
        '!stop - this command will force the bot to leave the voice channel even if he is playing (please use this command after you are done using the bot) ⛔\n\n'\
        '!pause - this command will pause whatever song is playing right now ⏸️\n\n'\
        '!resume - this command will resume the paused song 🔹\n\n'\
        '!status - this command will show current status of the bot🔥\n\n'\
        '!queue - this command will show the queue of the youtube videos🎼\n\n'\
        '!jsr - this command accepts radio station name and streams random music from JetSetRadio.live🎉 (example: !jsr Future) if you wont set any radio then the bot will play random music from all jsr stations \n"Crank up the volume and wake up the neighbors!! Are you hearin this or what?  Show me what you got! I am counting on yall!"\n\n'\
        '!eight_ball - this command will look into the future and tell you upcoming results to the question that bothers you 🎱🔮\n\n'\
        '!jsr_stations - this command will show all jsr stations that you could play 📻\n\n'\
        '!wr_run - this command accepts an optional game_name value and shows the random category world record from that game, if the game_name is not set then will show a random world record (example: !wr_run garfields nightmare)\n\n'\
        'also this bot is listening for some twitch channels so you will get notification when they will start streaming'
        await ctx.send('```'+message+'```')

    @commands.command()
    async def cat_pic(self,ctx) -> None:
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        await print_message_async(message='Sending a cat picture',came_from='Discord_Client')
        await ctx.send(file = discord.File('cats/cat.jpg'))
        await ctx.send.add_reaction('🐱')

    @commands.command()
    async def cat_fact(self,ctx) -> None:
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await print_message_async(message='Sending a cat fact',came_from='Discord_Client')
        await ctx.send(json_object['fact'])

    @commands.command()
    async def status(self,ctx) -> None:
        connection = self.voice_client
        
        await print_message_async(message='Sending bot status',came_from='Discord_Client')
        if connection == None:
            await ctx.channel.send('The bot is chilling 😎')
        else:
            if connection.is_paused():
                await ctx.channel.send('The bot is paused')
            elif self.yt_playing == True:
                await ctx.channel.send('The bot is playing youtube videos')
            elif self.radio_jsr_playing == True:
                await ctx.channel.send('The bot is playing music from jetsetradio.live')
            elif self.radio_playing == True:
                await ctx.channel.send('The bot is playing music from radio')
            elif connection.is_connected():
                await ctx.channel.send('The bot is in the channel (please use !stop command)')

    @commands.command()
    async def eight_ball(self,ctx) -> None:
        answers = ('It is certain', 'It is decidedly so',
                   'Reply hazy, try again','Ask again later...',
                   'Dont count on it','My reply is no',
                   'Without a doubt','Better not tell you now',
                   'My sources say no','Yes definitely',
                   'Cannot predict now','Outlook not so good',
                   'You may rely on it','Concentrate and ask again',
                   'Very doubtful','As I see it, yes',
                   'Most likely', 'Signs point to yes', 'Stars are saying no')
        await print_message_async(message='Predicting future',came_from='Discord_Client')

        if ctx.message.content != '' and len(ctx.message.content.split('eight_ball')[1]) > 8:
            await ctx.send(random.choice(answers) + ' 🎱✨🧙‍♂️')
        else:
             await ctx.send('We are out of fairy wings, cant tell right now... 🧙‍♂️')
            
    async def async_cleanup(self):
        await print_message_async(message='Closing the bot connection',came_from='Discord_Client')

    async def close(self):
        await self.async_cleanup()
        await super().close()

async def send_discord_notification_search_request(json_channels,streamer: Streamer,channel) -> None:
    for channels in json_channels['data']:
        #check if it is not the same stream
        if str(channels['id']) == str(streamer.id) and streamer.start_stream != str(channels['started_at']) and channel != None:
            insert_stream_start_data(channels['started_at'], str(streamer.id))
            await channel.send(f'@here HEY! {streamer.query.upper()} IS LIVE \nCHECKOUT {streamer.stream_link}')
            
async def send_discord_notification_helix_request(stream:str, streamer:Streamer, channel: discord.VoiceChannel) -> None:
    for tag_stream in game_tags:
        has_tag = ((str.lower(tag_stream) in stream['tags']) or (str.lower(tag_stream) in str.lower(stream['title'])))

        if has_tag and find_twitch_start_stream_by_id(streamer.id,streamer.start_stream) == False:
            insert_stream_start_data(stream['started_at'], str(streamer.id))
            await channel.send(f'@here HEY! {streamer.query.upper()} IS LIVE \nCHECKOUT {streamer.stream_link}')

def make_api_call_twitch(link) -> dict:
    req = urllib.request.Request(link)
    req.add_header('Authorization', twitch_access)
    req.add_header('Client-Id', client_id)
                    
    content = urllib.request.urlopen(req).read()
    return json.loads(content)

def clear_all_voice_related_fields(self:Discord_Client) -> None:
    self.voice_channel = None
    self.voice_client = None
    self.is_audio_stopping = False
    self.yt_playing = False
    self.radio_jsr_playing = False
    self.radio_playing = False
    self.youtube_queue.clear()

#use this method to access vc and channel from other cogs
async def connect_bot_to_channel_if_not_other_cog(self: Radio_Client | Youtube_Client | Audio_Client, channel:discord.VoiceChannel) -> discord.VoiceClient:
    if self.discord_cog.voice_client == None or self.discord_cog.voice_channel == None:
        connection = await channel.connect()
        self.discord_cog.voice_client = connection
        self.discord_cog.voice_channel = channel
        return connection
    else:
        return self.discord_cog.voice_client

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Discord_Client(client))