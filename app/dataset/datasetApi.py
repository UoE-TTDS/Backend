import sqlite3
from tqdm import tqdm
from utils import Configuration, SqlClient, TableObj

config = Configuration.get_config()
logger = Configuration.get_logger()

songs_table_name = 'songs'
lyrics_table_name = 'lyrics'
popularity_table_name = 'popularity'


class DatasetApi:

    @staticmethod
    def get_song_by_id(song_id):
        logger.info('Calling {getsongbyid}')
        conn = sqlite3.connect(config.songs_path)
        c = conn.cursor()
        query = f"SELECT title, artist, raw_lyrics from {songs_table_name} where song_id={song_id}"
        logger.info(f"executing {query}")
        c.execute(query)
        data = c.fetchone()
        if data is None:
            return None
        return {
            'lyrics': data[2],
            'name': data[0],
            'artist': data[1]
        }

    def get_songs_by_id(self, ids):
        logger.info('Calling {getsongbyid}')
        conn = sqlite3.connect(config.songs_path)
        c = conn.cursor()
        ids = ','.join([str(id) for id in ids])
        query = f"SELECT title, artist, raw_lyrics, song_id from {songs_table_name} where song_id IN ({ids})"
        logger.info(f"executing {query}")
        c.execute(query)
        data = c.fetchall()
        if data is None:
            return None
        for d in data:
            yield {
                'lyrics': d[2],
                'name': d[0],
                'artist': d[1],
                'id': d[3]
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
            for batch in tqdm(iter(lambda: c.fetchmany(per_batch), []), unit=" batches", total=count // per_batch):
                f.write(' '.join([b[0] for b in batch]))
        print('Dump done')

    @staticmethod
    def get_table_definitions():

        keys_to_songs = {
            'song_id': (songs_table_name, 'song_id')
        }
        # Songs
        columns = {
            'song_id': 'INTEGER PRIMARY KEY',
            'title': 'TEXT',
            'artist': 'TEXT',
            'raw_lyrics': 'TEXT'
        }
        songs = TableObj(songs_table_name, columns)

        # Lyrics
        columns = {
            'song_id': 'INTEGER',
            'word': 'TEXT'
        }
        lyrics = TableObj(lyrics_table_name, columns, keys_to_songs)

        # Lyrics
        columns = {
            'song_id': 'INTEGER',
            'counter': 'INTEGER',
            'last_searched': 'TEXT'
        }

        popularity = TableObj(popularity_table_name, columns, keys_to_songs)

        return [songs, lyrics, popularity]

    @staticmethod
    def create_tables():
        logger.info('Creating tables')

        tables = DatasetApi.get_table_definitions()

        with SqlClient() as client:
            for table in tables:
                client.create_table(table)
        logger.info('Tables created')

    @staticmethod
    def clear_database():
        with SqlClient() as client:
            client.clear_database()

    @staticmethod
    def insert_data(data):
        try:
            conn = sqlite3.connect(config.songs_path)
            c = conn.cursor()
            c.execute(f'DELETE FROM {songs_table_name}')
            c.execute(f'DELETE FROM {lyrics_table_name}')
            i = 1
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
