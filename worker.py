"""
Temporal Worker - Hour 6
Runs workflows and activities
"""
import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import HelloWorkflow

async def main():
    """
    Start the Temporal worker
    
    The worker:
    1. Connects to Temporal server
    2. Listens for workflow tasks on the "dj-set-queue" task queue
    3. Executes workflows when triggered
    """
    # Connect to Temporal server (running on localhost:7233)
    client = await Client.connect("localhost:7233")
    
    # Create worker that listens on "dj-set-queue"
    worker = Worker(
        client,
        task_queue="dj-set-queue",
        workflows=[HelloWorkflow],
        activities=[],  # No activities yet
    )
    
    print("=" * 70)
    print("TEMPORAL WORKER STARTED".center(70))
    print("=" * 70)
    print("\nListening for workflows on task queue: dj-set-queue")
    print("Worker is ready to execute HelloWorkflow")
    print("\nPress Ctrl+C to stop\n")
    print("=" * 70)
    
    # Run the worker (blocks until stopped)
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())

