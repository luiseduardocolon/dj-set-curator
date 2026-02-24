"""
Monitor Workflow Progress Continuously
Watch progress updates in real-time
"""
import asyncio
import time
from temporalio.client import Client
from workflow import DJSetWorkflow

async def monitor_workflow(workflow_id: str, interval_seconds: int = 1):
    """
    Monitor workflow progress continuously
    
    Args:
        workflow_id: ID of workflow to monitor
        interval_seconds: How often to query (default: 1 second)
    """
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)
    
    print("=" * 70)
    print("REAL-TIME WORKFLOW MONITOR".center(70))
    print("=" * 70)
    print(f"\nWorkflow ID: {workflow_id}")
    print(f"Update interval: {interval_seconds} second(s)")
    print("\nPress Ctrl+C to stop monitoring\n")
    print("=" * 70)
    
    last_status = None
    
    try:
        while True:
            try:
                # Query current progress
                progress = await handle.query(DJSetWorkflow.get_progress)
                
                # Only print if status changed
                current_status = progress['status']
                if current_status != last_status:
                    print(f"\n[{time.strftime('%H:%M:%S')}] Status changed: {current_status}")
                    last_status = current_status
                
                # Print current state
                bar_length = 30
                filled = int((progress['progress_percentage'] / 100) * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                print(f"\r[{bar}] {progress['progress_percentage']:3}% | "
                      f"Step {progress['current_step']}/{progress['total_steps']} | "
                      f"{progress['status']:25} | "
                      f"{progress['elapsed_seconds']}s   ", end='', flush=True)
                
                # Check if completed
                if progress['status'] == 'completed':
                    print("\n\n" + "=" * 70)
                    print("✓ WORKFLOW COMPLETED".center(70))
                    print("=" * 70)
                    print(f"\nFinal Stats:")
                    print(f"  Tracks Loaded:    {progress['tracks_loaded']}")
                    print(f"  Tracks Sequenced: {progress['tracks_sequenced']}")
                    print(f"  Total Time:       {progress['elapsed_seconds']} seconds")
                    print("\n" + "=" * 70)
                    break
                
                # Wait before next query
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                print(f"\n\n⚠ Error querying workflow: {e}")
                break
                
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Monitoring stopped by user".center(70))
        print("=" * 70)

async def main():
    """
    Main entry point - monitor the standard workflow
    """
    workflow_id = "dj-set-workflow-monitored"
    
    print("\nStarting workflow to monitor...")
    print("Workflow will execute while we monitor its progress.\n")
    
    # You could also start the workflow here and monitor it
    # For now, we assume it's already running
    # If you want to start it automatically:
    
    # client = await Client.connect("localhost:7233")
    # await client.start_workflow(
    #     DJSetWorkflow.run,
    #     "tracks_enriched.json",
    #     id=workflow_id,
    #     task_queue="dj-set-queue",
    # )
    
    await monitor_workflow(workflow_id)

if __name__ == "__main__":
    asyncio.run(main())

