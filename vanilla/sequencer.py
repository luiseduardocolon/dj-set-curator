"""
Greedy Track Sequencing Algorithm
Builds optimal DJ sets using multi-factor compatibility scoring

Algorithm:
1. Start with highest-popularity track
2. At each step, pick the best-scoring unplayed track
3. Consider position in set for popularity weighting
4. Continue until all tracks are sequenced

This is a "greedy" algorithm - it makes the locally optimal
choice at each step, which produces good (but not perfect) results.
"""

import json
from scoring import total_compatibility

def sequence_tracks_greedy(tracks, start_track_idx=None):
    """
    Sequence tracks using greedy algorithm with multi-factor scoring
    
    Args:
        tracks: List of track dicts (must have camelot, bpm, energy, popularity)
        start_track_idx: Optional index to force as starting track
                        (default: highest popularity track)
    
    Returns:
        List of tracks in optimal sequence
    """
    if not tracks:
        return []
    
    # Make a copy so we don't modify original
    remaining = tracks.copy()
    sequence = []
    
    # Step 1: Pick starting track
    if start_track_idx is not None:
        # Use specified track
        current = remaining.pop(start_track_idx)
    else:
        # Start with highest popularity track (crowd-pleaser opener)
        remaining.sort(key=lambda t: t['popularity'], reverse=True)
        current = remaining.pop(0)
    
    sequence.append(current)
    
    # Step 2: Greedily add remaining tracks
    while remaining:
        # Calculate position in set (0.0 = start, 1.0 = end)
        position = len(sequence) / (len(tracks) - 1) if len(tracks) > 1 else 0.5
        
        # Score all remaining tracks against current track
        scores = []
        for i, candidate in enumerate(remaining):
            score = total_compatibility(current, candidate, position)
            scores.append((i, candidate, score))
        
        # Pick the highest-scoring track
        scores.sort(key=lambda x: x[2]['total'], reverse=True)
        best_idx, best_track, best_score = scores[0]
        
        # Add to sequence
        sequence.append(best_track)
        remaining.pop(best_idx)
        
        # This becomes the new current track
        current = best_track
    
    return sequence

def sequence_tracks_bpm_only(tracks):
    """
    Simple BPM-only sequencing for comparison
    Just sorts tracks by ascending BPM
    """
    sorted_tracks = sorted(tracks, key=lambda t: t['bpm'])
    return sorted_tracks

