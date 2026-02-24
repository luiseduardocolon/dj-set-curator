cat > README.md << 'EOF'
# 🎵 DJ Set Curator - Temporal Workflow Demo

**AI-powered DJ set sequencing with Temporal orchestration**

Built to leverage Temporal - demonstrates workflow patterns, fault tolerance, and observability.

[![Temporal](https://img.shields.io/badge/Temporal-Workflow-blue)](https://temporal.io)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)

---

## 🎯 What This Does

Creates optimized DJ sets using:
- **Harmonic mixing** (Camelot Wheel key compatibility)
- **BPM matching** (tempo transitions)
- **Energy progression** (crowd dynamics)
- **Strategic banger placement** (popularity optimization)

**Powered by Temporal** for fault-tolerant, observable, scalable execution.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Temporal CLI (`brew install temporal`)

### Setup
```bash
# Clone the repo
git clone https://github.com/luiseduardocolon/dj-set-curator.git
cd dj-set-curator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run It

**Terminal 1 - Start Temporal:**
```bash
temporal server start-dev
```

**Terminal 2 - Start Worker:**
```bash
python worker.py
```

**Terminal 3 - Run Workflow:**
```bash
# Complete pipeline with progress monitoring
python demo_progress_monitoring.py

# Or just run the workflow
python run_dj_workflow.py

# Query progress while running
python check_progress.py
```

**Terminal 4 - View Results:**
```bash
# Open Temporal Web UI
open http://localhost:8233

# Check generated DJ set
cat temporal_workflow_result.json
```

---

## 📊 Vanilla vs. Temporal Comparison

### Vanilla Python Pipeline (Hours 1-5)

**Files:**
- `fetch_tracks.py` - Load dataset
- `camelot.py` - Key conversion
- `scoring.py` - Compatibility scoring
- `sequencer.py` - Greedy algorithm
- `justifier.py` - Generate explanations

**Limitations:**
- ❌ No retry logic
- ❌ No crash recovery
- ❌ No observability
- ❌ Manual error handling
- ❌ Monolithic execution

### Temporal Workflow (Hours 6-10)

**Files:**
- `workflow.py` - Workflow orchestration
- `activities.py` - Fault-tolerant activities
- `worker.py` - Workflow executor

**Benefits:**
- ✅ Automatic retries (3 attempts with exponential backoff)
- ✅ Crash recovery (resume from any step)
- ✅ Real-time observability (query progress anytime)
- ✅ Scalable (distribute activities across workers)
- ✅ Debuggable (complete execution history)

**Example:**
```python
# If sequencing fails, Temporal automatically retries
# If worker crashes, workflow resumes from last checkpoint
# Query progress without interrupting execution
progress = await handle.query(DJSetWorkflow.get_progress)
```

---

## 🏗️ Architecture

### Workflow Structure
```
DJSetWorkflow
├── Activity 1: load_tracks_activity
│   └── Loads 20 tracks from JSON dataset
├── Activity 2: sequence_tracks_activity
│   └── Runs greedy algorithm (multi-factor optimization)
└── Activity 3: generate_justifications_activity
    └── Creates transition explanations & analysis
```

### Multi-Factor Scoring System

Each transition scored on 4 factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Harmonic** | 40% | Camelot wheel key compatibility |
| **BPM** | 30% | Tempo matching (≤6% change ideal) |
| **Energy** | 20% | Crowd energy progression |
| **Popularity** | 10% | Strategic banger placement |

**Example Transition:**
```
Billie Jean (11A, 117 BPM) → Get Lucky (11A, 116 BPM)

Harmonic:   1.00/1.0 (perfect match - same key)
BPM:        0.90/1.0 (0.9% change - imperceptible)
Energy:     0.80/1.0 (maintains momentum)
Popularity: 0.60/1.0 (high-pop track)

TOTAL:      0.85/1.0 (excellent transition)
```

---

## 🎛️ Algorithm: Greedy Sequencing

**Approach:**
1. Start with highest-popularity track (strong opener)
2. At each step, pick the best-scoring unplayed track
3. Consider set position for popularity weighting (35-65% = peak zone)
4. Continue until all tracks sequenced

**Results:**
- **+36.5%** better avg transition scores vs. BPM-only
- **8 fewer** harmonic violations (6 vs. 14)
- **Ideal energy arc** (peak in middle)

**Performance:**
- 20 tracks sequenced in <1 second
- Avg transition score: **0.71/1.0**

---

## 📈 Observability Features

### Real-Time Progress Queries
```python
# Query workflow progress without interrupting
progress = await handle.query(DJSetWorkflow.get_progress)

# Returns:
{
  "status": "sequencing_tracks",
  "current_step": 2,
  "total_steps": 3,
  "progress_percentage": 66,
  "tracks_loaded": 20,
  "tracks_sequenced": 20,
  "elapsed_seconds": 5
}
```

### Monitoring Scripts

- `check_progress.py` - One-time progress snapshot
- `monitor_progress.py` - Continuous monitoring loop
- `demo_progress_monitoring.py` - Full demo with visualization

### Web UI

View execution timeline at http://localhost:8233:
- ✅ Activity execution history
- ✅ Retry attempts
- ✅ Input/output data
- ✅ Logs from each activity

---

## 🎵 Sample Output

**Opening Sequence:**
```
1. Billie Jean          | Michael Jackson  | 117.0 BPM | 11A | Pop: 97
2. Get Lucky            | Daft Punk        | 116.0 BPM | 11A | Pop: 89
3. Uptown Funk          | Bruno Mars       | 115.0 BPM | 7A  | Pop: 95
4. 24K Magic            | Bruno Mars       | 107.0 BPM | 10A | Pop: 87
5. Good Times           | Chic             | 109.0 BPM | 9A  | Pop: 76
```

**Peak Energy (Middle):**
```
10. September           | Earth, Wind...   | 126.0 BPM | 11B | Pop: 92
11. I Wanna Dance...    | Whitney Houston  | 119.0 BPM | 11A | Pop: 88
12. Stayin' Alive       | Bee Gees         | 104.0 BPM | 2A  | Pop: 91
```

**Set Metrics:**
- Total Duration: **81.8 minutes**
- Avg Transition Score: **0.71/1.0**
- Harmonic Violations: **6/19 transitions** (32%)

---

## 🛠️ Development Timeline

Built in 14 hours as a structured learning project:

**Day 1 - Vanilla Pipeline (Hours 0-5):**
- Hour 0: GitHub repo setup
- Hour 1: Dataset creation (pivoted from Spotify API lockdown)
- Hour 2: Camelot wheel implementation
- Hour 3: Multi-factor scoring system
- Hour 4: Greedy sequencing algorithm
- Hour 5: Justification engine

**Day 2 - Temporal Integration (Hours 6-10):**
- Hour 6: Temporal setup + Hello World
- Hour 7: Convert track loading to activity
- Hour 8: Complete activity-based pipeline
- Hour 9: Progress tracking & queries
- Hour 10: Documentation & comparison

---

## 📝 Key Learnings

### Temporal Best Practices

**1. Determinism is Critical:**
```python
# ❌ Non-deterministic (causes errors)
import time
elapsed = time.time() - start_time

# ✅ Deterministic (workflow-safe)
elapsed = workflow.now() - self._start_time
```

**2. Activities for Side Effects:**
- File I/O → Activity
- API calls → Activity
- Database operations → Activity
- Pure computation → Can be in workflow or activity

**3. Retry Policies:**
```python
RetryPolicy(
    initial_interval=timedelta(seconds=1),
    maximum_interval=timedelta(seconds=10),
    backoff_coefficient=2.0,
    maximum_attempts=3,
)
```

### Algorithmic Insights

**1. Greedy is Good Enough:**
- Perfect optimization (TSP-like) is NP-hard
- Greedy achieves 36% improvement over naive
- Executes in <1 second for 20 tracks

**2. Multi-Factor Beats Single-Factor:**
- BPM-only: 0.52/1.0 avg score
- Multi-factor: 0.71/1.0 avg score
- Harmonic compatibility is most important (40% weight)

**3. Position-Aware Scoring:**
- Placing bangers at peaks (35-65%) maximizes impact
- Early/late bangers are "wasted"

---

## 🎯 Interview Talking Points

### Why Temporal?

**Before (Vanilla):**
- "If the sequencing crashes halfway, start over"
- "No way to track progress"
- "Hope nothing fails"

**After (Temporal):**
- "Workflow resumes from checkpoint on crash"
- "Query progress anytime without interrupting"
- "Automatic retries with exponential backoff"

### Real-World Applications

This pattern applies to:
- **ETL pipelines** (data extraction → transform → load)
- **Order processing** (payment → inventory → shipping)
- **Content moderation** (detect → review → action)
- **ML pipelines** (preprocess → train → deploy)

Anywhere you have multi-step processes that need:
- Fault tolerance
- Observability
- Scalability

---

## 📂 Project Structure
```
dj-set-curator/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
│
├── tracks_dataset.json          # 20 curated tracks
├── tracks_enriched.json         # With Camelot keys
│
├── vanilla/                     # Original pipeline (Hours 1-5)
│   ├── fetch_tracks.py
│   ├── camelot.py
│   ├── scoring.py
│   ├── sequencer.py
│   └── justifier.py
│
├── temporal/                    # Temporal implementation (Hours 6-10)
│   ├── workflow.py              # Workflow definitions
│   ├── activities.py            # Activity implementations
│   ├── worker.py                # Worker process
│   ├── run_dj_workflow.py       # Execute workflow
│   ├── check_progress.py        # Query progress
│   ├── monitor_progress.py      # Continuous monitoring
│   └── demo_progress_monitoring.py  # Full demo
│
└── outputs/
    ├── sequence_optimized.json  # Generated DJ set
    ├── set_with_justifications.txt  # Full analysis
    └── temporal_workflow_result.json  # Workflow output
```

## 📁 File Organization

**Core Temporal Files (use these):**
- `workflow.py` - Workflow definitions
- `activities.py` - Activity implementations  
- `worker.py` - Worker process
- `run_dj_workflow.py` - Execute workflow
- `demo_progress_monitoring.py` - Full demo

**Vanilla Pipeline (reference):**
- `camelot.py`, `scoring.py`, `sequencer.py`, `justifier.py`

**Utilities:**
- `check_progress.py` - Query workflow
- `compare_approaches.py` - Vanilla vs Temporal comparison

**Data:**
- `tracks_enriched.json` - Input dataset
- `temporal_workflow_result.json` - Output results

---

## 🤝 Contributing

This is a demo project, but your feedback is welcomed!

**Contact:** Luis Eduardo Colón
**GitHub:** https://github.com/luiseduardocolon

---

## 📄 License

MIT License - See LICENSE file

---

## 🙏 Acknowledgments

- **Temporal.io** - Workflow orchestration platform
- **Anthropic Claude** - Development assistance
- **Mixed In Key** - Camelot Wheel system inspiration

---

**Built with ❤️ for the benefit of others**
