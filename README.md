# Dataset configuration
1. Download dataset from https://www.kaggle.com/gyani95/380000-lyrics-from-metrolyrics
1. Extract the dataset
1. Set the following configurations in `config.cfg` (you can change the paths as you wish)
    1. LyricsDatabase - this is a path where you should put your csv file
    1. SelectedLyrics - this is a path where all english songs will be saved
    1. Songs - this is a path where sql database will be placed

# Processing configuration
Since the processing and loading the dataset is a costly operation, two boolean values are provided to select whether the processing should be done.

* If `SelectSongs` is set to True, the preprocessing will generate a new csv file that contains all english songs
* If `RebuildDatabase` is set to True, the preprocessing script will generate a new database

After the script with both of them on, it is recommended to set those values to `False`

# Running songs processing
1. For pip run the following
```
python -m pip install -r requirements.txt
```
If you are using Conda
```
conda install --file requirements.txt
```

2. From main catalog run `python start-processing.py`. The processing should start

# Other
## Configuration class
In order to use some configurable values you might need to retrieve a config class.
```
from utils import Configuration
config = Configuration.get_config()
```
## Logging
You have an option to use a logger. The storage file for logs is being set in `LogFile` option in config file.
To use logger you just need to call
```
logger = config.get_logger()
logger.debug('This works')
```