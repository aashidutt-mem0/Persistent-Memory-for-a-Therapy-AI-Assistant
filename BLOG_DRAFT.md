# Patient Memory Handoff with Mem0: From Therapy Sessions to Psychiatry Intake

Author: Aashi Dutt

## Quick Takeaways

The previous post covered the architecture problem: therapy AI systems can capture session notes, but they often cannot retrieve the right fact at the right time. After enough sessions, clinically useful details get buried. At referral, those details get compressed into a short letter.

This post shows the same problem as a runnable demo.

In the demo, a fictional patient named Alex has three therapy sessions. Mem0 extracts structured facts after each session: panic triggers, medication side effects, coping strategies, sleep trends, treatment goals, and allergies.

Then Alex is referred to psychiatry. The referral letter preserves only four sentences. The memory store preserves fourteen structured facts.

The payoff is the intake screen: same patient message, two different assistants. One only has the referral letter and asks Alex to repeat everything. The other retrieves relevant Mem0 memories first and opens with the clinical context already in place.

Get a free API key at app.mem0.ai to follow along. The demo works offline by default, and can also mirror `add()` and `search()` calls to Mem0.

## Why build a demo for this?

In healthcare AI, the phrase "persistent memory" can sound abstract. It becomes obvious when you put it next to the current handoff workflow.

Most provider handoffs still look like this:

```text
Therapy sessions -> referral letter -> psychiatry intake
```

That sounds reasonable until you inspect what gets lost.

The therapist may know that:

- sertraline caused GI side effects, specifically nausea and diarrhea,
- grounding works for mild panic but not severe episodes,
- progressive muscle relaxation was tried and abandoned,
- sleep is averaging 5.2 hours and declining,
- Sunday evenings are the trigger pattern,
- the treatment goal is to reduce panic attacks from 3/week to less than 1/week,
- the patient responds better to direct communication.

The referral letter may say:

```text
Alex is being treated for panic disorder and generalized anxiety disorder.
Alex tried sertraline and discontinued it due to side effects.
Alex is currently using CBT techniques with partial success.
Referring for medication evaluation.
```

That is not wrong. It is just too compressed.

For a psychiatrist, "discontinued due to side effects" is not enough. Which side effects? GI or neurological? Did the medication fail, or was tolerability the issue? Which coping strategies are still useful? Is sleep getting better or worse?

The demo makes that compression visible.

## Demo Flow

The app has two tabs:

1. Therapy Sessions
2. Handoff

The top row gives the whole system state:

```text
Structured facts stored: 14
Source: 3 therapy sessions, 1 provider
Referral letter: 4 sentences
Retrievable in: <2 seconds, ~7,000 tokens/query
```

The point is simple: the referral letter is small because it is compressed. The memory store is small because it is structured.

## Step 1: Build Memory Across Therapy Sessions

The demo starts with three pre-filled therapy transcripts.

Session 3 captures the first important facts:

- panic attacks correlate with Sunday evenings,
- sertraline 50mg was stopped in week 3 because of GI side effects,
- CBT grounding was introduced,
- Alex has a penicillin allergy.

When the user clicks `Save Session 3`, the app runs the equivalent of:

```python
from mem0 import MemoryClient
import os

mem0 = MemoryClient(api_key=os.environ["MEM0_API_KEY"])

mem0.add(
    [
        {
            "role": "user",
            "content": session_3_transcript
        }
    ],
    user_id="alex-rivera",
    agent_id="therapist",
    run_id="session_3",
    metadata={
        "provider": "dr_chen",
        "session_type": "therapy",
        "session_number": 3
    }
)
```

The important architectural move is not saving the transcript. It is extracting facts that can be retrieved later.

By the end of Session 11, the memory store contains fourteen facts across diagnosis, medications, coping strategies, treatment goals, triggers, sleep, preferences, and allergies.

The therapist does not need to remember where each detail appeared. The application does not need to replay three transcripts. The facts are independently retrievable.

## Step 2: Show the Compression Gap

The Handoff tab generates a realistic referral letter.

It looks normal:

```text
Dear Psychiatry Team,

I am referring Alex Rivera for medication evaluation. Alex is being treated
for panic disorder and generalized anxiety disorder. Alex tried sertraline
and discontinued it due to side effects. Alex is currently using CBT
techniques with partial success.

Sincerely,
Dr. Maya Chen
```

But next to the letter, the UI shows what was lost:

- which side effects: GI symptoms, not neurological symptoms,
- which coping strategies work for which severity,
- sleep trend: 5.2 hours average and declining,
- Sunday night trigger pattern.

This is the handoff failure mode.

The referral letter is not useless. It is useful as a human-readable summary. But it should not be the primary context source for an AI intake assistant.

The primary context source should be queryable memory.

## Step 3: Run the Intake Comparison

The demo uses the same patient message in both panels:

```text
Hi, I'm here for the medication evaluation.
```

### Without Mem0

The assistant only has the referral letter.

```text
Welcome Alex. Can you tell me about your mental health history?
What medications have you tried before?
```

