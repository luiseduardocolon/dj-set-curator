"""
Temporal Workflows - DJ Set Curator
Complete pipeline with progress tracking (FIXED)
"""
from datetime import timedelta, datetime
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
    Complete DJ Set Creation Workflow with Progress Tracking
    
    Pipeline:
    1. Load tracks from dataset
    2. Sequence tracks using greedy algorithm
    3. Generate justifications and analysis
    
    Progress can be queried in real-time using workflow queries
    """
    
    def __init__(self):
        """Initialize workflow state for progress tracking"""
        self._status = "initializing"
        self._current_step = 0
        self._total_steps = 3
        self._tracks_loaded = 0
        self._tracks_sequenced = 0
        self._start_time = None
    
    @workflow.run
    async def run(self, dataset_path: str = 'tracks_enriched.json') -> dict:
        """
        Execute the complete DJ set creation pipeline
        
        Args:
            dataset_path: Path to track dataset
            
        Returns:
            Complete DJ set with justifications
        """
        # FIXED: Use workflow.now() instead of time.time()
        # This is deterministic and safe for workflows
        self._start_time = workflow.now()
        
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ SET WORKFLOW STARTED")
        workflow.logger.info("=" * 70)
        
        self._status = "running"
        
        # Retry policy for all activities
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=10),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )
        
        # STEP 1: Load tracks
        self._current_step = 1
        self._status = "loading_tracks"
        workflow.logger.info("Step 1/3: Loading track dataset...")
        
        tracks = await workflow.execute_activity(
            load_tracks_activity,
            dataset_path,
            start_to_close_timeout=timedelta(seconds=30),
            retry_policy=retry_policy,
        )
        
        self._tracks_loaded = len(tracks)
        workflow.logger.info(f"✓ Loaded {len(tracks)} tracks")
        
        # STEP 2: Sequence tracks
        self._current_step = 2
        self._status = "sequencing_tracks"
        workflow.logger.info("Step 2/3: Sequencing tracks with greedy algorithm...")
        
        sequenced = await workflow.execute_activity(
            sequence_tracks_activity,
            tracks,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        
        self._tracks_sequenced = len(sequenced)
        workflow.logger.info(f"✓ Sequenced {len(sequenced)} tracks")
        
        # STEP 3: Generate justifications
        self._current_step = 3
        self._status = "generating_justifications"
        workflow.logger.info("Step 3/3: Generating justifications and analysis...")
        
        justifications = await workflow.execute_activity(
            generate_justifications_activity,
            sequenced,
            start_to_close_timeout=timedelta(seconds=60),
            retry_policy=retry_policy,
        )
        
        workflow.logger.info(f"✓ Generated justifications")
        
        # Complete
        self._status = "completed"
        
        workflow.logger.info("=" * 70)
        workflow.logger.info("DJ SET WORKFLOW COMPLETED SUCCESSFULLY")
        workflow.logger.info("=" * 70)
        
        return justifications
    
    @workflow.query
    def get_progress(self) -> dict:
        """
        Query handler: Get current workflow progress
        
        This can be called while the workflow is running to check status
        without interrupting execution.
        
        Returns:
            Dict with current progress information
        """
        # Calculate elapsed time using workflow.now()
        elapsed_seconds = 0
        if self._start_time:
            elapsed = workflow.now() - self._start_time
            elapsed_seconds = int(elapsed.total_seconds())
        
        return {
            "status": self._status,
            "current_step": self._current_step,
            "total_steps": self._total_steps,
            "progress_percentage": int((self._current_step / self._total_steps) * 100),
            "tracks_loaded": self._tracks_loaded,
            "tracks_sequenced": self._tracks_sequenced,
            "elapsed_seconds": elapsed_seconds
        }
    
    @workflow.query
    def get_status(self) -> str:
        """
        Query handler: Get simple status string
        
        Returns:
            Current status (e.g., "loading_tracks", "sequencing_tracks")
        """
        return self._status

@workflow.defn
class HelloWorkflow:
    """Simple hello world workflow (from Hour 6)"""
    
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info(f"HelloWorkflow started for: {name}")
        greeting = f"Hello, {name}! Welcome to Temporal DJ Set Curator!"
        workflow.logger.info(f"HelloWorkflow completed: {greeting}")
        return greeting