def analyze_sequence(sequence):
    """
    Analyze a track sequence and return metrics
    
    Returns dict with:
    - total_duration: Total set duration in minutes
    - avg_transition_score: Average compatibility between consecutive tracks
    - harmonic_violations: Count of incompatible key changes
    - bpm_range: Min to max BPM
    - energy_progression: Description of energy arc
    """
    from scoring import total_compatibility, are_compatible
    
    if len(sequence) < 2:
        return {
            'total_duration': sum(t['duration_ms'] for t in sequence) / 60000,
            'avg_transition_score': 0,
            'harmonic_violations': 0,
            'bpm_range': (sequence[0]['bpm'], sequence[0]['bpm']),
            'energy_progression': 'N/A'
        }
    
    # Calculate metrics
    total_duration = sum(t['duration_ms'] for t in sequence) / 60000  # minutes
    
    transition_scores = []
    harmonic_violations = 0
    
    for i in range(len(sequence) - 1):
        position = i / (len(sequence) - 1)
        scores = total_compatibility(sequence[i], sequence[i+1], position)
        transition_scores.append(scores['total'])
        
        # Check for harmonic violation
        compatible, _ = are_compatible(sequence[i]['camelot'], sequence[i+1]['camelot'])
        if not compatible:
            harmonic_violations += 1
    
    avg_score = sum(transition_scores) / len(transition_scores)
    
    bpms = [t['bpm'] for t in sequence]
    bpm_range = (min(bpms), max(bpms))
    
    # Energy progression analysis
    energies = [t['energy'] for t in sequence]
    first_third_avg = sum(energies[:len(energies)//3]) / max(1, len(energies)//3)
    middle_third_avg = sum(energies[len(energies)//3:2*len(energies)//3]) / max(1, len(energies)//3)
    last_third_avg = sum(energies[2*len(energies)//3:]) / max(1, len(energies) - 2*len(energies)//3)
    
    if middle_third_avg > first_third_avg and middle_third_avg > last_third_avg:
        energy_progression = "Peak in middle (ideal DJ arc)"
    elif last_third_avg > first_third_avg:
        energy_progression = "Building to climax"
    elif first_third_avg > last_third_avg:
        energy_progression = "Cool-down ending"
    else:
        energy_progression = "Flat energy"
    
    return {
        'total_duration': total_duration,
        'avg_transition_score': avg_score,
        'harmonic_violations': harmonic_violations,
        'bpm_range': bpm_range,
        'energy_progression': energy_progression
    }

def print_sequence(sequence, title="DJ SET SEQUENCE"):
    """
    Print a formatted sequence with analysis
    """
    print("\n" + "=" * 100)
    print(title.center(100))
    print("=" * 100 + "\n")
    
    # Header
    print(f"{'#':<3} | {'Track':<30} | {'Artist':<20} | {'BPM':<6} | {'Camelot':<7} | {'Energy':<6} | {'Pop':<3}")
    print("-" * 100)
    
    # Tracks
    for i, t in enumerate(sequence, 1):
        name = t['track'][:29] if len(t['track']) > 29 else t['track']
        artist = t['artist'][:19] if len(t['artist']) > 19 else t['artist']
        
        print(f"{i:<3} | {name:<30} | {artist:<20} | "
              f"{t['bpm']:<6.1f} | {t['camelot']:<7} | "
              f"{t['energy']:<6.2f} | {t['popularity']:<3}")
    
    # Analysis
    analysis = analyze_sequence(sequence)
    
    print("\n" + "=" * 100)
    print("SET ANALYSIS".center(100))
    print("=" * 100)
    
    print(f"\nTotal Duration:           {analysis['total_duration']:.1f} minutes")
    print(f"Avg Transition Score:     {analysis['avg_transition_score']:.2f}/1.0")
    print(f"Harmonic Violations:      {analysis['harmonic_violations']} transitions")
    print(f"BPM Range:                {analysis['bpm_range'][0]:.0f} - {analysis['bpm_range'][1]:.0f} BPM")
    print(f"Energy Progression:       {analysis['energy_progression']}")

if __name__ == '__main__':
    # Load tracks
    with open('tracks_enriched.json', 'r') as f:
        tracks = json.load(f)
    
    print("=" * 100)
    print("TRACK SEQUENCING COMPARISON".center(100))
    print("=" * 100)
    
    # Method 1: BPM-only (naive approach)
    print("\n" + "-" * 100)
    print("METHOD 1: BPM-ONLY SEQUENCING (NAIVE)".center(100))
    print("-" * 100)
    
    bpm_sequence = sequence_tracks_bpm_only(tracks)
    print_sequence(bpm_sequence, "BPM-ONLY SEQUENCE")
    bpm_analysis = analyze_sequence(bpm_sequence)
    
    # Method 2: Multi-factor greedy (our algorithm)
    print("\n" + "-" * 100)
    print("METHOD 2: MULTI-FACTOR GREEDY SEQUENCING (OUR ALGORITHM)".center(100))
    print("-" * 100)
    
    greedy_sequence = sequence_tracks_greedy(tracks)
    print_sequence(greedy_sequence, "OPTIMIZED SEQUENCE")
    greedy_analysis = analyze_sequence(greedy_sequence)
    
    # Comparison
    print("\n" + "=" * 100)
    print("IMPROVEMENT ANALYSIS".center(100))
    print("=" * 100)
    
    print("\nBPM-Only vs. Multi-Factor Greedy:")
    print("-" * 100)
    
    score_improvement = ((greedy_analysis['avg_transition_score'] - 
                         bpm_analysis['avg_transition_score']) / 
                        bpm_analysis['avg_transition_score'] * 100)
    
    print(f"Avg Transition Score:")
    print(f"  BPM-only:       {bpm_analysis['avg_transition_score']:.2f}/1.0")
    print(f"  Multi-factor:   {greedy_analysis['avg_transition_score']:.2f}/1.0")
    print(f"  Improvement:    {score_improvement:+.1f}%")
    
    print(f"\nHarmonic Violations:")
    print(f"  BPM-only:       {bpm_analysis['harmonic_violations']} transitions")
    print(f"  Multi-factor:   {greedy_analysis['harmonic_violations']} transitions")
    print(f"  Improvement:    {bpm_analysis['harmonic_violations'] - greedy_analysis['harmonic_violations']} fewer violations")
    
    print(f"\nEnergy Progression:")
    print(f"  BPM-only:       {bpm_analysis['energy_progression']}")
    print(f"  Multi-factor:   {greedy_analysis['energy_progression']}")
    
    print("\n" + "=" * 100)
    print("✓ Hour 4 Complete: Sequencing algorithm working!".center(100))
    print(f"Algorithm achieves {score_improvement:+.1f}% better transitions".center(100))
    print("=" * 100)

