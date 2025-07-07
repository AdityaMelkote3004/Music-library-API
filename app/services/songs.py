from sqlalchemy.orm import Session, joinedload
from app.models import Song, Playlist , Album


def create_song(db: Session, title: str, artist: str, album_id: int):
    db_song = Song(title=title, artist=artist, album_id=album_id)
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song


def get_all_songs(db: Session):
    return db.query(Song).all()


def get_song_by_id(db: Session, song_id: int):
    return db.query(Song).filter(Song.id == song_id).first()


def update_song(db: Session, song_id: int, title: str, artist: str, album_id: int):
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        return None
    
    song.title = title
    song.artist = artist
    song.album_id = album_id
    db.commit()
    db.refresh(song)
    return song


def create_playlist(db: Session, name: str):
    db_playlist = Playlist(name=name)
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def get_all_playlists(db: Session):
    return db.query(Playlist).options(joinedload(Playlist.songs)).all()


def add_song_to_playlist(db: Session, song_id: int, playlist_id: int):
    song = db.query(Song).filter(Song.id == song_id).first()
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()

    if not song or not playlist:
        return None

    playlist.songs.append(song)
    db.commit()
    db.refresh(playlist)
    return playlist


def delete_song(db: Session, song_id: int):
    song = db.query(Song).filter(Song.id == song_id).first()
    if song:
        db.delete(song)
        db.commit()
        return True
    return False


def update_playlist(db: Session, playlist_id: int, new_name: str):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        return None

    playlist.name = new_name
    db.commit()
    db.refresh(playlist)
    return playlist

def create_album(db: Session , title: str, artist: str):
    db_album = Album(title=title, artist=artist)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album

def update_album(db: Session, album_id: int, title: str, artist: str):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        return None

    album.title = title
    album.artist = artist
    db.commit()
    db.refresh(album)
    return album

def delete_album(db: Session, album_id: int):
    album = db.query(Album).filter(Album.id == album_id).first()
    if album:
        db.delete(album)
        db.commit()
        return True
    return False

def get_all_albums(db: Session):
    return db.query(Album).all()

