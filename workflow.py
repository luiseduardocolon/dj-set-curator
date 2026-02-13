"""
Temporal Workflows - DJ Set Curator
Complete pipeline orchestration
"""
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from activities import (
        load_tracks_activity,
        sequence_tracks_activity,
        generate_justifications_activity
    )

@workflow.defn
class DJSetWorkflow:
    """
    Complete DJ Set Creation Workflow
    
    Pipeline:
    1. Load tracks from dataset
    2. Sequence tracks using greedy algorithm
    3. Generate justifications and analysis
    
    Each step is a separate activity with:
    - Automatic retries
    - Timeout protection
    - Progress tracking
    """
    
    @workflow.run
    async def run(self, dataset_path: str = 'tracks_enriched.json') -> dict:
        """
        Execute the complete DJ set creation pipeline
        
        Args:
            dataset_path: Path to track dataset
            
        Returns:
            Complete DJ set with justifications
        """
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ SET WORKFLOW STARTED")
        workflow.logger.info("=" * 70)
        
        # Retry policy for all activities
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )
        
        # STEP 1: Load tracks
        workflow.logger.info("Step 1/3: Loading track dataset...")
        
        tracks = await workflow.execute_activity(
            load_tracks_activity,
            dataset_path,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )
        
        workflow.logger.info(f"✓ Loaded {len(tracks)} tracks")
        
        # STEP 2: Sequence tracks
        workflow.logger.info("Step 2/3: Sequencing tracks with greedy algorithm...")
        
        sequenced = await workflow.execute_activity(
            sequence_tracks_activity,
            tracks,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        
        workflow.logger.info(f"✓ Sequenced {len(sequenced)} tracks")
        
        # STEP 3: Generate justifications
        workflow.logger.info("Step 3/3: Generating justifications and analysis...")
        
        justifications = await workflow.execute_activity(
            generate_justifications_activity,
            sequenced,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        
        workflow.logger.info(f"✓ Generated justifications")
        
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ SET WORKFLOW COMPLETED SUCCESSFULLY")
        workflow.logger.info("=" * 70)
        
        return justifications

@workflow.defn
class HelloWorkflow:
    """Simple hello world workflow (from Hour 6)"""
    
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info(f"HelloWorkflow started for: {name}")
        greeting = f"Hello, {name}! Welcome to Temporal DJ Set Curator!"
        workflow.logger.info(f"HelloWorkflow completed: {greeting}")
        return greeting

