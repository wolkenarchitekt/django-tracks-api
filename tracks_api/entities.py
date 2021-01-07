import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class TrackEntity:
    artist: Optional[str]
    title: Optional[str]
    comment: Optional[str]
    album: Optional[str]
    bpm: Optional[int]
    key: Optional[str]
    file: Optional[str]
    duration: Optional[float]
    file_mtime: Optional[datetime.datetime]
    date_created = datetime.datetime
    date_updated = datetime.datetime
    bitrate = Optional[int]


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
