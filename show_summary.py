"""
Quick summary viewer - shows key insights without full details
"""
import json
from justifier import generate_set_summary

# Load optimized sequence
with open('sequence_optimized.json', 'r') as f:
    sequence = json.load(f)

# Print summary
print(generate_set_summary(sequence))

print("\n" + "=" * 100)
print("OPENING SEQUENCE (First 5 Tracks):".center(100))
print("=" * 100)

for i, track in enumerate(sequence[:5], 1):
    print(f"{i}. {track['track']:35} | {track['artist']:25} | "
          f"{track['bpm']:6.1f} BPM | {track['camelot']:4} | "
          f"Energy: {track['energy']:.2f} | Pop: {track['popularity']}")

print("\n" + "=" * 100)
print("PEAK SEQUENCE (Middle 5 Tracks):".center(100))
print("=" * 100)

middle_start = len(sequence) // 2 - 2
for i, track in enumerate(sequence[middle_start:middle_start+5], middle_start+1):
    print(f"{i}. {track['track']:35} | {track['artist']:25} | "
          f"{track['bpm']:6.1f} BPM | {track['camelot']:4} | "
          f"Energy: {track['energy']:.2f} | Pop: {track['popularity']}")

print("\n" + "=" * 100)
print("CLOSING SEQUENCE (Last 5 Tracks):".center(100))
print("=" * 100)

for i, track in enumerate(sequence[-5:], len(sequence)-4):
    print(f"{i}. {track['track']:35} | {track['artist']:25} | "
          f"{track['bpm']:6.1f} BPM | {track['camelot']:4} | "
          f"Energy: {track['energy']:.2f} | Pop: {track['popularity']}")

