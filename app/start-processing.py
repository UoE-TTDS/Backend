from processing.processCsv import preprocess_songs, select_songs

import sqlite3
import os

songs_table_name = 'songs'
lyrics_table_name = 'lyrics'
database_name = '../data/songs.sql'



def create_tables():
    try:
        print('Creating tables')
        try:
            os.remove(database_name)
        except:
            pass
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        sql = f"""create table if not exists {songs_table_name} (song_id integer PRIMARY KEY  , title TEXT, artist TEXT, raw_lyrics TEXT)"""
        print(f'Execute {sql}')
        c.execute(sql)
        sql = f"""create table if not exists {lyrics_table_name} (song_id integer, word TEXT, FOREIGN KEY(song_id) REFERENCES {songs_table_name}(song_id))"""
        print(f'Execute {sql}')
        c.execute(sql)
        conn.commit()
        print('Tables created')
    finally:
        c.close()
        conn.close()


def lyrics_to_insert(i, song):
    #print(list(song.prepocessed_lyrics))
    for word in song.prepocessed_lyrics:
        #print((i, word))
        yield (i, word)


def insert_data(data):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        i = 0
        for song in data:
            c.execute(
                f"INSERT INTO {songs_table_name} ('song_id', 'title', 'artist', 'raw_lyrics') VALUES (?, ?, ?, ?)",
                (i, song.title, song.artist, song.raw_lyrics))
            c.executemany(f"INSERT INTO {lyrics_table_name} ('song_id', 'word')  VALUES (?, ?)",
                          lyrics_to_insert(i, song))
            i += 1
            if i % 1000 == 0:
                print(f'inserted {i} songs')
        conn.commit()
    finally:
        c.close()
        conn.close()


def prepare_dataset(rebuild_database=True, needs_selecting=True):
    print('Preparing dataset')
    if needs_selecting:
        print('Selecting songs')
        select_songs()
    if rebuild_database:
        create_tables()
        data = preprocess_songs()
        insert_data(data)


def load_dataset():
    pass


prepare_dataset(True, False)
