"""
Test retry behavior - demonstrates fault tolerance
"""
import asyncio
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    
    print("Testing retry behavior with invalid file path...")
    print("This will fail 3 times, then the workflow will fail.\n")
    
    try:
        result = await client.execute_workflow(
            DJSetWorkflow.run,
            "nonexistent_file.json",  # This will fail!
            id="dj-set-workflow-retry-test",
            task_queue="dj-set-queue",
        )
    except Exception as e:
        print(f"Workflow failed as expected: {e}")
        print("\n✓ Check the Web UI to see 3 retry attempts!")
        print("   URL: http://localhost:8233")

if __name__ == "__main__":
    asyncio.run(main())

