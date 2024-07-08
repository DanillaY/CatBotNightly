import asyncio
from datetime import datetime
import json
import discord
from discord.ext import tasks, commands
import os
from dotenv import load_dotenv
import youtube_dl
import urllib.request

import discord.ext
from sqlite import get_all_data_tuple, insert_stream_start_data, sqlite_init

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
twitch_secret = os.getenv('TWITCH_BOT_SECRET')
twitch_access = os.getenv('TWITCH_ACCESS_TOKEN')
ffmpeg_exe_path = os.getenv('FFMPEG_EXE_PATH')

async def send_discord_notification(json_channels,tup,channel):
    for channels in json_channels['data']:
        #check if it is not the same stream
        if channels['id'] == str(tup[0]) and tup[3] != channels['started_at'] and channel != None:
            insert_stream_start_data(channels['started_at'],tup[0])
            await channel.send(f'@here YOOO {tup[1].upper()} IS LIVE CHECKOUT {tup[2]}')

class Discord_Client(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        sqlite_init()
        self.counter = 0
        self.listen_for_twitch_channels.start()
        self.bot = bot

    #async def setup_hook(self) -> None:
     #   print('111')
     #   await sqlite_init()
     #   self.loop.create_task(self.isten_for_twitch_channels())

    @commands.Cog.listener()
    async def on_ready(self):
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[{time}] Bot started working')
    
    @tasks.loop(seconds=10)
    async def listen_for_twitch_channels(self):
        try:
            for tup in get_all_data_tuple():
                if len(tup) >= 3:
                    req = urllib.request.Request('https://api.twitch.tv/helix/search/channels?live_only=true&query='+str(tup[1])) 
                    req.add_header('Authorization', twitch_access)
                    req.add_header('Client-Id', client_id)
                    
                    content = urllib.request.urlopen(req).read()
                    json_channels = json.loads(content)
                    ch = self.bot.get_channel(1258405419273949276)
                    await send_discord_notification(json_channels,tup,ch)
        except BaseException as e:
            print('Could not notify about streams')
            print(e)

    @commands.command()
    async def cat_pic(self,ctx):
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[{time}] Sending a cat picture')
        await ctx.send(file = discord.File('cats/cat.jpg'))
        await ctx.send.add_reaction('🐱')

    @commands.command()
    async def cat_fact(self,ctx):
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await ctx.send(json_object['fact'])

    @commands.command()
    async def radio(self,ctx):
        if ctx.author.voice != None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            connection: discord.VoiceClient = await channel.connect()
            #await urllib.request.urlretrieve('http://radio.garden/api/ara/content/listen/vbFsCngB/channel.mp3','radio.mp3')

            audio = discord.FFmpegPCMAudio(executable=ffmpeg_exe_path,source='mis.mp3')
            connection.play(audio) 
            
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')
    
    @commands.command()
    async def yt(self,ctx,link):
        if ctx.author.voice != None:
            channel: discord.VoiceChannel = ctx.author.voice.channel
            connection: discord.VoiceClient = await channel.connect()

            try:
                print('TO DO download mp3 and rewrite it to tmp file')
            except BaseException as e:
                print('Could not play yt video')
                print(e)
        else:
            await ctx.channel.send('You should be in the voice channel to use that command')

    @radio.error
    async def info_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Error?...' + str(error))
        
async def setup(client: commands.Bot):
    await client.add_cog(Discord_Client(client))

#TO DO this method locks the whole program, in order to make bot leade after playing the source need to figure out how to use that method
def after_voice_msg_done(channel:discord.VoiceChannel, client:discord.voice_client):
    coro = channel.send('Song is done!')
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
    fut.result()
    client.disconnect()