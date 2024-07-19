from datetime import datetime
import json
import os
import random
import string
import discord
from discord.ext import tasks, commands
from requests import get

from database.models.speedrun import Speedrun
from database.sqlite import does_record_db_exist, insert_new_speedrun
from logger import print_message_async

games_ids = os.getenv('SPEEDRUN_GAMES_ID_FOLLOW')
channel_id = os.getenv('TEXT_CHANNEL_ID')

class Speedrun_Client(commands.Cog):

    def __init__(self,bot : commands.Bot):
        super().__init__()
        self.bot = bot
        self.listen_for_new_speedruns.start()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message_async(message='Speedrun cog started working',came_from='Speedrun_Client')
    
    @tasks.loop(minutes=20)
    async def listen_for_new_speedruns(self):
        try:
            
            await print_message_async(message='Sending requests to speedrun.com api (followed games)',came_from='Speedrun_Client')

            games_ids_follow = games_ids.split(',')
            ch = await self.bot.fetch_channel(channel_id)

            for game_id in games_ids_follow:
                game_info:str = get(f'https://www.speedrun.com/api/v1/games/{game_id}').text
                json_categories = json.loads(game_info)
                game_name = json_categories['data']['names']['international']

                categories:str = get(f'https://www.speedrun.com/api/v1/games/{game_id}/categories').text
                json_categories = json.loads(categories)
                category_ids = []
                for category in json_categories['data']:
                    if category['type'] == 'per-game':
                        category_ids.append(category['id'])

                for category_id in category_ids:
                    runs:str = get(f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category_id}').text
                    json_runs = json.loads(runs)['data']['runs']

                    category_info:str = get(f'https://www.speedrun.com/api/v1/categories/{category_id}').text
                    category_name = json.loads(category_info)['data']['name']

                    for run in json_runs:
                        speedrun_link = run['run']['weblink']
                        run_id = run['run']['id']
                        date = run['run']['date']

                        if does_record_db_exist(run_id,'speedrun','RunId') == False:
                            await ch.send(f'@here Thers a new {game_name} speedrun posted in the {category_name} category! \nCheckout: {speedrun_link}')
                            insert_new_speedrun(Speedrun(None,game_id,run_id,speedrun_link,game_name,category_name,date))
                            
        except BaseException as e:
            await print_message_async(message='Error while sending requests to speedrun.com api (followed games)',came_from='Speedrun_Client',error=str(e))
                

    #if the game_name is empty will send a random world record speedrun
    @commands.command()
    async def wr_run(self,ctx,game_name:str='') -> None:
        try:

            random.seed(datetime.now().second)
            offset = random.randint(1,41000) #need to figure out how to get the max offset amount

            if game_name != '':
                game_name:str = ctx.message.content.split('wr_run')[1].strip()

            if game_name == '':
                game_id:str = await get_value_from_api_answer(link_request= f'https://www.speedrun.com/api/v1/games?max=20&offset={offset}&skip-empty=true',attr_field='id',random_run=True)
            else:
                game_id:str = await get_value_from_api_answer(link_request= f'https://www.speedrun.com/api/v1/games?max=20&skip-empty=true&name={game_name}',attr_field='id',random_run=False)

            print( f'https://www.speedrun.com/api/v1/games?max=20&skip-empty=true&name={game_name}')
            if game_id == '' and game_name != '':
                await ctx.channel.send('Game was not found')
                return

            category_id:str = await get_value_from_api_answer(link_request=f'https://www.speedrun.com/api/v1/games/{game_id}/categories',attr_field= 'id')
            runs:str = get(f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category_id}?video-only=true').text
            runs_json = json.loads(runs)

            world_record_run = runs_json['data']['runs'][0]
            run_comment = world_record_run['run']['comment']
            speedrun_link = world_record_run['run']['weblink']
            video_run_link = world_record_run['run']['videos']['links'][0]['uri']
            date = world_record_run['run']['date']

            if world_record_run != '' and run_comment != None:
                await ctx.channel.send(f'Speedrun.com link - {speedrun_link} \nVideo link - {video_run_link}\nWith the comment - {run_comment}\nSubmitted date - {date}')
            elif world_record_run != '' and run_comment == None:
                await ctx.channel.send(f'Speedrun.com link - {speedrun_link} \nVideo link - {video_run_link}\nWithout the comment\nSubmitted date - {date}')
            
            await print_message_async(message='Sending wr run', came_from='Speedrun_Client')
        except BaseException as e:
            await print_message_async(message='Erorr while sending wr run', came_from='Speedrun_Client', error=str(e))

async def get_value_from_api_answer(link_request:str,attr_field:str,random_run:bool = True) -> str:
        if link_request == '':
            await print_message_async('The request link is empty')
            return
        
        api_answer:str = get(link_request).text
        request_list_json = json.loads(api_answer)
        json_items: list[str] = []

        for item in request_list_json['data']:
            json_items.append(item[attr_field])

        if len(json_items) == 0:
            return ''
        
        result = random.choice(json_items)
        if random_run == True:
            return result
        elif json_items[0] != None:
            return json_items[0]

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Speedrun_Client(client))