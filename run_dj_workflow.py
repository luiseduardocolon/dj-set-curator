"""
Execute Complete DJ Set Workflow
Demonstrates full pipeline execution
"""
import asyncio
import json
from temporalio.client import Client
from workflow import DJSetWorkflow

async def main():
    """
    Execute the complete DJ Set creation workflow
    """
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    print("=" * 80)
    print("EXECUTING COMPLETE DJ SET WORKFLOW".center(80))
    print("=" * 80)
    print("\nPipeline Steps:")
    print("  1. Load tracks from dataset")
    print("  2. Sequence tracks using greedy algorithm")
    print("  3. Generate justifications and analysis")
    print("\nWatch progress at: http://localhost:8233")
    print()
    
    # Start the workflow
    result = await client.execute_workflow(
        DJSetWorkflow.run,
        "tracks_enriched.json",
        id="dj-set-workflow-complete",
        task_queue="dj-set-queue",
    )
    
    # Display results
    print("=" * 80)
    print("WORKFLOW COMPLETED - RESULTS".center(80))
    print("=" * 80)
    
    metrics = result['metrics']
    print(f"\nSet Metrics:")
    print(f"  Total tracks:        {metrics['total_tracks']}")
    print(f"  Total duration:      {metrics['total_duration_minutes']:.1f} minutes")
    print(f"  Avg transition score: {metrics['avg_transition_score']:.2f}/1.0")
    
    print(f"\nOpening Sequence (First 5 tracks):")
    for i, track in enumerate(result['sequence'][:5], 1):
        print(f"  {i}. {track['track']:30} | {track['artist']:20} | "
              f"{track['bpm']:6.1f} BPM | {track['camelot']}")
    
    print(f"\nClosing Sequence (Last 3 tracks):")
    for i, track in enumerate(result['sequence'][-3:], len(result['sequence'])-2):
        print(f"  {i}. {track['track']:30} | {track['artist']:20} | "
              f"{track['bpm']:6.1f} BPM | {track['camelot']}")
    
    # Show some transition scores
    print(f"\nSample Transition Scores:")
    for i, trans in enumerate(result['transitions'][:3], 1):
        print(f"  {trans['from_track']} → {trans['to_track']}")
        print(f"    Overall: {trans['scores']['total']:.2f} | "
              f"Harmonic: {trans['scores']['harmonic']:.2f} | "
              f"BPM: {trans['scores']['bpm']:.2f}")
    
    # Save complete result to file
    with open('temporal_workflow_result.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print("\n" + "=" * 80)
    print("✓ Complete DJ set generated successfully!".center(80))
    print("Full results saved to: temporal_workflow_result.json".center(80))
    print("Check Temporal UI for execution timeline".center(80))
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())

