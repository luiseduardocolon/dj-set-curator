"""
Enrich tracks with Camelot key notation
Takes tracks_dataset.json and adds Camelot keys
"""
import json
from camelot import to_camelot

def enrich_tracks_with_camelot(input_file='tracks_dataset.json', 
                                output_file='tracks_enriched.json'):
    """
    Add Camelot notation to all tracks in dataset
    """
    # Load original dataset
    with open(input_file, 'r') as f:
        tracks = json.load(f)
    
    print(f"Enriching {len(tracks)} tracks with Camelot notation...\n")
    
    # Add Camelot key to each track
    enriched = []
    for track in tracks:
        # Convert to Camelot
        camelot = to_camelot(track['key'], track['mode'])
        
        # Add Camelot field
        track['camelot'] = camelot
        
        print(f"✓ {track['track'][:30]:30} | "
              f"{track['key']} {track['mode']:6} → {camelot}")
        
        enriched.append(track)
    
    # Save enriched dataset
    with open(output_file, 'w') as f:
        json.dump(enriched, f, indent=2)
    
    print(f"\n✓ Saved enriched dataset to {output_file}")
    
    # Summary
    camelot_counts = {}
    for track in enriched:
        cam = track['camelot']
        camelot_counts[cam] = camelot_counts.get(cam, 0) + 1
    
    print("\n" + "=" * 70)
    print("CAMELOT DISTRIBUTION".center(70))
    print("=" * 70)
    
    for camelot in sorted(camelot_counts.keys()):
        count = camelot_counts[camelot]
        tracks_in_key = [t['track'] for t in enriched if t['camelot'] == camelot]
        print(f"{camelot}: {count} track(s) - {', '.join(tracks_in_key)}")
    
    return enriched

if __name__ == '__main__':
    tracks = enrich_tracks_with_camelot()
    
    print("\n" + "=" * 70)
    print("✓ Hour 2 Complete: Camelot enrichment done!".center(70))
    print("All tracks now have Camelot keys for harmonic mixing.".center(70))
    print("=" * 70)

