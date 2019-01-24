from processing.processCsv import preprocess_songs, select_songs
from utils import Configuration
import sqlite3
import os
from tqdm import tqdm
from dataset import DatasetApi

config = Configuration.get_config()
logger = Configuration.get_logger()


def prepare_dataset(rebuild_database, needs_selecting):
    logger.info('Preparing dataset')
    if needs_selecting:
        logger.info('Selecting songs')
        select_songs()
    if rebuild_database:
        DatasetApi.create_tables()
        songs_to_process = Configuration.songs_to_process
        print(f'Will process {songs_to_process} songs')
        data = preprocess_songs(songs_to_process)
        DatasetApi.insert_data(data)


prepare_dataset(config.rebuild_database, config.select_songs)

if config.should_dump_lyrics:
    logger.info(f'Dumping lyrics to a {config.lyrics_dump_path}')
    api = DatasetApi.dump_lyrics(config.lyrics_dump_path)
