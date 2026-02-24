"""
Transition Justification Engine
Generates human-readable explanations for DJ set decisions

Explains each transition based on:
- Harmonic compatibility (Camelot wheel)
- BPM changes (tempo shifts)
- Energy progression (crowd dynamics)
- Popularity placement (strategic bangers)
- Overall compatibility score
"""

from camelot import are_compatible, get_transition_description
from scoring import total_compatibility

def justify_transition(track1, track2, position_in_set):
    """
    Generate detailed justification for a track transition
    
    Args:
        track1: First track dict
        track2: Second track dict
        position_in_set: Position (0.0-1.0)
    
    Returns:
        String with multi-line explanation
    """
    # Calculate scores
    scores = total_compatibility(track1, track2, position_in_set)
    
    # Build justification
    lines = []
    lines.append(f"TRANSITION: {track1['track']} → {track2['track']}")
    lines.append("=" * 80)
    
    # Harmonic justification
    compatible, comp_type = are_compatible(track1['camelot'], track2['camelot'])
    lines.append(f"\n1. HARMONIC COMPATIBILITY (Score: {scores['harmonic']:.2f}/1.0)")
    lines.append(f"   {track1['camelot']} → {track2['camelot']}")
    
    if comp_type == 'perfect':
        lines.append("   ✓ Perfect match - same key maintains harmonic continuity")
    elif comp_type == 'adjacent':
        lines.append("   ✓ Adjacent on Camelot wheel - smooth, professional transition")
    elif comp_type == 'relative':
        lines.append("   ✓ Relative major/minor - shifts energy while staying harmonic")
    else:
        lines.append("   ⚠ Key clash - may sound dissonant to trained ears")
    
    # BPM justification
    bpm_diff = track2['bpm'] - track1['bpm']
    bpm_pct = abs(bpm_diff) / track1['bpm'] * 100
    
    lines.append(f"\n2. BPM TRANSITION (Score: {scores['bpm']:.2f}/1.0)")
    lines.append(f"   {track1['bpm']:.1f} → {track2['bpm']:.1f} BPM "
                 f"({bpm_diff:+.1f} BPM, {bpm_pct:.1f}% change)")
    
    if bpm_pct == 0:
        lines.append("   ✓ Identical tempo - seamless mix possible")
    elif bpm_pct <= 3:
        lines.append("   ✓ Imperceptible change - crowd won't notice the shift")
    elif bpm_pct <= 6:
        lines.append("   ✓ Smooth transition - feels natural on the dancefloor")
    elif bpm_pct <= 10:
        lines.append("   ○ Noticeable shift - requires skilled mixing technique")
    else:
        lines.append("   ⚠ Large tempo jump - may disrupt flow")
    
    # Energy justification
    energy_diff = track2['energy'] - track1['energy']
    
    lines.append(f"\n3. ENERGY PROGRESSION (Score: {scores['energy']:.2f}/1.0)")
    lines.append(f"   {track1['energy']:.2f} → {track2['energy']:.2f} "
                 f"({energy_diff:+.2f} change)")
    
    if abs(energy_diff) <= 0.05:
        lines.append("   ✓ Maintains current energy - keeps momentum steady")
    elif 0.05 < energy_diff <= 0.15:
        lines.append("   ✓ Gradual energy increase - building the vibe")
    elif energy_diff > 0.15:
        lines.append("   ↑ Significant energy boost - taking it to the next level")
    elif -0.15 <= energy_diff < -0.05:
        lines.append("   ↓ Gentle cool-down - giving dancers a breather")
    else:
        lines.append("   ↓↓ Major energy drop - risk of losing momentum")
    
    # Popularity justification
    avg_pop = (track1['popularity'] + track2['popularity']) / 2
    is_peak = 0.35 <= position_in_set <= 0.65
    
    lines.append(f"\n4. CROWD ENGAGEMENT (Score: {scores['popularity']:.2f}/1.0)")
    lines.append(f"   Avg Popularity: {avg_pop:.0f}/100")
    lines.append(f"   Position in set: {position_in_set:.0%} (Peak zone: 35-65%)")
    
    if avg_pop >= 80:
        if is_peak:
            lines.append("   🔥 BANGER at PEAK position - maximum crowd impact!")
        else:
            lines.append("   🔥 High-recognition track - crowd favorite")
    elif avg_pop >= 60:
        lines.append("   ○ Solid crowd-pleaser - keeps energy consistent")
    else:
        lines.append("   ○ Lower-profile track - good for pacing variation")
    
    # Overall score
    lines.append(f"\n" + "=" * 80)
    lines.append(f"OVERALL COMPATIBILITY: {scores['total']:.2f}/1.0")
    
    if scores['total'] >= 0.8:
        lines.append("✓ EXCELLENT transition - professional DJ-quality mix")
    elif scores['total'] >= 0.6:
        lines.append("✓ GOOD transition - solid choice")
    elif scores['total'] >= 0.4:
        lines.append("○ ACCEPTABLE transition - workable with skill")
    else:
        lines.append("⚠ CHALLENGING transition - requires expert technique")
    
    return "\n".join(lines)

