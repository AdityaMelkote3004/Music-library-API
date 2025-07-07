from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ✅ Association table for many-to-many Playlist ↔ Song
playlist_songs = Table(
    'playlist_songs',
    Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id'), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
)

# ✅ Song Model
class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'))

    album = relationship("Album", back_populates="songs")

    # ✅ Many-to-Many: Song ↔ Playlist
    playlists = relationship(
        "Playlist",
        secondary=playlist_songs,
        back_populates="songs"
    )

# ✅ Album Model
class Album(Base):
    __tablename__ = 'albums'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    
    songs = relationship("Song", back_populates="album")

# ✅ Playlist Model
class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # ✅ Many-to-Many: Playlist ↔ Song
    songs = relationship(
        "Song",
        secondary=playlist_songs,
        back_populates="playlists"
    )
