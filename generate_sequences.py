"""
Generate and save optimized sequences for later use
"""
import json
from sequencer import sequence_tracks_greedy, sequence_tracks_bpm_only

# Load tracks
with open('tracks_enriched.json', 'r') as f:
    tracks = json.load(f)

# Generate sequences
bpm_sequence = sequence_tracks_bpm_only(tracks)
greedy_sequence = sequence_tracks_greedy(tracks)

# Save sequences
with open('sequence_bpm_only.json', 'w') as f:
    json.dump(bpm_sequence, f, indent=2)

with open('sequence_optimized.json', 'w') as f:
    json.dump(greedy_sequence, f, indent=2)

print("✓ Saved sequences:")
print("  - sequence_bpm_only.json (naive BPM sort)")
print("  - sequence_optimized.json (multi-factor greedy)")