This is the familiar experience. The patient repeats the context.

### With Mem0

Before responding, the assistant retrieves relevant patient memories:

```python
context = mem0.search(
    "mental health history medications coping strategies treatment goals",
    filters={"user_id": "alex-rivera"},
    top_k=10
)
```

The retrieved memories include:

```text
- Panic disorder and generalized anxiety disorder
- Sertraline 50mg stopped week 3 - GI side effects (nausea, diarrhea)
- CBT grounding effective for mild episodes, less for severe attacks
- Reduce panic attacks from 3/wk to <1/wk, current: 2.4/wk
- Averaging 5.2 hours/night, declining over 3 weeks
- Panic attacks correlate with Sunday evenings
- PMR tried in session 7, patient found it unhelpful
- Responds better to direct communication style
```

Now the assistant can open differently:

```text
I can see you've been working with Dr. Chen on panic disorder and GAD.
Sertraline caused GI issues - nausea and diarrhea specifically.
Grounding techniques help with mild episodes but not severe ones.
Your attacks are down from 3 to about 2.4 per week, but sleep has been
declining, especially Sunday nights. Let's talk about medication options
that avoid the GI side effects.
```

Same patient message. Different context architecture.

## What developers should notice

This is not a prompt-engineering trick.

The difference is the memory layer.

The referral-only assistant has:

```text
4 sentences of manually compressed context
```

The Mem0-backed assistant has:

```text
10 retrieved facts selected from 14 structured memories
```

That is the core pattern:

```text
session transcript -> mem0.add() -> structured memory
intake message -> mem0.search() -> relevant memory injection
```

The application does not need to stuff all historical notes into the prompt. It asks a narrow question and injects only the relevant facts.

This matters for three reasons:

- Lower tokens: retrieval uses a small memory set instead of full-context replay.
- Better precision: medication side effects, triggers, and treatment goals survive handoff.
- Better UX: patients do not have to repeat longitudinal history at every provider transition.

## Why this is different from summarization

Summaries compress. Memory retrieves.

A summary asks:

```text
What is the shortest version of everything that happened?
```

Memory asks:

```text
What facts are relevant to this query right now?
```

Those are different operations.

For a referral letter, the shortest useful version may be:

```text
Tried sertraline, discontinued due to side effects.
```

For a psychiatry intake query, the relevant memory is:

```text
Sertraline 50mg was stopped in week 3 because of GI side effects:
nausea and diarrhea.
```

That extra specificity changes the next clinical question.

## How the demo is structured

The repo is intentionally small:

```text
therapy-memory-demo/
├── streamlit_app.py        # two-tab UI
├── mem0_helpers.py         # add/search wrappers
├── simulated_sessions.py   # fictional therapy transcripts
├── requirements.txt
├── .env.example
└── README.md
```

The offline mode is deterministic so the demo is reliable in a live walkthrough.

The live mode mirrors calls to Mem0:

```bash
MEM0_DEMO_MODE=live
MEM0_API_KEY=your-mem0-api-key
```

Then run:

```bash
streamlit run streamlit_app.py
```

The UI stays deterministic, but the app also calls `MemoryClient.add()` and `MemoryClient.search()` behind the scenes.

## Production architecture

In production, the pattern is the same.

After every therapy session:

```python
mem0.add(
    session_notes,
    user_id=patient_mrn,
    agent_id="therapist",
    run_id=f"session_{session_id}",
    metadata={
        "provider": "dr_chen",
        "session_type": "therapy"
    }
)
```

Before psychiatry intake:

```python
context = mem0.search(
    "medication history reactions side effects coping strategies treatment goals",
    filters={"user_id": patient_mrn},
    top_k=10
)
```

Then inject the retrieved facts into the intake assistant's system context.

The referral letter can still exist. Clinicians need readable summaries. But the AI assistant should not depend on that letter as its only memory source.

## Compliance note

This demo uses fictional data.

For real mental health workflows, memory architecture must support:

- extracted facts instead of raw psychotherapy transcripts,
- consent-gated retrieval,
- audit logging for every `add()` and `search()` call,
- scoped access by patient, provider role, session, and organization,
- managed cloud, private cloud, or on-prem deployment depending on the organization's requirements.

The key design principle is minimum necessary retrieval. A psychiatry intake assistant should retrieve medication history, symptoms, treatment goals, sleep trends, and relevant coping strategies. It should not receive an entire therapy transcript unless the patient and clinical workflow explicitly allow it.

## Conclusion

The previous post made the architecture case: clinical AI needs persistent memory because session notes get buried, referral letters are lossy, and prose notes are hard to query.

This demo makes the case visually.

The user sees fourteen facts accumulated across therapy sessions. Then they see those facts compressed into a four-sentence referral letter. Then they see the intake assistant behave differently when it can retrieve the original structured memories.

That is the product moment:

```text
The patient does not repeat themselves.
The provider starts with context.
The AI assistant retrieves what matters.
```

Start free at app.mem0.ai and try the same `add()` and `search()` flow with your own patient workflow.

