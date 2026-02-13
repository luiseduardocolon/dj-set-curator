"""
Temporal Activities - DJ Set Curator
Each activity is a retriable, fault-tolerant operation

Activities in this module:
- load_tracks_activity: Load track dataset from JSON
"""
import json
from temporalio import activity

@activity.defn
async def load_tracks_activity(filepath: str = 'tracks_enriched.json') -> list:
    """
    Load track dataset as a Temporal activity
    
    Benefits of using an activity:
    - Automatic retries if file read fails
    - Timeout protection
    - Execution tracking in Temporal UI
    - Fault tolerance (survives worker crashes)
    
    Args:
        filepath: Path to JSON track dataset
        
    Returns:
        List of track dictionaries
        
    Raises:
        FileNotFoundError: If dataset doesn't exist
        json.JSONDecodeError: If JSON is invalid
    """
    activity.logger.info(f"Loading tracks from: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            tracks = json.load(f)
        
        activity.logger.info(f"Successfully loaded {len(tracks)} tracks")
        
        # Log summary for debugging
        if tracks:
            avg_bpm = sum(t['bpm'] for t in tracks) / len(tracks)
            activity.logger.info(f"Dataset summary: {len(tracks)} tracks, avg BPM: {avg_bpm:.1f}")
        
        return tracks
        
    except FileNotFoundError as e:
        activity.logger.error(f"Dataset file not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        activity.logger.error(f"Invalid JSON in dataset: {e}")
        raise
    except Exception as e:
        activity.logger.error(f"Unexpected error loading tracks: {e}")
        raise

# More activities will be added in future hours

