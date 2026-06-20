# Patient Memory Handoff with Mem0

Streamlit demo showing how Mem0 preserves patient context across therapy sessions and a psychiatry handoff.

## Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The default mode is deterministic and offline. It simulates `mem0.add()` and `mem0.search()` so the demo is reliable during live presentations.

## Optional live Mem0 mode

```bash
cp .env.example .env
```

Then set:

```bash
MEM0_DEMO_MODE=live
MEM0_API_KEY=your-mem0-api-key
```

In live mode, the app mirrors session transcripts to Mem0 with `MemoryClient.add()` and probes `MemoryClient.search()`, while keeping the UI output deterministic for a crisp demo.

## Flow

1. **Therapy Sessions** - save Sessions 3, 7, and 11 to build 14 structured facts.
2. **Handoff** - generate the compressed referral and compare referral-only intake with Mem0-backed intake.

Source and retrieval proof are shown in the top metrics row.
