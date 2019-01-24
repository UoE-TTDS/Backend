import logging
import csv
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from .preprocessor import PreprocessorBuilder
from .Song import Song
from utils import Configuration
from tqdm import tqdm
from bigread import Reader

logging.basicConfig(filename='app.log', filemode='w', format='%(message)s', level=logging.INFO)

config = Configuration.get_config()
langs = {}
found_artists = {}
ignored_artists = {}
count = 10
logger = Configuration.get_logger()


def log_ignored_artist(record):
    logger.info(f'New ignored artist appeared = {record[3]}, the data is {record}')


def log_new_artist(record):
    logger.info(f'New artist appeared = {record[3]}')


def log_new_language(language):
    logger.info(f'New language appeared = {language}')


def format_song(song):
    lyrics = song[5].replace('\n', ' ').replace('"', '\\"')
    return f'{song[0]},{song[1]},{song[2]},{song[3]},{song[4]},"{lyrics}"\n'


def select_songs():
    print('Selecting songs began...')
    batch_size = 100
    with open(config.selected_lyrics_path, 'w', encoding="utf8") as output:

        #stream = Reader(file='config.lyrics_path', block_size=10)
        path = config.lyrics_path
        with open(path, 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            i = 0
            for row in tqdm(reader, unit=" songs"):
                a = row
                if a[5] == '' or a[3] in ignored_artists:
                    continue
                try:
                    to_add = None
                    if a[3] in found_artists:
                        to_add = a[5]
                    else:
                        detected = detect(a[5])
                        if detected == 'en':
                            found_artists[a[3]] = 1
                            log_new_artist(a)
                        elif detected not in langs:
                            langs[detected] = 1
                    if to_add is not None:
                        output.write(format_song(a))
                except LangDetectException:
                    if a[3] not in ignored_artists:
                        ignored_artists[a[3]] = 1
                    continue
                if i % 10000 == 1:
                    logger.info(f'{i} done')
                i += 1
    print('Selecting songs finished')


def preprocess_songs(songs_to_process):
    print('Preprocessing songs started')
    builder = PreprocessorBuilder()
    preprocessor = builder.to_lowercase().stop_words().smart_removal().remove_special().stem().smart_removal().build()
    with open(config.selected_lyrics_path, 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            d = preprocessor.preprocess(row[5])
            yield Song(row[1], row[3], row[5], d)
            i += 1
            if 0 < songs_to_process == i:
                break
    print('Preprocessing songs finished')
