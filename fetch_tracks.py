"""
Spotify playlist fetcher - First milestone
Demonstrates basic API authentication and data retrieval
"""
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

def fetch_playlist_tracks(playlist_url):
    """Fetch track names from Spotify playlist"""
    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    ))
    
    # Extract playlist ID from URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]
    
    # Fetch playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    
    for item in results['items']:
        track = item['track']
        if track:  # Skip None tracks (removed/unavailable)
            tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'id': track['id']
            })
    
    return tracks

if __name__ == '__main__':
    # Using my "Lovejoy2026" playlist - globally accessible
    PLAYLIST_URL = "https://open.spotify.com/playlist/3ruQYIEimENbrj6Pa6XZfe?si=rt-bEAEXR9Wr_ER35i40_Q"
    
    tracks = fetch_playlist_tracks(PLAYLIST_URL)
    
    print("=== FETCHED TRACKS ===")
    for i, track in enumerate(tracks, 1):
        print(f"{i}. {track['name']} - {track['artist']}")
    
    print(f"\nTotal tracks: {len(tracks)}")

