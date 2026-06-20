"""Small Mem0 wrapper with a deterministic offline fallback for the demo."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

from simulated_sessions import PATIENT_ID, SESSIONS


@dataclass(frozen=True)
class MemoryFact:
    id: str
    category: str
    memory: str
    display: str
    session: int
    source: str
    keywords: tuple[str, ...]


def fact_from_session(session_id: int, raw_fact: dict) -> MemoryFact:
    return MemoryFact(
        id=raw_fact["id"],
        category=raw_fact["category"],
        memory=raw_fact["memory"],
        display=raw_fact["display"],
        session=session_id,
        source=f"Session {session_id}",
        keywords=tuple(raw_fact.get("keywords", [])),
    )


def session_facts(session_id: int) -> list[MemoryFact]:
    return [fact_from_session(session_id, fact) for fact in SESSIONS[session_id]["facts"]]


def add_session_to_memory(
    existing_memories: Iterable[MemoryFact],
    session_id: int,
    *,
    use_real_mem0: bool = False,
) -> tuple[list[MemoryFact], str]:
    """Simulate mem0.add() and optionally mirror the transcript to a live Mem0 project."""

    memories = list(existing_memories)
    existing_ids = {fact.id for fact in memories}
    new_facts = [fact for fact in session_facts(session_id) if fact.id not in existing_ids]

    status = "offline_demo"
    if use_real_mem0 and os.getenv("MEM0_API_KEY"):
        status = _try_live_add(session_id)

    return memories + new_facts, status


def search_memories(
    memories: Iterable[MemoryFact],
    query: str,
    *,
    limit: int = 10,
    use_real_mem0: bool = False,
) -> tuple[list[MemoryFact], str]:
    """Simulate mem0.search() with keyword scoring, optionally probing live Mem0."""

    facts = list(memories)
    status = "offline_demo"
    if use_real_mem0 and os.getenv("MEM0_API_KEY"):
        status = _try_live_search(query)

    priority_ids = [
        "dx-history",
        "sertraline-gi",
        "grounding-severity",
        "treatment-goal",
        "sleep-decline",
        "sunday-trigger",
        "sunday-sleep-monday",
        "box-breathing",
        "pmr-abandoned",
        "direct-style",
    ]
    priority = {memory_id: index for index, memory_id in enumerate(priority_ids)}
    query_terms = {
        token.strip(".,:;!?()").lower()
        for token in query.split()
        if len(token.strip(".,:;!?()")) > 3
    }

    def score(fact: MemoryFact) -> tuple[int, int, int]:
        haystack = set(fact.keywords) | set(fact.memory.lower().split())
        overlap = len(query_terms & haystack)
        ranked_position = priority.get(fact.id, 999)
        has_demo_priority = 1 if fact.id in priority else 0
        return has_demo_priority, -ranked_position, overlap

    ranked = sorted(facts, key=score, reverse=True)
    return ranked[:limit], status


def grouped_memories(memories: Iterable[MemoryFact]) -> dict[str, list[MemoryFact]]:
    groups: dict[str, list[MemoryFact]] = {}
    for fact in memories:
        groups.setdefault(fact.category, []).append(fact)
    return groups


def seed_all_memories() -> list[MemoryFact]:
    seeded: list[MemoryFact] = []
    for session_id in sorted(SESSIONS):
        seeded.extend(session_facts(session_id))
    return seeded


def _try_live_add(session_id: int) -> str:
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
        client.add(
            [{"role": "user", "content": SESSIONS[session_id]["transcript"]}],
            user_id=PATIENT_ID,
            metadata={"source": f"therapy_session_{session_id}", "demo": "therapy_handoff"},
        )
        return "live_mem0"
    except Exception:
        return "live_mem0_unavailable"


def _try_live_search(query: str) -> str:
    try:
        from mem0 import MemoryClient

        client = MemoryClient(api_key=os.environ["MEM0_API_KEY"])
        client.search(query, filters={"user_id": PATIENT_ID})
        return "live_mem0"
    except Exception:
        return "live_mem0_unavailable"
