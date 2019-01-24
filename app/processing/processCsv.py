import logging
import csv
import queue
from queue import Empty
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from .preprocessor import PreprocessorBuilder
from .Song import Song
from utils import Configuration
from tqdm import tqdm
from bigread import Reader
from threading import Thread
import asyncio

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


def solve(q, out):
    while True:
        if q.empty():
            break
        try:
            item = q.get_nowait()
            d = detect(item[5])
            if d == 'en':
                out.put(format_song(item))
        except LangDetectException:
            pass
        except Empty:
            break


def select_songs():
    print('Selecting songs began...')
    batch_size = 1000
    with open(config.selected_lyrics_path, 'w', encoding="utf8") as output:
        path = config.lyrics_path
        with open(path, 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            i = 0
            q = queue.Queue(batch_size)
            out = queue.Queue(batch_size)
            for row in tqdm(reader, unit=" songs"):
                if i < batch_size:
                    q.put(row)
                    i += 1
                else:  # batch gathered, create threads and solve
                    threads = []
                    for _ in range(2):
                        t = Thread(target=solve, args=(q, out))
                        threads.append(t)
                        t.start()
                    for t in threads:
                        t.join()

                    while True:
                        if out.empty():
                            break
                        item = out.get_nowait()
                        output.write(item)

                    q = queue.Queue(batch_size)
                    out = queue.Queue(batch_size)
                    i = 0
    print('Selecting songs finished')


def preprocess_songs(songs_to_process):
    print('Preprocessing songs started')
    builder = PreprocessorBuilder()
    preprocessor = builder. \
        to_lowercase(). \
        stop_words(). \
        number_removal(). \
        smart_removal(). \
        remove_special(). \
        stem(). \
        build()
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
