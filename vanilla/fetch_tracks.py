"""
Track data loader - Hours 1-2 Complete
Loads enriched dataset with Camelot notation
"""
import json

def load_tracks(filepath='tracks_enriched.json'):
    """
    Load enriched track data with Camelot keys
    
    Returns list of track dictionaries with:
    - track, artist, bpm, key, mode
    - energy, danceability, popularity
    - camelot: Camelot wheel notation (e.g., '8A', '5B')
    """
    try:
        with open(filepath, 'r') as f:
            tracks = json.load(f)
        return tracks
    except FileNotFoundError:
        print(f"Error: {filepath} not found!")
        return []

def print_track_table(tracks):
    """Print tracks with Camelot notation"""
    print("\n" + "=" * 100)
    print("TRACK DATASET WITH CAMELOT KEYS".center(100))
    print("=" * 100 + "\n")
    
    # Header
    print(f"{'#':<3} | {'Track':<30} | {'Artist':<20} | {'BPM':<6} | "
          f"{'Camelot':<7} | {'Energy':<6} | {'Pop':<3}")
    print("-" * 100)
    
    # Rows
    for i, t in enumerate(tracks, 1):
        name = t['track'][:29] if len(t['track']) > 29 else t['track']
        artist = t['artist'][:19] if len(t['artist']) > 19 else t['artist']
        
        print(f"{i:<3} | {name:<30} | {artist:<20} | "
              f"{t['bpm']:<6.1f} | {t['camelot']:<7} | "
              f"{t['energy']:<6.2f} | {t['popularity']:<3}")
    
    # Summary
    print("\n" + "=" * 100)
    print("SUMMARY".center(100))
    print("=" * 100)
    
    print(f"\nTotal tracks: {len(tracks)}")
    print(f"Average BPM: {sum(t['bpm'] for t in tracks) / len(tracks):.1f}")
    print(f"Average Energy: {sum(t['energy'] for t in tracks) / len(tracks):.2f}/1.0")
    
    # Camelot distribution
    camelot_keys = set(t['camelot'] for t in tracks)
    print(f"Unique Camelot keys: {len(camelot_keys)}")
    print(f"Keys present: {', '.join(sorted(camelot_keys))}")

if __name__ == '__main__':
    tracks = load_tracks()
    
    if tracks:
        print_track_table(tracks)
        
        print("\n" + "=" * 100)
        print("✓ Hours 1-2 Complete!".center(100))
        print("Dataset ready for harmonic mixing algorithm.".center(100))
        print("\nNext: Hour 3 - Compatibility scoring system".center(100))
        print("=" * 100)

