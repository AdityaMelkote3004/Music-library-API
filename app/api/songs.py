from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Playlist
from app.services.songs import (
    create_song,
    get_all_songs,
    get_song_by_id,
    update_song,
    create_playlist,
    get_all_playlists,
    add_song_to_playlist,
    delete_song,
    update_playlist,
    create_album,
    update_album,
    delete_album,
    get_all_albums,
    search_songs,
    search_playlists
)
from app.schemas import SongCreate, SongRead, PlaylistCreate, PlaylistRead,AlbumRead

router = APIRouter(prefix="/songs", tags=["Songs"])


# ✅ Static routes FIRST
@router.get("/playlists/", response_model=List[PlaylistRead])
def get_all_playlists_endpoint(db: Session = Depends(get_db)):
    return get_all_playlists(db=db)


@router.post("/playlists/", response_model=PlaylistRead, status_code=201)
def create_playlist_endpoint(name: str, db: Session = Depends(get_db)):
    return create_playlist(db=db, name=name)


@router.post("/", response_model=SongRead, status_code=201)
def create_song_endpoint(song: SongCreate, db: Session = Depends(get_db)):
    return create_song(db=db, **song.model_dump())


@router.get("/", response_model=List[SongRead])
def get_all_songs_endpoint(db: Session = Depends(get_db)):
    return get_all_songs(db=db)


@router.get("/{song_id}", response_model=SongRead)
def get_song_by_id_endpoint(song_id: int, db: Session = Depends(get_db)):
    song = get_song_by_id(db=db, song_id=song_id)
    if song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.put("/{song_id}", response_model=SongRead)
def update_song_endpoint(song_id: int, song: SongCreate, db: Session = Depends(get_db)):
    updated_song = update_song(db=db, song_id=song_id, **song.model_dump())
    if not updated_song:
        raise HTTPException(status_code=404, detail="Song not found")
    return updated_song


@router.delete("/{song_id}", status_code=204)
def delete_song_endpoint(song_id: int, db: Session = Depends(get_db)):
    success = delete_song(db=db, song_id=song_id)
    if not success:
        raise HTTPException(status_code=404, detail="Song not found")


@router.post("/{song_id}/playlists/{playlist_id}", response_model=PlaylistRead)
def add_song_to_playlist_endpoint(
    song_id: int, playlist_id: int, db: Session = Depends(get_db)
):
    result = add_song_to_playlist(db=db, song_id=song_id, playlist_id=playlist_id)
    if not result:
        raise HTTPException(status_code=404, detail="Song or playlist not found")
    return result

@router.post("/albums/", response_model=AlbumRead, status_code=201)
def create_album_endpoint(title: str, artist: str, db: Session = Depends(get_db)):
    return create_album(db=db, title=title, artist=artist)

@router.put("/albums/{album_id}", response_model=AlbumRead)
def update_album_endpoint(
    album_id: int, title: str, artist: str, db: Session = Depends(get_db)
):
    updated_album = update_album(db=db, album_id=album_id, title=title, artist=artist)
    if not updated_album:
        raise HTTPException(status_code=404, detail="Album not found")
    return updated_album

@router.delete("/albums/{album_id}", status_code=204)
def delete_album_endpoint(album_id: int, db: Session = Depends(get_db)):
    success = delete_album(db=db, album_id=album_id)
    if not success:
        raise HTTPException(status_code=404, detail="Album not found")


@router.get("/albums/", response_model=List[AlbumRead])
def get_all_albums_endpoint(db: Session = Depends(get_db)):
    return get_all_albums(db=db)


@router.get("/playlists/{playlist_id}/songs", response_model=List[SongRead])
def get_songs_in_playlist_endpoint(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist.songs


@router.get("/songs/search", response_model=list[SongRead])
def search_songs_endpoint(name: str = Query(..., description="Name of the song to search"), db: Session = Depends(get_db)):
    songs = search_songs(db=db, name=name)
    if not songs:
        raise HTTPException(status_code=404, detail="No songs found")
    return songs

@router.get("/playlists/search", response_model=list[PlaylistRead])
def search_playlists_endpoint(name: str = Query(..., description="Name of the playlist to search"), db: Session = Depends(get_db)):
    playlists = search_playlists(db=db, name=name)
    if not playlists:
        raise HTTPException(status_code=404, detail="No playlists found")
    return playlists






