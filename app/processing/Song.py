from dataclasses import dataclass
from typing import List
@dataclass
class Song:
    title: str
    artist: str
    raw_lyrics: str
    prepocessed_lyrics: List[str]
