"""
Temporal Workflow Executor - Hour 6
Starts workflows and retrieves results
"""
import asyncio
from temporalio.client import Client
from workflow import HelloWorkflow

async def main():
    """
    Execute the HelloWorkflow
    """
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    print("=" * 70)
    print("EXECUTING HELLO WORKFLOW".center(70))
    print("=" * 70)
    print()
    
    # Start the workflow
    result = await client.execute_workflow(
        HelloWorkflow.run,
        "DJ Set Curator Developer",  # Workflow argument
        id="hello-workflow-1",        # Unique workflow ID
        task_queue="dj-set-queue",    # Task queue to use
    )
    
    print(f"Workflow result: {result}")
    print()
    print("=" * 70)
    print("✓ Workflow completed successfully!".center(70))
    print("Check the Temporal Web UI at http://localhost:8233".center(70))
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

