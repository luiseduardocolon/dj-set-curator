"""
Query Workflow Progress in Real-Time
Demonstrates Temporal's query feature for observability
"""
import asyncio
import sys
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    """
    Query the progress of a running workflow
    """
    # Get workflow ID from command line or use default
    workflow_id = sys.argv[1] if len(sys.argv) > 1 else "dj-set-workflow-complete"
    
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    try:
        handle = client.get_workflow_handle(workflow_id)
        
        print("=" * 70)
        print("QUERYING WORKFLOW PROGRESS".center(70))
        print("=" * 70)
        print(f"\nWorkflow ID: {workflow_id}")
        print()
        
        # Query the progress
        progress = await handle.query(DJSetWorkflow.get_progress)
        
        # Display progress
        print(f"Status:           {progress['status']}")
        print(f"Current Step:     {progress['current_step']}/{progress['total_steps']}")
        print(f"Progress:         {progress['progress_percentage']}%")
        print(f"Tracks Loaded:    {progress['tracks_loaded']}")
        print(f"Tracks Sequenced: {progress['tracks_sequenced']}")
        print(f"Elapsed Time:     {progress['elapsed_seconds']} seconds")
        
        # Visual progress bar
        bar_length = 40
        filled = int((progress['progress_percentage'] / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\nProgress: [{bar}] {progress['progress_percentage']}%")
        
        print("\n" + "=" * 70)
        
        # Also query simple status
        status = await handle.query(DJSetWorkflow.get_status)
        print(f"Simple Status: {status}")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n⚠ Error querying workflow: {e}")
        print("\nTips:")
        print("  - Make sure a workflow is running with ID: " + workflow_id)
        print("  - Run: python run_dj_workflow.py")
        print("  - Or: python demo_progress_monitoring.py")
        print(f"\nUsage: python check_progress.py [workflow_id]")
        print(f"Example: python check_progress.py dj-set-workflow-queryable")

if __name__ == "__main__":
    asyncio.run(main())

