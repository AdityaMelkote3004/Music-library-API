from pydantic import BaseModel
from typing import List


class SongBase(BaseModel):
    title: str
    artist: str
    album_id: int


class SongCreate(SongBase):
    pass


class SongRead(SongBase):
    id: int

    class Config:
        orm_mode = True


class PlaylistBase(BaseModel):
    name: str


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistRead(PlaylistBase):
    id: int
    songs: List[SongRead] = []

    class Config:
        orm_mode = True


class AlbumRead(BaseModel):
    id: int
    title: str
    artist: str

    class Config:
        orm_mode = True