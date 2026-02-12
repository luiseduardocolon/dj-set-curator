"""
Track data loader - Hour 1 (Final)
Loads curated dataset with full audio features

After encountering API restrictions (Spotify lockdown, GetSongBPM
approval delays, AcousticBrainz limited coverage), we pivoted to
a curated dataset to focus on the core innovation: the harmonic
mixing algorithm and Temporal workflow orchestration.

Dataset includes 20 popular tracks with verified:
- BPM (tempo)
- Musical key + mode
- Energy level (0-1)
- Danceability (0-1)
- Popularity score (0-100)
"""
import json

def load_tracks(filepath='tracks_dataset.json'):
    """
    Load track data from JSON dataset
    
    Returns list of track dictionaries with:
    - track: Song title
    - artist: Artist name
    - bpm: Beats per minute
    - key: Musical key (C, D, E, F, G, A, B, with # for sharps)
    - mode: 'major' or 'minor'
    - energy: 0-1 scale
    - danceability: 0-1 scale
    - popularity: 0-100 scale
    - duration_ms: Track length in milliseconds
    """
    try:
        with open(filepath, 'r') as f:
            tracks = json.load(f)
        return tracks
    except FileNotFoundError:
        print(f"Error: {filepath} not found!")
        return []
    except json.JSONDecodeError:
        print(f"Error: {filepath} is not valid JSON!")
        return []

def print_track_table(tracks):
    """Print tracks in a formatted table"""
    print("\n" + "=" * 95)
    print("CURATED TRACK DATASET".center(95))
    print("=" * 95 + "\n")
    
    # Header
    print(f"{'#':<3} | {'Track':<25} | {'Artist':<20} | {'BPM':<6} | {'Key':<8} | {'Energy':<6} | {'Pop':<3}")
    print("-" * 95)
    
    # Rows
    for i, t in enumerate(tracks, 1):
        # Truncate long names
        name = t['track'][:24] if len(t['track']) > 24 else t['track']
        artist = t['artist'][:19] if len(t['artist']) > 19 else t['artist']
        key_str = f"{t['key']} {t['mode'][:3]}"  # e.g. "A maj"
        
        print(f"{i:<3} | {name:<25} | {artist:<20} | "
              f"{t['bpm']:<6.1f} | {key_str:<8} | "
              f"{t['energy']:<6.2f} | {t['popularity']:<3}")
    
    # Summary stats
    print("\n" + "=" * 95)
    print("SUMMARY STATISTICS".center(95))
    print("=" * 95)
    
    avg_bpm = sum(t['bpm'] for t in tracks) / len(tracks)
    avg_energy = sum(t['energy'] for t in tracks) / len(tracks)
    avg_dance = sum(t['danceability'] for t in tracks) / len(tracks)
    avg_pop = sum(t['popularity'] for t in tracks) / len(tracks)
    
    print(f"\nTotal tracks: {len(tracks)}")
    print(f"Average BPM: {avg_bpm:.1f}")
    print(f"Average Energy: {avg_energy:.2f}/1.0")
    print(f"Average Danceability: {avg_dance:.2f}/1.0")
    print(f"Average Popularity: {avg_pop:.1f}/100")
    
    # BPM range analysis
    min_bpm = min(t['bpm'] for t in tracks)
    max_bpm = max(t['bpm'] for t in tracks)
    print(f"\nBPM Range: {min_bpm:.0f} - {max_bpm:.0f} BPM")
    
    # Key distribution
    keys = {}
    for t in tracks:
        key_full = f"{t['key']} {t['mode']}"
        keys[key_full] = keys.get(key_full, 0) + 1
    
    print(f"\nKey distribution: {len(keys)} unique keys")
    
    # Highlight bangers
    bangers = [t for t in tracks if t['popularity'] >= 90]
    if bangers:
        print(f"\n🔥 High popularity tracks (90+):")
        for t in sorted(bangers, key=lambda x: x['popularity'], reverse=True):
            print(f"   - {t['track']} by {t['artist']} ({t['popularity']}/100)")

if __name__ == '__main__':
    tracks = load_tracks()
    
    if tracks:
        print_track_table(tracks)
        
        print("\n" + "=" * 95)
        print("✓ Hour 1 Complete: Dataset loaded successfully!".center(95))
        print("Dataset advantages:".center(95))
        print("- 100% data coverage (no API failures)".center(95))
        print("- Reproducible results".center(95))
        print("- Fast execution (no rate limiting)".center(95))
        print("- Focus on algorithm innovation".center(95))
        print("\nNext: Hour 2 - Camelot key conversion system".center(95))
        print("=" * 95)
    else:
        print("Failed to load dataset!")

