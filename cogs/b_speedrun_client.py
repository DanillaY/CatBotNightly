from datetime import datetime
import json
import os
import random
import string
import discord
from discord.ext import tasks, commands
from requests import get

from logger import print_message_async

games_follow = os.getenv('SPEEDRUN_GAMES_FOLLOW').split(',')

class Speedrun_Cog(commands.Cog):

    def __init__(self,bot : commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await print_message_async(message='Speedrun cog started working',came_from='Speedrun_Client')

    #if the game_name is empty will send a random world record speedrun
    @commands.command()
    async def wr_run(self,ctx,game_name:str='') -> None:
        try:

            if game_name.lower() == 'false' or game_name.lower() == 'true':
                ctx.channel.send('Incorrect game name input')

            random.seed(datetime.now().second)
            offset = random.randint(1,41000) #need to figure out how to get the max offest amount

            if game_name != '':
                game_name:str = ctx.message.content.split('wr_run')[1].strip()
                print(game_name)

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
    await client.add_cog(Speedrun_Cog(client))