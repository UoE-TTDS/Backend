import logging
import csv
import queue
from queue import Empty
import fastText
from .preprocessor import PreprocessorBuilder
from .Song import Song
from utils import Configuration
from tqdm import tqdm
from threading import Thread

logging.basicConfig(filename='app.log', filemode='w', format='%(message)s', level=logging.INFO)

config = Configuration.get_config()
lang = fastText.load_model(config.lang_path)
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
    lyrics = song[5].replace('"',"'")
    return f'{song[0]},{song[1]},{song[2]},{song[3]},{song[4]},"{lyrics}"\n'


def solve(q, out):
    while True:
        if q.empty():
            break
        try:
            item = q.get_nowait()
            if len(item[5]) != 0:
                d = lang.predict(item[5].replace('\n', ' '))[0][0]
                if d == '__label__en':
                    out.put(format_song(item))
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
    preprocessor = builder.build()# \
     #   stop_words(). \
      #  stem(). \
        #build()
    with open(config.selected_lyrics_path, 'r', encoding="utf8") as f,\
        open('./all_songs.txt', 'w', encoding='UTF-8') as songs_file:
        reader = csv.reader(f)
        next(reader) # need to skip the header from csv file
        i = 0
        for row in reader:
            d = preprocessor.preprocess(row[5])
            songs_file.write(' '.join(d)+'\n')
            yield Song(row[1], row[3], row[5], d)
            i += 1
            if 0 < songs_to_process == i:
                break
    print('Preprocessing songs finished')
