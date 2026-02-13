"""
Temporal Worker - Hours 6-7
Runs workflows and activities
"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

# Import workflows
from workflow import DJSetWorkflow, HelloWorkflow

# Import activities
from activities import load_tracks_activity

async def main():
    """
    Start the Temporal worker with activities
    """
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Create worker with both workflows and activities
    worker = Worker(
        client,
        task_queue="dj-set-queue",
        workflows=[DJSetWorkflow, HelloWorkflow],
        activities=[load_tracks_activity],
    )
    
    print("=" * 70)
    print("TEMPORAL WORKER STARTED".center(70))
    print("=" * 70)
    print("\nTask Queue:  dj-set-queue")
    print("\nWorkflows:")
    print("  - DJSetWorkflow")
    print("  - HelloWorkflow")
    print("\nActivities:")
    print("  - load_tracks_activity")
    print("\nPress Ctrl+C to stop")
    print("\n" + "=" * 70)
    
    # Run the worker
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

