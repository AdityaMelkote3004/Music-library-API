import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# Utility function to create a test album
def create_test_album():
    response = client.post("/songs/albums/?title=Test Album&artist=Test Artist")
    assert response.status_code == 201
    return response.json()["id"]

# Utility function to create a test playlist
def create_test_playlist():
    response = client.post("/songs/playlists/?name=Test Playlist")
    assert response.status_code == 201
    return response.json()["id"]

def test_create_song():
    album_id = create_test_album()
    response = client.post("/songs/", json={
        "title": "Test Song",
        "artist": "Test Artist",
        "album_id": album_id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Song"
    assert data["artist"] == "Test Artist"
    assert "id" in data

def test_get_song():
    album_id = create_test_album()
    create_resp = client.post("/songs/", json={
        "title": "Get Song",
        "artist": "Artist",
        "album_id": album_id
    })
    song_id = create_resp.json()["id"]
    response = client.get(f"/songs/{song_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Song"
    assert data["id"] == song_id

def test_update_song():
    album_id = create_test_album()
    create_resp = client.post("/songs/", json={
        "title": "Old Title",
        "artist": "Old Artist",
        "album_id": album_id
    })
    song_id = create_resp.json()["id"]
    response = client.put(f"/songs/{song_id}", json={
        "title": "New Title",
        "artist": "New Artist",
        "album_id": album_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["artist"] == "New Artist"

def test_delete_song():
    album_id = create_test_album()
    create_resp = client.post("/songs/", json={
        "title": "Delete Song",
        "artist": "Artist",
        "album_id": album_id
    })
    song_id = create_resp.json()["id"]
    response = client.delete(f"/songs/{song_id}")
    assert response.status_code == 204
    response = client.get(f"/songs/{song_id}")
    assert response.status_code == 404

def test_list_songs():
    album_id = create_test_album()
    client.post("/songs/", json={
        "title": "Song 1",
        "artist": "Artist 1",
        "album_id": album_id
    })
    client.post("/songs/", json={
        "title": "Song 2",
        "artist": "Artist 2",
        "album_id": album_id
    })
    response = client.get("/songs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_create_playlist():
    response = client.post("/songs/playlists/?name=New Playlist")
    assert response.status_code == 201
    assert "id" in response.json()

def test_add_song_to_playlist():
    album_id = create_test_album()
    song_resp = client.post("/songs/", json={
        "title": "Playlist Song",
        "artist": "Artist",
        "album_id": album_id
    })
    song_id = song_resp.json()["id"]
    playlist_id = create_test_playlist()
    response = client.post(f"/songs/{song_id}/playlists/{playlist_id}")
    assert response.status_code == 200

def test_get_songs_in_playlist():
    album_id = create_test_album()
    song_resp = client.post("/songs/", json={
        "title": "List Playlist Song",
        "artist": "Artist",
        "album_id": album_id
    })
    song_id = song_resp.json()["id"]
    playlist_id = create_test_playlist()
    client.post(f"/songs/{song_id}/playlists/{playlist_id}")
    response = client.get(f"/songs/playlists/{playlist_id}/songs")
    assert response.status_code == 200
    songs = response.json()
    assert any(song["id"] == song_id for song in songs)

def test_get_all_playlists():
    # Create a few playlists
    client.post("/songs/playlists/?name=Playlist 1")
    client.post("/songs/playlists/?name=Playlist 2")
    
    response = client.get("/songs/playlists/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_create_album():
    response = client.post("/songs/albums/?title=Test Album Create&artist=Test Artist Create")
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Album Create"
    assert data["artist"] == "Test Artist Create"
    assert "id" in data

def test_get_all_albums():
    # Create a few albums
    client.post("/songs/albums/?title=Album 1&artist=Artist 1")
    client.post("/songs/albums/?title=Album 2&artist=Artist 2")
    
    response = client.get("/songs/albums/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_update_album():
    # Create an album first
    create_resp = client.post("/songs/albums/?title=Old Album Title&artist=Old Artist")
    album_id = create_resp.json()["id"]
    
    # Update the album
    response = client.put(f"/songs/albums/{album_id}?title=New Album Title&artist=New Artist")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Album Title"
    assert data["artist"] == "New Artist"

def test_delete_album():
    # Create an album first
    create_resp = client.post("/songs/albums/?title=Delete Album&artist=Delete Artist")
    album_id = create_resp.json()["id"]
    
    # Delete the album
    response = client.delete(f"/songs/albums/{album_id}")
    assert response.status_code == 204

def test_song_not_found():
    # Test getting a non-existent song
    response = client.get("/songs/99999")
    assert response.status_code == 404

def test_playlist_not_found():
    # Test getting songs from a non-existent playlist
    response = client.get("/songs/playlists/99999/songs")
    assert response.status_code == 404

def test_add_nonexistent_song_to_playlist():
    # Create a playlist
    playlist_id = create_test_playlist()
    
    # Try to add a non-existent song
    response = client.post(f"/songs/99999/playlists/{playlist_id}")
    assert response.status_code == 404  # Should return 404 for non-existent songs

def test_add_song_to_nonexistent_playlist():
    # Create a song
    album_id = create_test_album()
    song_resp = client.post("/songs/", json={
        "title": "Test Song",
        "artist": "Test Artist",
        "album_id": album_id
    })
    song_id = song_resp.json()["id"]
    
    # Try to add to non-existent playlist
    response = client.post(f"/songs/{song_id}/playlists/99999")
    assert response.status_code == 404  # Should return 404 for non-existent playlists

def test_update_nonexistent_song():
    # Try to update a non-existent song
    response = client.put("/songs/99999", json={
        "title": "New Title",
        "artist": "New Artist", 
        "album_id": 1
    })
    assert response.status_code == 404  # Should return 404 for non-existent songs

def test_delete_nonexistent_song():
    # Try to delete a non-existent song
    response = client.delete("/songs/99999")
    assert response.status_code == 404  # Should return 404 for non-existent songs
