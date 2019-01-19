import logging
import csv
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

logging.basicConfig(filename='app.log', filemode='w', format='%(message)s', level=logging.INFO)

langs = {}
found_artists = {}
ignored_artists = {}
count = 10


def log_ignored_artist(record):
    logging.info(f'New ignored artist appeared = {record[3]}, the data is {record}')


def log_new_artist(record):
    logging.info(f'New artist appeared = {record[3]}')


def log_new_language(language):
    logging.info(f'New language appeared = {language}')

def preprocess(str):
    return str

def format_song(song):
    data = preprocess(song)
    return f'{song[0]},{song[1]},{song[2]},{song[3]},{song[4]},"{song[5]}"'



with open('../../data/processed-lyrics.csv', 'w', encoding="utf8") as output:
    with open('../../data/lyrics.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
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
                        log_new_language(detected)
                if to_add is not None:
                    count += 1
                    output.write(format_song(a))
            except LangDetectException:
                if a[3] not in ignored_artists:
                    ignored_artists[a[3]] = 1
                    log_ignored_artist(a)
                continue
            if i % 1000 == 1:
                print(i, 'done')
            i += 1
print('We have {} songs'.format(count))
