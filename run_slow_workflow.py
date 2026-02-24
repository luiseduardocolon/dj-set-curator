"""
Start a workflow you can query while it runs
Uses the demo workflow which shows progress updates
"""
import asyncio
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    
    print("Starting workflow: dj-set-workflow-queryable")
    print("\nRun this in another terminal to query it:")
    print("  python check_progress.py")
    print()
    
    result = await client.execute_workflow(
        DJSetWorkflow.run,
        "tracks_enriched.json",
        id="dj-set-workflow-queryable",
        task_queue="dj-set-queue",
    )
    
    print("\n✓ Workflow completed!")

if __name__ == "__main__":
    asyncio.run(main())

