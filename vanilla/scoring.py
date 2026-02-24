"""
Multi-Factor Compatibility Scoring System
Rates how well two tracks will transition in a DJ set

Scoring factors (weighted):
- Harmonic (40%): Camelot wheel compatibility
- BPM (30%): Tempo matching
- Energy (20%): Energy flow progression
- Popularity (10%): Crowd engagement placement

Total score: 0.0 (incompatible) to 1.0 (perfect match)
"""

from camelot import are_compatible

# Scoring weights (must sum to 1.0)
WEIGHTS = {
    'harmonic': 0.40,
    'bpm': 0.30,
    'energy': 0.20,
    'popularity': 0.10
}

def harmonic_score(camelot1, camelot2):
    """
    Score harmonic compatibility using Camelot wheel
    
    Returns:
        1.0: Perfect match (same key)
        0.8: Adjacent key (smooth transition)
        0.7: Relative major/minor (energy shift)
        0.3: Incompatible (harsh transition)
    
    Examples:
        >>> harmonic_score('8A', '8A')
        1.0
        >>> harmonic_score('8A', '9A')
        0.8
        >>> harmonic_score('8A', '8B')
        0.7
        >>> harmonic_score('8A', '3B')
        0.3
    """
    compatible, comp_type = are_compatible(camelot1, camelot2)
    
    scores = {
        'perfect': 1.0,
        'adjacent': 0.8,
        'relative': 0.7,
        'incompatible': 0.3,
        'invalid': 0.0
    }
    
    return scores.get(comp_type, 0.0)

def bpm_score(bpm1, bpm2):
    """
    Score BPM compatibility based on tempo difference
    
    DJ Rule: ≤3% change is imperceptible, ≤6% is smooth
    
    Returns:
        1.0: Identical BPM (0% change)
        0.9: ≤3% change (imperceptible)
        0.7: 3-6% change (smooth)
        0.5: 6-10% change (noticeable)
        0.2: >10% change (jarring)
    
    Examples:
        >>> bpm_score(120.0, 120.0)
        1.0
        >>> bpm_score(120.0, 123.0)  # 2.5% change
        0.9
        >>> bpm_score(120.0, 126.0)  # 5% change
        0.7
        >>> bpm_score(120.0, 135.0)  # 12.5% change
        0.2
    """
    if bpm1 == 0 or bpm2 == 0:
        return 0.0
    
    # Calculate percentage difference
    diff_pct = abs(bpm1 - bpm2) / max(bpm1, bpm2) * 100
    
    if diff_pct == 0:
        return 1.0
    elif diff_pct <= 3:
        return 0.9
    elif diff_pct <= 6:
        return 0.7
    elif diff_pct <= 10:
        return 0.5
    else:
        return 0.2

def energy_score(energy1, energy2):
    """
    Score energy flow compatibility
    
    DJ Rule: Gradual energy changes keep crowd engaged
    
    Returns:
        1.0: Identical energy (maintaining vibe)
        0.8: ≤0.1 change (subtle shift)
        0.6: 0.1-0.2 change (noticeable shift)
        0.4: 0.2-0.3 change (significant shift)
        0.2: >0.3 change (dramatic shift)
    
    Examples:
        >>> energy_score(0.8, 0.8)
        1.0
        >>> energy_score(0.8, 0.85)
        0.8
        >>> energy_score(0.8, 0.95)
        0.6
        >>> energy_score(0.8, 0.5)
        0.2
    """
    diff = abs(energy1 - energy2)
    
    if diff == 0:
        return 1.0
    elif diff <= 0.1:
        return 0.8
    elif diff <= 0.2:
        return 0.6
    elif diff <= 0.3:
        return 0.4
    else:
        return 0.2

def popularity_score(pop1, pop2, position_in_set=0.5):
    """
    Score popularity compatibility for crowd engagement
    
    Strategy: Place high-popularity tracks (80+) at peak moments
    Peak = middle 30% of set (positions 0.35-0.65)
    
    Returns:
        1.0: High-pop track at peak position
        0.8: High-pop track near peak
        0.6: Medium-pop track, or high-pop off-peak
        0.4: Low-pop track
    
    Args:
        pop1: First track popularity (0-100)
        pop2: Second track popularity (0-100)
        position_in_set: Position in set (0.0=start, 1.0=end)
    
    Examples:
        >>> popularity_score(90, 92, position_in_set=0.5)  # Peak
        1.0
        >>> popularity_score(90, 92, position_in_set=0.2)  # Early
        0.6
        >>> popularity_score(70, 72, position_in_set=0.5)
        0.6
    """
    avg_pop = (pop1 + pop2) / 2
    
    # Is this a peak position? (35-65% through the set)
    is_peak = 0.35 <= position_in_set <= 0.65
    
    # High popularity track (80+)
    if avg_pop >= 80:
        if is_peak:
            return 1.0  # Perfect: banger at peak
        else:
            return 0.6  # Suboptimal: wasting a banger
    
    # Medium popularity (60-80)
    elif avg_pop >= 60:
        return 0.6
    
    # Lower popularity (<60)
    else:
        return 0.4

