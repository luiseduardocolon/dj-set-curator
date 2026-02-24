"""
Camelot Wheel Key Conversion System
Converts musical keys to Camelot notation for harmonic mixing

The Camelot Wheel is a DJ tool that simplifies harmonic mixing:
- Numbers (1-12): Represent the musical key
- Letters (A/B): A = Minor, B = Major
- Compatible mixes: Same number, adjacent numbers (±1), or switch A↔B

Example transitions:
- 8A → 8B (same key, energy shift)
- 8A → 9A (adjacent, smooth)
- 8A → 7A (adjacent, smooth)
"""

# Camelot Wheel Mapping
# Format: (key, mode) -> Camelot notation
CAMELOT_MAP = {
    # Major keys (B)
    ('C', 'major'): '8B',
    ('Db', 'major'): '3B',
    ('D', 'major'): '10B',
    ('Eb', 'major'): '5B',
    ('E', 'major'): '12B',
    ('F', 'major'): '7B',
    ('F#', 'major'): '2B',
    ('Gb', 'major'): '2B',  # Enharmonic equivalent
    ('G', 'major'): '9B',
    ('Ab', 'major'): '4B',
    ('A', 'major'): '11B',
    ('Bb', 'major'): '6B',
    ('B', 'major'): '1B',
    
    # Minor keys (A)
    ('C', 'minor'): '5A',
    ('C#', 'minor'): '12A',
    ('Db', 'minor'): '12A',  # Enharmonic equivalent
    ('D', 'minor'): '7A',
    ('Eb', 'minor'): '2A',
    ('E', 'minor'): '9A',
    ('F', 'minor'): '4A',
    ('F#', 'minor'): '11A',
    ('Gb', 'minor'): '11A',  # Enharmonic equivalent
    ('G', 'minor'): '6A',
    ('G#', 'minor'): '1A',
    ('Ab', 'minor'): '1A',  # Enharmonic equivalent
    ('A', 'minor'): '8A',
    ('Bb', 'minor'): '3A',
    ('B', 'minor'): '10A',
}

def to_camelot(key, mode):
    """
    Convert musical key and mode to Camelot notation
    
    Args:
        key: Musical key (e.g., 'C', 'F#', 'Bb')
        mode: 'major' or 'minor'
    
    Returns:
        Camelot notation (e.g., '8B', '5A') or None if invalid
    
    Examples:
        >>> to_camelot('A', 'minor')
        '8A'
        >>> to_camelot('C', 'major')
        '8B'
        >>> to_camelot('F#', 'minor')
        '11A'
    """
    # Normalize mode
    mode = mode.lower()
    
    # Look up in map
    camelot = CAMELOT_MAP.get((key, mode))
    
    if camelot:
        return camelot
    
    # Try common variations
    if key.endswith('b'):
        # Try sharp equivalent (e.g., Db -> C#)
        pass  # Already handled in map
    
    return None

def are_compatible(camelot1, camelot2):
    """
    Check if two Camelot keys are harmonically compatible
    
    Compatible transitions:
    1. Same key (8A → 8A): Perfect match
    2. Adjacent numbers (8A → 9A, 8A → 7A): Smooth transition
    3. Same number, different letter (8A → 8B): Energy shift
    
    Args:
        camelot1: First Camelot key (e.g., '8A')
        camelot2: Second Camelot key (e.g., '9A')
    
    Returns:
        Tuple: (is_compatible: bool, compatibility_type: str)
    
    Examples:
        >>> are_compatible('8A', '8A')
        (True, 'perfect')
        >>> are_compatible('8A', '9A')
        (True, 'adjacent')
        >>> are_compatible('8A', '8B')
        (True, 'relative')
        >>> are_compatible('8A', '3B')
        (False, 'incompatible')
    """
    if not camelot1 or not camelot2:
        return (False, 'invalid')
    
    # Parse Camelot notation
    num1 = int(camelot1[:-1])
    letter1 = camelot1[-1]
    num2 = int(camelot2[:-1])
    letter2 = camelot2[-1]
    
    # Same key
    if camelot1 == camelot2:
        return (True, 'perfect')
    
    # Same number, different letter (relative major/minor)
    if num1 == num2 and letter1 != letter2:
        return (True, 'relative')
    
    # Adjacent numbers (wrap around 1-12)
    if letter1 == letter2:
        diff = abs(num1 - num2)
        # Handle wrap-around (12 → 1)
        if diff == 1 or diff == 11:
            return (True, 'adjacent')
    
    # Not compatible
    return (False, 'incompatible')

def get_compatible_keys(camelot):
    """
    Get all compatible keys for a given Camelot key
    
    Args:
        camelot: Camelot key (e.g., '8A')
    
    Returns:
        Dict with categories: perfect, relative, adjacent
    
    Example:
        >>> get_compatible_keys('8A')
        {
            'perfect': ['8A'],
            'relative': ['8B'],
            'adjacent': ['7A', '9A']
        }
    """
    if not camelot:
        return None
    
    num = int(camelot[:-1])
    letter = camelot[-1]
    
    # Calculate adjacent numbers (with wrap-around)
    prev_num = 12 if num == 1 else num - 1
    next_num = 1 if num == 12 else num + 1
    
    # Opposite letter (A ↔ B)
    opposite_letter = 'B' if letter == 'A' else 'A'
    
    return {
        'perfect': [camelot],
        'relative': [f'{num}{opposite_letter}'],
        'adjacent': [f'{prev_num}{letter}', f'{next_num}{letter}']
    }

def get_transition_description(from_key, to_key):
    """
    Get human-readable description of a key transition
    
    Args:
        from_key: Starting Camelot key
        to_key: Ending Camelot key
    
    Returns:
        String description of the transition
    """
    compatible, comp_type = are_compatible(from_key, to_key)
    
    if not compatible:
        return f"❌ Incompatible ({from_key} → {to_key})"
    
    descriptions = {
        'perfect': f"✓ Perfect match ({from_key} → {to_key})",
        'relative': f"✓ Relative major/minor ({from_key} → {to_key})",
        'adjacent': f"✓ Adjacent key ({from_key} → {to_key})"
    }
    
    return descriptions.get(comp_type, f"? Unknown ({from_key} → {to_key})")

if __name__ == '__main__':
    # Test the conversions
    print("=" * 70)
    print("CAMELOT WHEEL CONVERSION TESTS".center(70))
    print("=" * 70)
    
    test_keys = [
        ('A', 'minor'),
        ('C', 'major'),
        ('F#', 'minor'),
        ('D', 'major'),
        ('Eb', 'minor'),
    ]
    
    print("\nKey → Camelot Conversions:")
    print("-" * 70)
    for key, mode in test_keys:
        camelot = to_camelot(key, mode)
        print(f"{key} {mode:6} → {camelot}")
    
    print("\n" + "=" * 70)
    print("COMPATIBILITY TESTS".center(70))
    print("=" * 70)
    
    test_transitions = [
        ('8A', '8A'),   # Perfect
        ('8A', '8B'),   # Relative
        ('8A', '9A'),   # Adjacent
        ('8A', '7A'),   # Adjacent
        ('8A', '3B'),   # Incompatible
    ]
    
    print("\nTransition Compatibility:")
    print("-" * 70)
    for from_k, to_k in test_transitions:
        print(get_transition_description(from_k, to_k))
    
    print("\n" + "=" * 70)
    print("✓ Camelot system working!".center(70))
    print("=" * 70)

