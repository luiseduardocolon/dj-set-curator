"""
Scoring Demo - Compare different track transitions
Shows how scoring helps choose better transitions
"""
import json
from scoring import total_compatibility, score_transition

def load_tracks():
    with open('tracks_enriched.json', 'r') as f:
        return json.load(f)

def demo_transitions():
    tracks = load_tracks()
    
    print("=" * 90)
    print("TRACK TRANSITION COMPARISON DEMO".center(90))
    print("=" * 90)
    
    # Pick a starting track
    start_track = tracks[0]  # September
    
    print(f"\nStarting track: {start_track['track']} by {start_track['artist']}")
    print(f"  Camelot: {start_track['camelot']}, BPM: {start_track['bpm']}, "
          f"Energy: {start_track['energy']:.2f}, Pop: {start_track['popularity']}")
    
    print("\n" + "=" * 90)
    print("COMPARING 3 POSSIBLE NEXT TRACKS".center(90))
    print("=" * 90)
    
    # Compare 3 potential next tracks
    candidates = [
        tracks[6],   # Dancing Queen (same Camelot)
        tracks[2],   # Uptown Funk (different Camelot)
        tracks[4],   # Don't Stop Me Now (high BPM jump)
    ]
    
    results = []
    
    for i, next_track in enumerate(candidates, 1):
        scores = total_compatibility(start_track, next_track, position_in_set=0.5)
        
        print(f"\n{i}. {next_track['track']} by {next_track['artist']}")
        print(f"   Camelot: {next_track['camelot']}, BPM: {next_track['bpm']}, "
              f"Energy: {next_track['energy']:.2f}, Pop: {next_track['popularity']}")
        print(f"   Scores:")
        print(f"     Harmonic:    {scores['harmonic']:.2f} "
              f"({start_track['camelot']} → {next_track['camelot']})")
        print(f"     BPM:         {scores['bpm']:.2f} "
              f"({start_track['bpm']:.1f} → {next_track['bpm']:.1f} BPM)")
        print(f"     Energy:      {scores['energy']:.2f} "
              f"({start_track['energy']:.2f} → {next_track['energy']:.2f})")
        print(f"     Popularity:  {scores['popularity']:.2f}")
        print(f"   → TOTAL: {scores['total']:.2f}/1.0")
        
        results.append((next_track, scores))
    
    # Rank by total score
    results.sort(key=lambda x: x[1]['total'], reverse=True)
    
    print("\n" + "=" * 90)
    print("RANKING (Best to Worst)".center(90))
    print("=" * 90)
    
    for rank, (track, scores) in enumerate(results, 1):
        print(f"{rank}. {track['track']:30} - Score: {scores['total']:.2f}/1.0")
    
    print("\n" + "=" * 90)
    print("RECOMMENDATION".center(90))
    print("=" * 90)
    
    best_track, best_scores = results[0]
    print(f"\n✓ BEST CHOICE: {best_track['track']} by {best_track['artist']}")
    print(f"  Total Score: {best_scores['total']:.2f}/1.0")
    print(f"\n  Why this works:")
    if best_scores['harmonic'] >= 0.8:
        print(f"  • Excellent harmonic compatibility ({start_track['camelot']} → {best_track['camelot']})")
    if best_scores['bpm'] >= 0.7:
        print(f"  • Smooth BPM transition ({abs(start_track['bpm'] - best_track['bpm']):.1f} BPM change)")
    if best_scores['energy'] >= 0.6:
        print(f"  • Good energy flow")
    if best_scores['popularity'] >= 0.6:
        print(f"  • Well-positioned crowd pleaser")

if __name__ == '__main__':
    demo_transitions()
    
    print("\n" + "=" * 90)
    print("✓ Hour 3 Complete: Scoring system working!".center(90))
    print("Next: Hour 4 will use this scoring to sequence the entire set".center(90))
    print("=" * 90)

