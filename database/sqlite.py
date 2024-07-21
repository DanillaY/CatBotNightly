import asyncio
from imaplib import Commands
import json
import os
from random import randint
import random
import sqlite3
from requests import get
from discord.ext import commands

from database.models.radio import Radio, list_tuple_to_radio_list
from database.models.radio_jsr import Radio_JSR, list_tuple_to_radio_jsr_list
from database.models.speedrun import Speedrun
from database.models.streamer import Streamer, list_tuple_to_streamer_list
from logger import print_message, print_message_async

def database_sqlite_init_from_script(database_name:str) -> None:
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()

    with open(f'./database/sql_scripts/{database_name}.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    connection.commit()
    connection.close()

def insert_new_streamer(streamer:Streamer) -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()
    cursor.execute('INSERT OR REPLACE INTO twitch VALUES(?,?,?,?)',(streamer.id,streamer.query,streamer.stream_link,streamer.start_stream))

    connection.commit()
    connection.close()

def insert_new_speedrun(speedrun:Speedrun) -> None:
    connection = sqlite3.connect('speedrun.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO speedrun VALUES(?,?,?,?,?,?,?)',(speedrun.id,speedrun.game_id,speedrun.run_id,speedrun.speedrun_link,speedrun.game_name,speedrun.category,speedrun.date))

    connection.commit()
    connection.close()

def update_stream_start_data(start_stream, id) -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE twitch SET StartStream = ? WHERE id = ?',(start_stream, id))
    connection.commit()
    connection.close()

def get_twitch_db_streamers() -> list:
    tuple_list = get_all_from_twitch()
    return list_tuple_to_streamer_list(tuple_list)

def get_radio_db_info() -> list:
    tuple_list = get_all_from_radio()
    return list_tuple_to_radio_list(tuple_list)

def get_radio_jsr_db_info() -> list:
    tuple_list = get_all_from_jet_set_radio()
    return list_tuple_to_radio_jsr_list(tuple_list)

def find_speedrun_by_run_id(run_id:str) -> bool:
    connection = sqlite3.connect('speedrun.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(ID) FROM speedrun WHERE RunId == ?',(run_id,))
    id_count = cursor.fetchone()[0]
    connection.close()
    return id_count > 0

def find_radio_by_id(radio_id:str) -> bool:
    connection = sqlite3.connect('radio.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(ID) FROM radio WHERE ID == ?',(radio_id,))
    id_count = cursor.fetchone()[0]
    connection.close()
    return id_count > 0

def find_twitch_start_stream_by_id(streamer_id:str, start_time:str) -> bool:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(ID) FROM twitch WHERE ID == ? AND StartStream == ?',(streamer_id, start_time,))
    id_count = cursor.fetchone()[0]
    connection.close()
    return id_count > 0

def find_jet_set_radio_station(station:str) -> bool:
    connection = sqlite3.connect('jet_set_radio.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(ID) FROM jet_set_radio WHERE Station == ?',(station,))
    id_count = cursor.fetchone()[0]
    connection.close()
    return id_count > 0

def get_random_radio() -> Radio:
    radio: Radio = random.choice(get_radio_db_info())
    return radio

def get_random_radio_jsr() -> Radio_JSR:
    radio: Radio_JSR = random.choice(get_radio_jsr_db_info())
    return radio

def get_radios_by_country(country:str) -> list[Radio]:
    try:
        connection = sqlite3.connect('radio.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM radio WHERE LOWER(Country) == ?',(country.lower(),))
        tuple_list = cursor.fetchall()
        connection.close()
        return list_tuple_to_radio_list(tuple_list)

    except BaseException as e:
        print_message(message='Error while getting coutries from database',error=str(e),came_from='Sqlite')
        return []

def get_radios_jsr_by_station(station:str) -> list[Radio_JSR]:
    try:
        connection = sqlite3.connect('jet_set_radio.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM jet_set_radio WHERE LOWER(Station) == ?',(station.lower(),))
        radio_jsr_music = cursor.fetchall()
        
        connection.close()
        return list_tuple_to_radio_jsr_list(radio_jsr_music)

    except BaseException as e:
        print_message(message='Error while getting music from station database',error=str(e),came_from='Sqlite')
        return []

def get_stations_jsr() -> tuple[str]:
    try:
        connection = sqlite3.connect('jet_set_radio.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT Station FROM jet_set_radio')

        tuple_stations = cursor.fetchall()
        connection.close()

    except BaseException as e:
        print_message(message='Error while radio stations from database',error=str(e),came_from='Sqlite')
        tuple_stations = ()

    return tuple_stations

def get_all_from_radio() -> tuple:
    connection = sqlite3.connect('radio.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM radio')
    radios = cursor.fetchall()
    connection.close()
    
    return radios

def get_all_from_twitch() -> tuple:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM twitch')
    streams = cursor.fetchall()
    connection.close()
    
    return streams

def get_all_from_jet_set_radio() -> tuple:
    connection = sqlite3.connect('jet_set_radio.db')
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM jet_set_radio')
    radios = cursor.fetchall()
    connection.close()
    
    return radios

async def radio_sqlite_init() -> None:
    database_sqlite_init_from_script('radio')

    connection = sqlite3.connect('radio.db')
    cursor = connection.cursor()
    places:str = get('http://radio.garden/api/ara/content/places',allow_redirects=False).text
    json_places = json.loads(places)

    for place in json_places['data']['list']:      
        radios:str = get(f'http://radio.garden/api/ara/content/page/{place["id"]}/channels',allow_redirects=False).text
        json_radios = json.loads(radios)
        db_id_place = json_radios['data']['map']
        db_place_country = place['country']

        for data in json_radios['data']['content'][0]['items']:
            db_radio_id = str(data['page']['url']).split('/')[-1]
            db_title_place = data['page']['title']

            cursor.execute('INSERT OR REPLACE INTO radio VALUES(?, ?, ?, ?)', (db_radio_id, db_title_place,db_place_country,db_id_place))
            await asyncio.sleep(randint(1,3))
            connection.commit()
    connection.close()

async def speedrun_sqlite_init(games_ids:str) -> bool:
    try:
        database_sqlite_init_from_script('speedrun')
        
        games_ids_follow = games_ids.split(',')
        connection = sqlite3.connect('speedrun.db')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM speedrun")
        connection.commit()  

        for game_id in games_ids_follow:
            game_info:str = get(f'https://www.speedrun.com/api/v1/games/{game_id}',allow_redirects=False).text
            json_categories = json.loads(game_info)
            game_name = json_categories['data']['names']['international']

            categories:str = get(f'https://www.speedrun.com/api/v1/games/{game_id}/categories',allow_redirects=False).text
            json_categories = json.loads(categories)
            category_ids = []
            for category in json_categories['data']:
                if category['type'] == 'per-game':
                    category_ids.append(category['id'])

            for category_id in category_ids:
                runs:str = get(f'https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category_id}',allow_redirects=False).text
                json_runs = json.loads(runs)['data']['runs']

                category_info:str = get(f'https://www.speedrun.com/api/v1/categories/{category_id}',allow_redirects=False).text
                category_name = json.loads(category_info)['data']['name']

                for run in json_runs:
                    date = run['run']['date']
                    speedrun_link = run['run']['weblink']
                    id = run['run']['id']

                    cursor.execute('INSERT OR REPLACE INTO speedrun VALUES(?, ?, ?, ?, ?, ?, ?)', (None,game_id, id, speedrun_link,game_name,category_name,date))
                    connection.commit()      

        connection.close()
        return False
    except BaseException as e:
        await print_message_async(message='Could not init speedrun db',error=str(e),came_from='Sqlite')
        return False
