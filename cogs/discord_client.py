import asyncio
from datetime import datetime
import json
import discord
from discord.ext import tasks
import os
from discord.ext import commands
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
        if channels['id'] == str(tup[0]) and tup[3] != channels['started_at']:
            insert_stream_start_data(channels['started_at'],tup[0])
            await channel.send(f'@here YOOO {tup[1].upper()} IS LIVE CHECKOUT {tup[2]}')

class Discord_Client(commands.Cog):

    def __init__(self, bot):
        super().__init__()
        self.counter = 0
        self.bot = bot

    async def setup_hook(self) -> None:
        self.listen_for_twitch_channels.start()

    @commands.Cog.listener()
    async def on_ready(self):
        c = datetime.now()
        time = c.strftime('%H:%M:%S')
        print(f'[ {time} ] Bot started working')

    @commands.command()
    async def cat_pic(self,ctx):
        urllib.request.urlretrieve('https://cataas.com/cat', 'cats/cat.jpg')
        await ctx.send(file = discord.File('cats/cat.jpg'))
        await ctx.send.add_reaction('🐱')

    @commands.command()
    async def cat_fact(self,ctx):
        data = urllib.request.urlopen('https://catfact.ninja/fact').read()
        json_object = json.loads(data.decode('utf-8'))
        await ctx.send(json_object['fact'])
    
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

    @tasks.loop(minutes=10)
    async def listen_for_twitch_channels(self):

        for tup in get_all_data_tuple():
            if len(tup) >= 3:
                req = urllib.request.Request('https://api.twitch.tv/helix/search/channels?live_only=true&query='+str(tup[1])) 
                req.add_header('Authorization', twitch_access)
                req.add_header('Client-Id', client_id)
                
                content = urllib.request.urlopen(req).read()
                json_channels = json.loads(content)
                ch = self.get_channel(1258405419273949276)
                await send_discord_notification(json_channels,tup,ch)

    @listen_for_twitch_channels.before_loop
    async def before_my_task(self):
        sqlite_init()
        await self.wait_until_ready()
        
async def setup(client: commands.Bot):
    await client.add_cog(Discord_Client(client))
        