import asyncio
import json
from random import randint
import random
import sqlite3
import pandas as pd
from requests import get

from database.radio import Radio, list_tuple_to_radio_list
from database.streamer import list_tuple_to_streamer_list

def twitch_sqlite_init() -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    with open('./database/twitch.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    cursor.executescript(sql_script)
    connection.commit()
    connection.close()
    

def insert_stream_start_data(start_stream, id) -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE Streamers SET start_stream = ? WHERE id = ?', (start_stream, id))
    connection.commit()
    connection.close()

def get_twitch_db_streamers() -> list:
    tuple_list = get_all_from_table('twitch')
    return list_tuple_to_streamer_list(tuple_list)

def get_radio_db_info() -> list:
    tuple_list = get_all_from_table('radio')
    return list_tuple_to_radio_list(tuple_list)

def does_radio_db_exist(radio_id:str) -> bool:
    connection = sqlite3.connect('radio.db')
    cursor = connection.cursor()

    radios = cursor.execute('SELECT * FROM radio WHERE ID == ?',radio_id)
    connection.close()
    return len(radios) > 0

def get_random_radio() -> Radio:
    radio: Radio = random.choice(get_radio_db_info())
    return radio

#use this method only in this file
def get_radios_by_country(country:str) -> list[Radio]:
    try:
        tuple_list = get_all_from_table(db='radio', where='LOWER(Country) =='+str.lower("'"+country+"'"))
    except BaseException as e:
        print(e)
    return list_tuple_to_radio_list(tuple_list)

#use this method only in this file
def get_all_from_table(db, where = ''):
    connection = sqlite3.connect(db+'.db')
    cursor = connection.cursor()

    if where == '':
        cursor.execute('SELECT * FROM ' + db)
    else:
        print(where)
        cursor.execute('SELECT * FROM ' + db + ' WHERE ' + where)

    tuple_list = cursor.fetchall()
    connection.close()
    return tuple_list

async def radio_sqlite_init():
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
            print(db_title_place, db_place_country)
            cursor.execute('INSERT OR REPLACE INTO radio VALUES(?, ?, ?, ?)', (db_radio_id, db_title_place,db_place_country,db_id_place))
            await asyncio.sleep(randint(2,4))
            connection.commit()
    connection.close()