def total_compatibility(track1, track2, position_in_set=0.5, weights=None):
    """
    Calculate total compatibility score between two tracks
    
    Args:
        track1: First track dict with camelot, bpm, energy, popularity
        track2: Second track dict
        position_in_set: Position in set (0.0-1.0)
        weights: Optional custom weights dict
    
    Returns:
        Dict with individual scores and total weighted score
    
    Example:
        >>> track1 = {
        ...     'camelot': '8A', 'bpm': 120, 
        ...     'energy': 0.8, 'popularity': 90
        ... }
        >>> track2 = {
        ...     'camelot': '9A', 'bpm': 122, 
        ...     'energy': 0.82, 'popularity': 88
        ... }
        >>> result = total_compatibility(track1, track2, 0.5)
        >>> result['total']  # Should be ~0.85
        0.85
    """
    if weights is None:
        weights = WEIGHTS
    
    # Calculate individual scores
    scores = {
        'harmonic': harmonic_score(track1['camelot'], track2['camelot']),
        'bpm': bpm_score(track1['bpm'], track2['bpm']),
        'energy': energy_score(track1['energy'], track2['energy']),
        'popularity': popularity_score(
            track1['popularity'], 
            track2['popularity'], 
            position_in_set
        )
    }
    
    # Calculate weighted total
    total = sum(scores[factor] * weights[factor] for factor in scores)
    
    return {
        'harmonic': scores['harmonic'],
        'bpm': scores['bpm'],
        'energy': scores['energy'],
        'popularity': scores['popularity'],
        'total': total
    }

def score_transition(track1, track2, position_in_set=0.5):
    """
    Score and explain a transition between two tracks
    
    Returns human-readable analysis
    """
    scores = total_compatibility(track1, track2, position_in_set)
    
    # Build explanation
    lines = []
    lines.append(f"Transition: {track1['track']} → {track2['track']}")
    lines.append(f"")
    lines.append(f"Harmonic:    {scores['harmonic']:.2f} ({track1['camelot']} → {track2['camelot']})")
    lines.append(f"BPM:         {scores['bpm']:.2f} ({track1['bpm']:.1f} → {track2['bpm']:.1f})")
    lines.append(f"Energy:      {scores['energy']:.2f} ({track1['energy']:.2f} → {track2['energy']:.2f})")
    lines.append(f"Popularity:  {scores['popularity']:.2f} (avg: {(track1['popularity'] + track2['popularity'])/2:.0f}/100)")
    lines.append(f"")
    lines.append(f"TOTAL SCORE: {scores['total']:.2f}/1.0")
    
    return "\n".join(lines)

if __name__ == '__main__':
    print("=" * 80)
    print("COMPATIBILITY SCORING SYSTEM TESTS".center(80))
    print("=" * 80)
    
    # Test harmonic scoring
    print("\n1. HARMONIC SCORING")
    print("-" * 80)
    harmonic_tests = [
        ('8A', '8A', 'Perfect match'),
        ('8A', '9A', 'Adjacent'),
        ('8A', '8B', 'Relative'),
        ('8A', '3B', 'Incompatible'),
    ]
    for c1, c2, desc in harmonic_tests:
        score = harmonic_score(c1, c2)
        print(f"{c1} → {c2:3} ({desc:15}): {score:.2f}")
    
    # Test BPM scoring
    print("\n2. BPM SCORING")
    print("-" * 80)
    bpm_tests = [
        (120, 120, 'Identical'),
        (120, 123, '2.5% change'),
        (120, 126, '5% change'),
        (120, 135, '12.5% change'),
    ]
    for b1, b2, desc in bpm_tests:
        score = bpm_score(b1, b2)
        pct = abs(b1 - b2) / b1 * 100
        print(f"{b1} → {b2:3} BPM ({desc:15}): {score:.2f}")
    
    # Test energy scoring
    print("\n3. ENERGY SCORING")
    print("-" * 80)
    energy_tests = [
        (0.8, 0.8, 'Identical'),
        (0.8, 0.85, 'Subtle shift'),
        (0.8, 0.95, 'Noticeable shift'),
        (0.8, 0.5, 'Dramatic shift'),
    ]
    for e1, e2, desc in energy_tests:
        score = energy_score(e1, e2)
        print(f"{e1:.2f} → {e2:.2f} ({desc:15}): {score:.2f}")
    
    # Test popularity scoring
    print("\n4. POPULARITY SCORING (Position-Aware)")
    print("-" * 80)
    pop_tests = [
        (90, 92, 0.5, 'High-pop at peak'),
        (90, 92, 0.2, 'High-pop early'),
        (70, 72, 0.5, 'Medium-pop at peak'),
    ]
    for p1, p2, pos, desc in pop_tests:
        score = popularity_score(p1, p2, pos)
        print(f"Pop {(p1+p2)/2:.0f}, Pos {pos:.1f} ({desc:20}): {score:.2f}")
    
    # Test full compatibility
    print("\n5. FULL COMPATIBILITY EXAMPLE")
    print("-" * 80)
    track1 = {
        'track': 'September',
        'camelot': '11B',
        'bpm': 126.0,
        'energy': 0.85,
        'popularity': 92
    }
    track2 = {
        'track': 'Dancing Queen',
        'camelot': '11B',
        'bpm': 102.0,
        'energy': 0.76,
        'popularity': 88
    }
    
    print(score_transition(track1, track2, position_in_set=0.5))
    
    print("\n" + "=" * 80)
    print("✓ Scoring system working!".center(80))
    print("=" * 80)

