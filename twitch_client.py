import json
import discord
from discord.ext import tasks
from discord.ext import tasks
import os
from dotenv import load_dotenv
import urllib.request

from sqlite import get_all_data_tuple, insert_stream_start_data, sqlite_init

load_dotenv()
client_id = os.getenv('TWITCH_CLIENT_ID')
twitch_secret = os.getenv('TWITCH_BOT_SECRET')
twitch_access = os.getenv('TWITCH_ACCESS_TOKEN')

async def send_discord_notification(json_channels,tup,channel):

    for channels in json_channels['data']:
        #check if it is not the same stream
        if channels['id'] == str(tup[0]) and tup[3] != channels['started_at']:
            insert_stream_start_data(channels['started_at'],tup[0])
            await channel.send(f'@here YOOO {tup[1].upper()} IS LIVE CHECKOUT {tup[2]}')

class Twitch_Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = 0

    async def setup_hook(self) -> None:
        self.listen_for_twitch_channels.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    @tasks.loop(minutes=10)
    async def listen_for_twitch_channels(self):

        for tup in get_all_data_tuple():
        
            if len(tup) >= 3:
                req = urllib.request.Request('https://api.twitch.tv/helix/search/channels?live_only=true&query='+str(tup[1])) 
                req.add_header('Authorization', twitch_access)
                req.add_header('Client-Id', client_id)
                
                content = urllib.request.urlopen(req).read()
                json_channels = json.loads(content)
                ch = self.get_guild(1258405418670096406).get_channel(1258405419273949276)
                await send_discord_notification(json_channels,tup,ch)
                
    @listen_for_twitch_channels.before_loop
    async def before_my_task(self):
        sqlite_init()
        await self.wait_until_ready()
    