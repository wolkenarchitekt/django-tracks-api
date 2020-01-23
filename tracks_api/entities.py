import datetime
from dataclasses import dataclass


@dataclass
class TrackEntity:
    artist: str
    title: str
    comment: str
    album: str
    bpm: int
    key: str
    file: str
    duration: float
    file_mtime: datetime.datetime
    date_created = datetime.datetime
    date_updated = datetime.datetime
    bitrate = int


@dataclass
class TrackRatingEntity:
    track = TrackEntity
    email = str
    rating: int
    count: int


@dataclass
class TrackImageEntity:
    track: TrackEntity
    image: object
    desc: str
