from processing.processCsv import preprocess_songs, select_songs
from utils import Configuration
import sqlite3
import os
from tqdm import tqdm

songs_table_name = 'songs'
lyrics_table_name = 'lyrics'
database_name = '../data/songs.sql'

Configuration.from_file('./config.cfg')
config = Configuration.get_config()
logger = Configuration.get_logger()

def create_tables():
    try:
        logger.info('Creating tables')
        try:
            os.remove(database_name)
        except:
            pass
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        sql = f"""create table if not exists {songs_table_name} (song_id integer PRIMARY KEY  , title TEXT, artist TEXT, raw_lyrics TEXT)"""
        logger.info(f'Executing {sql}')
        c.execute(sql)
        sql = f"""create table if not exists {lyrics_table_name} (song_id integer, word TEXT, FOREIGN KEY(song_id) REFERENCES {songs_table_name}(song_id))"""
        logger.info(f'Executing {sql}')
        c.execute(sql)
        conn.commit()
        logger.info('Tables created')
    finally:
        c.close()
        conn.close()


def lyrics_to_insert(i, song):
    for word in song.prepocessed_lyrics:
        yield (i, word)

def insert_data(data):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        i = 0
        for song in tqdm(data, unit=" songs"):
            c.execute(
                f"INSERT INTO {songs_table_name} ('song_id', 'title', 'artist', 'raw_lyrics') VALUES (?, ?, ?, ?)",
                (i, song.title, song.artist, song.raw_lyrics))
            c.executemany(f"INSERT INTO {lyrics_table_name} ('song_id', 'word')  VALUES (?, ?)",
                          lyrics_to_insert(i, song))
            i += 1
        conn.commit()
    finally:
        c.close()
        conn.close()


def prepare_dataset(rebuild_database, needs_selecting):
    logger.info('Preparing dataset')
    if needs_selecting:
        logger.info('Selecting songs')
        select_songs()
    if rebuild_database:
        create_tables()
        data = preprocess_songs()
        insert_data(data)


prepare_dataset(config.rebuild_database, config.select_songs)
