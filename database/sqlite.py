import asyncio
import json
import os
from random import randint
import random
import sqlite3
import pandas as pd
from requests import get

from database.models.radio import Radio, list_tuple_to_radio_list
from database.models.radio_jsr import Radio_JSR, list_tuple_to_radio_jsr_list
from database.models.speedrun import Speedrun
from database.models.streamer import Streamer, list_tuple_to_streamer_list
from logger import print_message

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

def insert_stream_start_data(start_stream, id) -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE twitch SET start_stream = ? WHERE id = ?',(start_stream, id))
    connection.commit()
    connection.close()

def get_twitch_db_streamers() -> list:
    tuple_list = _get_all_from_table('twitch')
    return list_tuple_to_streamer_list(tuple_list)

def get_radio_db_info() -> list:
    tuple_list = _get_all_from_table('radio')
    return list_tuple_to_radio_list(tuple_list)

def get_radio_jsr_db_info() -> list:
    tuple_list = _get_all_from_table('jet_set_radio')
    return list_tuple_to_radio_jsr_list(tuple_list)

def find_twitch_start_stream_by_id(streamer_id:str, start_time:str) -> bool:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(ID) FROM twitch WHERE ID == ? AND start_stream == ?',(streamer_id, start_time,))
    id_count = cursor.fetchone()[0]
    connection.close()
    return id_count > 0

def does_record_db_exist(record_id:str, database_name:str, where_field:str)-> bool:
    connection = sqlite3.connect(f'{database_name}.db')
    cursor = connection.cursor()

    cursor.execute(f'SELECT COUNT(ID) FROM {database_name} WHERE {where_field} == ?',(record_id,))
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
        tuple_list = _get_all_from_table(db='radio', where='LOWER(Country) =='+str.lower("'"+country+"'"))
    except BaseException as e:
        print_message('Error while getting coutries from database',e)
    return list_tuple_to_radio_list(tuple_list)

def get_radios_jsr_by_station(station:str) -> list[Radio_JSR]:
    try:
        radio_jsr_music = _get_all_from_table(db='jet_set_radio', where='LOWER(Station) =='+str.lower("'"+station+"'"))
    except BaseException as e:
        print_message('Error while getting music from station database',e)
    return list_tuple_to_radio_jsr_list(radio_jsr_music)

def get_stations_jsr() -> tuple[str]:
    try:
        connection = sqlite3.connect('jet_set_radio.db')
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT Station FROM jet_set_radio')

        tuple_stations = cursor.fetchall()
        connection.close()

    except BaseException as e:
        print_message('Error while radio stations from database',e)
        tuple_stations = ()
    return tuple_stations

#use this method only in this file
def _get_all_from_table(db, where = '') -> list:
    connection = sqlite3.connect(db+'.db')
    cursor = connection.cursor()

    if where == '':
        cursor.execute('SELECT * FROM ' + db)
    else:
        cursor.execute('SELECT * FROM ' + db + ' WHERE ' + where)

    tuple_list = cursor.fetchall()
    connection.close()
    return tuple_list

async def radio_sqlite_init() -> None:
    connection = sqlite3.connect('radio.db')
    cursor = connection.cursor()
    places:str = get('http://radio.garden/api/ara/content/places').text
    json_places = json.loads(places)

    for place in json_places['data']['list']:      
        radios:str = get(f'http://radio.garden/api/ara/content/page/{place["id"]}/channels').text
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

async def database_sqlite_init_speedrun(games_ids:str):
    games_ids_follow = games_ids.split(',')
    connection = sqlite3.connect('speedrun.db')
    cursor = connection.cursor()
    cursor.execute("DELETE * FROM speedrun")

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
                date = run['run']['date']
                speedrun_link = run['run']['weblink']
                id = run['run']['id']

                cursor.execute('INSERT OR REPLACE INTO speedrun VALUES(?, ?, ?, ?, ?, ?, ?)', (None,game_id, id, speedrun_link,game_name,category_name,date))
                connection.commit()      

    connection.close()
    return True    
