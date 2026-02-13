"""
Execute DJ Set Workflow - Hour 7
Demonstrates activity-based workflow execution
"""
import asyncio
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    """
    Execute the DJ Set creation workflow
    """
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    print("=" * 70)
    print("EXECUTING DJ SET WORKFLOW".center(70))
    print("=" * 70)
    print("\nWorkflow: DJSetWorkflow")
    print("Activity: load_tracks_activity")
    print("Dataset:  tracks_enriched.json")
    print("\nWatch progress at: http://localhost:8233")
    print()
    
    # Start the workflow
    result = await client.execute_workflow(
        DJSetWorkflow.run,
        "tracks_enriched.json",         # Workflow argument
        id="dj-set-workflow-hour7",     # Unique workflow ID
        task_queue="dj-set-queue",      # Task queue
    )
    
    print("=" * 70)
    print("WORKFLOW RESULT".center(70))
    print("=" * 70)
    print(f"\nStatus:        {result['status']}")
    print(f"Tracks loaded: {result['tracks_loaded']}")
    print(f"\nSample tracks:")
    
    for i, track in enumerate(result['sample_tracks'], 1):
        print(f"  {i}. {track['track']:30} | {track['artist']:20} | "
              f"{track['bpm']:6.1f} BPM | {track['camelot']}")
    
    print("\n" + "=" * 70)
    print("✓ Workflow completed successfully!".center(70))
    print("Check Temporal UI for execution details".center(70))
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

