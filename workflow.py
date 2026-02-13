"""
Temporal Workflows - DJ Set Curator

Workflows orchestrate activities into complete processes
Each workflow represents a full DJ set creation pipeline
"""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# We'll import activity types when needed
with workflow.unsafe.imports_passed_through():
    from activities import load_tracks_activity

@workflow.defn
class DJSetWorkflow:
    """
    Main workflow for creating optimized DJ sets
    
    This workflow will eventually:
    1. Load tracks
    2. Calculate Camelot keys
    3. Score compatibility
    4. Sequence tracks
    5. Generate justifications
    
    For Hour 7, we start with just step 1.
    """
    
    @workflow.run
    async def run(self, dataset_path: str = 'tracks_enriched.json') -> dict:
        """
        Execute the DJ set creation workflow
        
        Args:
            dataset_path: Path to track dataset
            
        Returns:
            Dict with workflow results
        """
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ Set Workflow Started")
        workflow.logger.info("=" * 70)
        
        # Define retry policy for activities
        # If an activity fails, Temporal will automatically retry it
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )
        
        # Step 1: Load tracks (with automatic retries)
        workflow.logger.info("Step 1: Loading track dataset...")
        
        tracks = await workflow.execute_activity(
            load_tracks_activity,
            dataset_path,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )
        
        workflow.logger.info(f"Loaded {len(tracks)} tracks successfully")
        
        # For now, just return the loaded tracks
        result = {
            'status': 'success',
            'tracks_loaded': len(tracks),
            'sample_tracks': [
                {
                    'track': t['track'],
                    'artist': t['artist'],
                    'bpm': t['bpm'],
                    'camelot': t['camelot']
                }
                for t in tracks[:3]  # First 3 tracks as sample
            ]
        }
        
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ Set Workflow Completed")
        workflow.logger.info("=" * 70)
        
        return result

# Keep the old HelloWorkflow for backwards compatibility
@workflow.defn
class HelloWorkflow:
    """Simple hello world workflow (from Hour 6)"""
    
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info(f"HelloWorkflow started for: {name}")
        greeting = f"Hello, {name}! Welcome to Temporal DJ Set Curator!"
        workflow.logger.info(f"HelloWorkflow completed: {greeting}")
        return greeting

