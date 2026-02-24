"""
Demo: Progress Monitoring
Starts a workflow and monitors it in real-time
"""
import asyncio
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    """
    Demo script that:
    1. Starts a workflow
    2. Monitors its progress in real-time
    3. Shows final results
    """
    client = await Client.connect("localhost:7233")
    workflow_id = "dj-set-workflow-monitored-demo"
    
    print("=" * 80)
    print("PROGRESS MONITORING DEMO".center(80))
    print("=" * 80)
    print("\nThis demo will:")
    print("  1. Start a DJ Set workflow")
    print("  2. Monitor its progress in real-time")
    print("  3. Show updates as each step completes")
    print("\n" + "=" * 80)
    
    # Start the workflow (don't wait for result yet)
    handle = await client.start_workflow(
        DJSetWorkflow.run,
        "tracks_enriched.json",
        id=workflow_id,
        task_queue="dj-set-queue",
    )
    
    print(f"\n✓ Workflow started: {workflow_id}")
    print("\nMonitoring progress...\n")
    
    # Monitor progress
    last_step = 0
    
    while True:
        # Query progress
        progress = await handle.query(DJSetWorkflow.get_progress)
        
        # Show update when step changes
        if progress['current_step'] > last_step:
            last_step = progress['current_step']
            print(f"\n[Step {progress['current_step']}/{progress['total_steps']}] {progress['status']}")
            
            if progress['tracks_loaded'] > 0:
                print(f"  → Tracks loaded: {progress['tracks_loaded']}")
            if progress['tracks_sequenced'] > 0:
                print(f"  → Tracks sequenced: {progress['tracks_sequenced']}")
        
        # Progress bar
        bar_length = 50
        filled = int((progress['progress_percentage'] / 100) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r  [{bar}] {progress['progress_percentage']:3}%  ", end='', flush=True)
        
        # Check if completed
        if progress['status'] == 'completed':
            print("\n")
            break
        
        await asyncio.sleep(0.5)
    
    # Get final result
    result = await handle.result()
    
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETED".center(80))
    print("=" * 80)
    
    metrics = result['metrics']
    print(f"\nResults:")
    print(f"  Total tracks:         {metrics['total_tracks']}")
    print(f"  Avg transition score: {metrics['avg_transition_score']:.2f}/1.0")
    print(f"  Total duration:       {metrics['total_duration_minutes']:.1f} minutes")
    print(f"  Execution time:       {progress['elapsed_seconds']} seconds")
    
    print("\n" + "=" * 80)
    print("✓ Demo complete!".center(80))
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

