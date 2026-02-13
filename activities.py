"""
Temporal Activities - DJ Set Curator
Each activity is a retriable, fault-tolerant operation
"""
import json
from temporalio import activity

@activity.defn
async def load_tracks_activity(filepath: str = 'tracks_enriched.json') -> list:
    """
    Load track dataset as a Temporal activity
    
    Benefits:
    - Automatic retries if file read fails
    - Timeout protection
    - Execution tracking in Temporal UI
    """
    activity.logger.info(f"Loading tracks from: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            tracks = json.load(f)
        
        activity.logger.info(f"Successfully loaded {len(tracks)} tracks")
        
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

@activity.defn
async def sequence_tracks_activity(tracks: list) -> list:
    """
    Sequence tracks using greedy algorithm as a Temporal activity
    
    This activity:
    - Takes unsorted tracks
    - Applies multi-factor greedy sequencing
    - Returns optimized track order
    
    Benefits of activity:
    - Can retry if computation fails
    - Tracks execution time
    - Can be monitored in real-time
    
    Args:
        tracks: List of track dicts
        
    Returns:
        Optimized sequence of tracks
    """
    activity.logger.info(f"Sequencing {len(tracks)} tracks using greedy algorithm")
    
    try:
        # Import sequencer (inside activity to avoid import issues)
        from sequencer import sequence_tracks_greedy
        
        # Run the greedy sequencing algorithm
        sequenced = sequence_tracks_greedy(tracks)
        
        activity.logger.info(f"Successfully sequenced {len(sequenced)} tracks")
        
        # Log some metrics
        if len(sequenced) > 1:
            from scoring import total_compatibility
            
            # Calculate average transition score
            scores = []
            for i in range(len(sequenced) - 1):
                position = i / (len(sequenced) - 1)
                score = total_compatibility(sequenced[i], sequenced[i+1], position)
                scores.append(score['total'])
            
            avg_score = sum(scores) / len(scores)
            activity.logger.info(f"Avg transition score: {avg_score:.2f}/1.0")
            activity.logger.info(f"Opening track: {sequenced[0]['track']} "
                               f"({sequenced[0]['bpm']} BPM)")
            activity.logger.info(f"Closing track: {sequenced[-1]['track']} "
                               f"({sequenced[-1]['bpm']} BPM)")
        
        return sequenced
        
    except Exception as e:
        activity.logger.error(f"Error during sequencing: {e}")
        raise

@activity.defn
async def generate_justifications_activity(sequence: list) -> dict:
    """
    Generate comprehensive justifications for the DJ set
    
    This activity:
    - Takes a sequenced track list
    - Generates transition justifications
    - Creates overall set analysis
    - Returns structured justification data
    
    Args:
        sequence: Ordered list of tracks
        
    Returns:
        Dict with justifications and analysis
    """
    activity.logger.info(f"Generating justifications for {len(sequence)} track sequence")
    
    try:
        from justifier import generate_set_summary
        from scoring import total_compatibility
        
        # Generate transitions with scores
        transitions = []
        
        for i in range(len(sequence) - 1):
            position = i / (len(sequence) - 1)
            scores = total_compatibility(sequence[i], sequence[i+1], position)
            
            transitions.append({
                'from_track': sequence[i]['track'],
                'to_track': sequence[i+1]['track'],
                'position': position,
                'scores': {
                    'harmonic': scores['harmonic'],
                    'bpm': scores['bpm'],
                    'energy': scores['energy'],
                    'popularity': scores['popularity'],
                    'total': scores['total']
                }
            })
        
        # Generate summary analysis
        activity.logger.info("Generating set summary analysis")
        summary_text = generate_set_summary(sequence)
        
        # Calculate metrics
        total_duration = sum(t['duration_ms'] for t in sequence) / 60000
        avg_transition = sum(t['scores']['total'] for t in transitions) / len(transitions)
        
        activity.logger.info(f"Set duration: {total_duration:.1f} minutes")
        activity.logger.info(f"Avg transition score: {avg_transition:.2f}/1.0")
        
        result = {
            'sequence': [
                {
                    'track': t['track'],
                    'artist': t['artist'],
                    'bpm': t['bpm'],
                    'camelot': t['camelot'],
                    'energy': t['energy'],
                    'popularity': t['popularity']
                }
                for t in sequence
            ],
            'transitions': transitions,
            'summary': summary_text,
            'metrics': {
                'total_tracks': len(sequence),
                'total_duration_minutes': total_duration,
                'avg_transition_score': avg_transition
            }
        }
        
        activity.logger.info("Justifications generated successfully")
        
        return result
        
    except Exception as e:
        activity.logger.error(f"Error generating justifications: {e}")
        raise