def generate_set_summary(sequence):
    """
    Generate summary analysis of entire set
    
    Returns comprehensive report on set quality
    """
    from scoring import total_compatibility, are_compatible
    
    lines = []
    lines.append("=" * 100)
    lines.append("COMPLETE DJ SET ANALYSIS".center(100))
    lines.append("=" * 100)
    
    # Basic stats
    total_duration = sum(t['duration_ms'] for t in sequence) / 60000
    avg_bpm = sum(t['bpm'] for t in sequence) / len(sequence)
    avg_energy = sum(t['energy'] for t in sequence) / len(sequence)
    avg_pop = sum(t['popularity'] for t in sequence) / len(sequence)
    
    lines.append(f"\nSET OVERVIEW:")
    lines.append(f"  Total tracks:     {len(sequence)}")
    lines.append(f"  Total duration:   {total_duration:.1f} minutes ({total_duration/60:.1f} hours)")
    lines.append(f"  Average BPM:      {avg_bpm:.1f}")
    lines.append(f"  Average energy:   {avg_energy:.2f}/1.0")
    lines.append(f"  Average popularity: {avg_pop:.0f}/100")
    
    # Transition quality analysis
    if len(sequence) > 1:
        transition_scores = []
        harmonic_violations = 0
        
        for i in range(len(sequence) - 1):
            position = i / (len(sequence) - 1)
            scores = total_compatibility(sequence[i], sequence[i+1], position)
            transition_scores.append(scores['total'])
            
            compatible, _ = are_compatible(sequence[i]['camelot'], sequence[i+1]['camelot'])
            if not compatible:
                harmonic_violations += 1
        
        avg_transition = sum(transition_scores) / len(transition_scores)
        excellent = sum(1 for s in transition_scores if s >= 0.8)
        good = sum(1 for s in transition_scores if 0.6 <= s < 0.8)
        acceptable = sum(1 for s in transition_scores if 0.4 <= s < 0.6)
        challenging = sum(1 for s in transition_scores if s < 0.4)
        
        lines.append(f"\nTRANSITION QUALITY:")
        lines.append(f"  Average score:       {avg_transition:.2f}/1.0")
        lines.append(f"  Excellent (≥0.8):    {excellent} transitions ({excellent/len(transition_scores)*100:.0f}%)")
        lines.append(f"  Good (0.6-0.8):      {good} transitions ({good/len(transition_scores)*100:.0f}%)")
        lines.append(f"  Acceptable (0.4-0.6): {acceptable} transitions ({acceptable/len(transition_scores)*100:.0f}%)")
        lines.append(f"  Challenging (<0.4):  {challenging} transitions ({challenging/len(transition_scores)*100:.0f}%)")
        lines.append(f"  Harmonic violations: {harmonic_violations} ({harmonic_violations/len(transition_scores)*100:.0f}%)")
    
    # Energy arc analysis
    energies = [t['energy'] for t in sequence]
    third = len(energies) // 3
    
    start_energy = sum(energies[:third]) / max(1, third)
    middle_energy = sum(energies[third:2*third]) / max(1, third)
    end_energy = sum(energies[2*third:]) / max(1, len(energies) - 2*third)
    
    lines.append(f"\nENERGY ARC:")
    lines.append(f"  Opening third:   {start_energy:.2f}/1.0")
    lines.append(f"  Middle third:    {middle_energy:.2f}/1.0")
    lines.append(f"  Closing third:   {end_energy:.2f}/1.0")
    
    if middle_energy > start_energy and middle_energy > end_energy:
        lines.append("  ✓ Ideal arc - peaks in the middle like a pro DJ set")
    elif end_energy > start_energy:
        lines.append("  ↑ Building arc - climax at the end")
    elif start_energy > end_energy:
        lines.append("  ↓ Descending arc - winds down gradually")
    else:
        lines.append("  → Flat arc - consistent energy throughout")
    
    # BPM progression
    bpms = [t['bpm'] for t in sequence]
    lines.append(f"\nBPM PROGRESSION:")
    lines.append(f"  Range: {min(bpms):.0f} - {max(bpms):.0f} BPM")
    lines.append(f"  Starting BPM: {bpms[0]:.0f}")
    lines.append(f"  Peak BPM: {max(bpms):.0f}")
    lines.append(f"  Ending BPM: {bpms[-1]:.0f}")
    
    # Highlight bangers
    bangers = [(i+1, t) for i, t in enumerate(sequence) if t['popularity'] >= 90]
    
    if bangers:
        lines.append(f"\n🔥 HIGH-IMPACT TRACKS (90+ popularity):")
        for pos, track in bangers:
            position_pct = (pos / len(sequence)) * 100
            in_peak = 35 <= position_pct <= 65
            marker = "★" if in_peak else " "
            lines.append(f"  {marker} Track #{pos} ({position_pct:.0f}%): "
                        f"{track['track']} ({track['popularity']}/100)")
    
    lines.append("\n" + "=" * 100)
    
    return "\n".join(lines)

