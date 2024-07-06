import json
import sqlite3

def sqlite_init() -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    #take id variable from api call
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Streamers (
    id INTEGER PRIMARY KEY, 
    query TEXT NOT NULL,
    streamer_link TEXT NOT NULL,
    start_stream TEXT )
    ''')

    connection.commit()
    cursor.execute('INSERT OR REPLACE INTO Streamers (id, query, streamer_link) VALUES (?, ?, ?)', ('37650924', 'chiblee', 'https://www.twitch.tv/chiblee'))
    cursor.execute('INSERT OR REPLACE INTO Streamers (id, query, streamer_link) VALUES (?, ?, ?)', ('35958947', 'squeex', 'https://www.twitch.tv/squeex'))
    cursor.execute('INSERT OR REPLACE INTO Streamers (id, query, streamer_link) VALUES (?, ?, ?)', ('14371185', 'northernlion', 'https://www.twitch.tv/northernlion'))
    connection.commit()
    connection.close()

def insert_stream_start_data(start_stream, id) -> None:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE Streamers SET start_stream = ? WHERE id = ?', (start_stream, id))
    connection.commit()
    connection.close()

def get_all_data_tuple() -> list[tuple]:
    connection = sqlite3.connect('twitch.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Streamers')
    queries = cursor.fetchall()
    connection.close()
    return queries