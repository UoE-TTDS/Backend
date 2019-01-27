import sqlite3
import os
from tqdm import tqdm
from utils import Configuration

config = Configuration.get_config()
logger = Configuration.get_logger()
database_name = config.songs_path
songs_table_name = 'songs'
lyrics_table_name = 'lyrics'


class DatasetApi:

    @staticmethod
    def get_song_by_id(song_id):
        logger.info('Calling {getsongbyid}')
        conn = sqlite3.connect(config.songs_path)
        c = conn.cursor()
        query = f"SELECT title, artist, raw_lyrics from {songs_table_name} where song_id={song_id}"
        logger.info(f"executing {query}")
        c.execute(query)
        c.execute(query)
        data = c.fetchone()
        if data is None:
            return None
        return {
            'lyrics': data[2],
            'name': data[0],
            'artist': data[1]

        }

    @staticmethod
    def dump_lyrics(path):
        conn = sqlite3.connect(config.songs_path)
        c = conn.cursor()
        c.execute(f"SELECT COUNT(word) FROM {lyrics_table_name}")
        count = c.fetchone()[0]
        per_batch = 10000
        c.execute(f'SELECT word FROM {lyrics_table_name}')
        print(f'Dumping {count} words, {per_batch} per batch')
        with open(path, mode='w', encoding="utf8") as f:
            for batch in tqdm(iter(lambda: c.fetchmany(per_batch), []), unit=" batches", total=count//per_batch ):
                f.write(' '.join([b[0] for b in batch]))
        print('Dump done')

    @staticmethod
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

    @staticmethod
    def insert_data(data):
        try:
            conn = sqlite3.connect(config.songs_path)
            c = conn.cursor()
            i = 0
            for song in tqdm(data, unit=" songs"):
                c.execute(
                    f"INSERT INTO {songs_table_name} ('song_id', 'title', 'artist', 'raw_lyrics') VALUES (?, ?, ?, ?)",
                    (i, song.title, song.artist, song.raw_lyrics))
                c.executemany(f"INSERT INTO {lyrics_table_name} ('song_id', 'word')  VALUES (?, ?)",
                              DatasetApi.lyrics_to_insert(i, song))
                i += 1
            conn.commit()
        finally:
            c.close()
            conn.close()

    @staticmethod
    def lyrics_to_insert(i, song):
        for word in song.prepocessed_lyrics:
            yield (i, word)