def save_justified_set(sequence, output_file='set_with_justifications.txt'):
    """
    Save complete set with all justifications to file
    """
    with open(output_file, 'w') as f:
        # Write summary
        f.write(generate_set_summary(sequence))
        f.write("\n\n")
        
        # Write each transition with justification
        f.write("=" * 100 + "\n")
        f.write("TRACK-BY-TRACK JUSTIFICATIONS".center(100) + "\n")
        f.write("=" * 100 + "\n\n")
        
        for i in range(len(sequence) - 1):
            position = i / (len(sequence) - 1)
            justification = justify_transition(sequence[i], sequence[i+1], position)
            f.write(justification)
            f.write("\n\n" + "-" * 100 + "\n\n")
        
        # Final track (no transition)
        f.write(f"FINAL TRACK: {sequence[-1]['track']} by {sequence[-1]['artist']}\n")
        f.write(f"  BPM: {sequence[-1]['bpm']}, Camelot: {sequence[-1]['camelot']}, "
                f"Energy: {sequence[-1]['energy']:.2f}, Pop: {sequence[-1]['popularity']}\n")
        f.write("  Perfect closer - ends the set on a high note!\n")
    
    print(f"✓ Saved justified set to {output_file}")

if __name__ == '__main__':
    import json
    
    # Load optimized sequence
    with open('sequence_optimized.json', 'r') as f:
        sequence = json.load(f)
    
    print("=" * 100)
    print("GENERATING FULL SET JUSTIFICATIONS".center(100))
    print("=" * 100)
    
    # Generate and save
    save_justified_set(sequence)
    
    # Show a sample justification
    print("\nSAMPLE TRANSITION JUSTIFICATION:")
    print("-" * 100)
    sample = justify_transition(sequence[0], sequence[1], position_in_set=0.05)
    print(sample)
    
    print("\n" + "=" * 100)
    print("✓ Hour 5 Complete: Full justifications generated!".center(100))
    print("Check set_with_justifications.txt for complete analysis".center(100))
    print("=" * 100)

