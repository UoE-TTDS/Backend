import configparser
import os
import logging


class Configuration:
    config = None

    def __init__(self):
        self.__songs_path = ''
        self.__selected_lyrics_path = ''
        self.__lyrics_path = ''
        self.__rebuild_database = None
        self.__select_songs = None
        self.__lyrics_dump_path = ''
        self.__should_dump_lyrics = None
        self.__songs_to_process = 0

    @staticmethod
    def configure_logging(logFile):
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
        handler = logging.FileHandler(logFile)
        handler.setFormatter(formatter)
        logger = logging.getLogger('main')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    @staticmethod
    def from_file(path):
        print('Reading configuration')
        config = configparser.ConfigParser()
        config.read(path)
        if not config.sections():
            print(f'Config was not loaded correctly!! Check the path: {path}, currently reading from {os.getcwd()}')
        print(f'Config was loaded correctly from path {path}')
        paths = config['Paths']
        datasetProcessing = config['DatasetProcessing']
        Configuration.configure_logging(paths['LogFile'])
        logger = Configuration.get_logger()
        logger.info('Logger opened')
        logger.info('Reading paths')

        c = Configuration()
        c.__songs_path = paths['Songs']
        c.__selected_lyrics_path = paths['SelectedLyrics']
        c.__lyrics_path = paths['LyricsDatabase']
        c.__lyrics_dump_path = paths['LyricsDumpPath']
        c.__lang_path = paths['LangModelPath']
        c.__songs_to_process = datasetProcessing.getint('SongsToProcess')
        c.__rebuild_database = datasetProcessing.getboolean('RebuildDatabase')
        c.__select_songs = datasetProcessing.getboolean('SelectSongs')
        c.__should_dump_lyrics = datasetProcessing.getboolean('ShouldDumpLyrics')
        logger.info('All paths read\nPrinting')
        logger.info(
            f'LyricsDatabase = {c.lyrics_path},\nSelectedLyrics = {c.selected_lyrics_path},\nSongsPath = {c.songs_path}')
        Configuration.config = c
        return c

    @staticmethod
    def get_config() -> 'Configuration':
        if Configuration.config is None:
            Configuration.from_file('./config.cfg')
        return Configuration.config

    @staticmethod
    def get_logger():
        return logging.getLogger('main')

    @property
    def songs_path(self):
        return self.__songs_path

    @property
    def lang_path(self):
        return self.__lang_path

    @property
    def selected_lyrics_path(self):
        return self.__selected_lyrics_path

    @property
    def lyrics_path(self):
        return self.__lyrics_path

    @property
    def rebuild_database(self):
        return self.__rebuild_database

    @property
    def select_songs(self):
        return self.__select_songs

    @property
    def lyrics_dump_path(self):
        return self.__lyrics_dump_path

    @property
    def should_dump_lyrics(self):
        return self.__should_dump_lyrics

    @property
    def songs_to_process(self):
        return self.__songs_to_process
