import os

import streamlit as st
from dotenv import load_dotenv

from mem0_helpers import (
    add_session_to_memory,
    search_memories,
)
from simulated_sessions import MISSED_DETAILS, REFERRAL_LETTER, SESSIONS


load_dotenv()

st.set_page_config(
    page_title="Patient Memory Handoff with Mem0",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


CSS = """
<style>
:root {
  --ink: #17202a;
  --muted: #657180;
  --line: #d9e1ea;
  --mint: #e7f7ee;
  --mint-border: #91d8ae;
  --rose: #fff0f1;
  --rose-border: #f29aa3;
  --blue: #eaf3ff;
  --blue-border: #9fc5f8;
  --amber: #fff6df;
  --amber-border: #e8c66c;
}
.main .block-container {
  padding-top: 1.4rem;
  max-width: 1280px;
}
div[data-testid="stMetric"] {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px 14px;
  background: #ffffff;
}
.demo-header {
  border-bottom: 1px solid var(--line);
  padding-bottom: 12px;
  margin-bottom: 12px;
}
.demo-title {
  color: var(--ink);
  font-size: 2.1rem;
  font-weight: 760;
  line-height: 1.08;
  margin: 4px 0 4px;
}
.transcript {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #fbfcfe;
  padding: 16px;
  max-height: 340px;
  overflow-y: auto;
  white-space: pre-wrap;
  color: #243040;
  line-height: 1.45;
}
.fact-card {
  border: 1px solid var(--mint-border);
  background: var(--mint);
  color: #174d2d;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 0;
  font-weight: 620;
}
.miss-card {
  border: 1px solid var(--rose-border);
  background: var(--rose);
  color: #842029;
  border-radius: 8px;
  padding: 8px 10px;
  margin: 6px 0;
  font-weight: 620;
  font-size: 0.94rem;
}
.note-card {
  border: 1px solid var(--blue-border);
  background: var(--blue);
  border-radius: 8px;
  padding: 14px 16px;
  margin: 12px 0;
  color: #1d3d61;
}
.compare-card {
  border: 1px solid var(--amber-border);
  background: var(--amber);
  border-radius: 8px;
  padding: 12px;
  font-size: 0.98rem;
  color: #58430d;
}
.letter-card {
  border: 1px solid var(--line);
  background: #f7f9fb;
  border-radius: 8px;
  padding: 14px;
  color: #303846;
  line-height: 1.45;
}
.query-chip {
  border: 1px solid var(--line);
  background: #fbfcfe;
  border-radius: 8px;
  padding: 10px 12px;
  color: #303846;
  margin: 8px 0 14px;
}
.panel {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 16px;
  background: #ffffff;
  min-height: 290px;
}
.panel-left {
  border-top: 5px solid #a8b4c2;
}
.panel-right {
  border-top: 5px solid #44a06c;
}
.panel-title {
  font-weight: 760;
  color: var(--ink);
  font-size: 1.15rem;
  margin-bottom: 8px;
}
.response {
  background: #f7f9fb;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  min-height: 120px;
  line-height: 1.5;
}
.memory-row {
  border-bottom: 1px solid #edf1f5;
  padding: 8px 0;
}
.memory-row:last-child {
  border-bottom: 0;
}
.small-muted {
  color: var(--muted);
  font-size: 0.92rem;
}
.stButton > button, .stLinkButton > a {
  border-radius: 8px;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def init_state():
    defaults = {
        "memories": [],
        "saved_sessions": [],
        "last_new_facts": {},
        "referral_generated": False,
        "intake_generated": False,
        "use_real_mem0": os.getenv("MEM0_DEMO_MODE", "offline").lower() == "live",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_fact_card(text: str):
    st.markdown(f'<div class="fact-card">✓ {text}</div>', unsafe_allow_html=True)


def render_miss_card(text: str):
    st.markdown(f'<div class="miss-card">✗ {text}</div>', unsafe_allow_html=True)


def render_header():
    saved_count = len(st.session_state.saved_sessions)
    fact_count = len(st.session_state.memories)
    st.markdown(
        """
        <div class="demo-header">
          <div class="demo-title">Patient Memory Handoff with Mem0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1])
    col1.metric("Structured facts stored", fact_count, f"across {saved_count} sessions")
    col2.metric("Source", "3 therapy sessions", "1 provider")
    col3.metric("Referral letter", "4 sentences", "manual handoff")
    col4.metric("Retrievable in", "<2 seconds", "~7,000 tokens/query")


def status_caption(status: str):
    if status == "live_mem0":
        st.caption("mem0.add() completed against the configured Mem0 project.")
    elif status == "live_mem0_unavailable":
        st.caption("Live Mem0 was requested but unavailable, so the deterministic local demo store continued.")
    else:
        st.caption("mem0.add() simulated locally for a repeatable demo. Set MEM0_DEMO_MODE=live with MEM0_API_KEY to mirror calls to Mem0.")


def therapy_tab():
    st.subheader("1. Therapy Sessions")

    left, right = st.columns([1.15, 0.85], gap="large")
    next_session = next((sid for sid in sorted(SESSIONS) if sid not in st.session_state.saved_sessions), None)

    with left:
        if next_session is None:
            st.success("All three therapy sessions are stored.")
            selected = st.selectbox(
                "Review saved transcript",
                sorted(SESSIONS),
                format_func=lambda sid: SESSIONS[sid]["title"],
            )
        else:
            selected = next_session
            st.info(f"Next up: {SESSIONS[selected]['title']}")

        session = SESSIONS[selected]
        st.markdown(f"**{session['title']}**")
        st.caption(f"{session['date']} · {session['summary']}")
        st.markdown(f'<div class="transcript">{session["transcript"]}</div>', unsafe_allow_html=True)

        if selected not in st.session_state.saved_sessions:
            if st.button(f"Save Session {selected}", type="primary", use_container_width=True):
                with st.spinner("Running mem0.add() and extracting structured facts..."):
                    memories, status = add_session_to_memory(
                        st.session_state.memories,
                        selected,
                        use_real_mem0=st.session_state.use_real_mem0,
                    )
                st.session_state.memories = memories
                st.session_state.saved_sessions.append(selected)
                st.session_state.last_new_facts[selected] = [
                    fact for fact in memories if fact.session == selected
                ]
                st.session_state.last_status = status
                st.rerun()
        else:
            st.button(f"Session {selected} saved", disabled=True, use_container_width=True)

    with right:
        st.markdown("**Extracted facts**")
        if st.session_state.last_new_facts:
            latest_session = max(st.session_state.last_new_facts)
            st.caption(f"Most recent mem0.add(): Session {latest_session}")
            shown_facts = st.session_state.last_new_facts[latest_session]
            if latest_session == 3:
                session_3_highlights = {
                    "sunday-trigger",
                    "sertraline-gi",
                    "grounding-introduced",
                    "penicillin-allergy",
                }
                shown_facts = [fact for fact in shown_facts if fact.id in session_3_highlights]
            for fact in shown_facts:
                render_fact_card(fact.display)
            hidden_count = len(st.session_state.last_new_facts[latest_session]) - len(shown_facts)
            if hidden_count:
                st.caption(f"{hidden_count} additional patient-history facts were also stored.")
            status_caption(st.session_state.get("last_status", "offline_demo"))
        else:
            st.markdown(
                '<div class="note-card">Click <b>Save Session 3</b> to watch the first facts appear here.</div>',
                unsafe_allow_html=True,
            )


def handoff_tab():
    st.subheader("2. Handoff")

    ready = len(st.session_state.saved_sessions) == 3
    if not ready:
        st.warning("Save Sessions 3, 7, and 11 first.")

    if not st.session_state.intake_generated:
        if st.button("Run Handoff", type="primary", disabled=not ready):
            st.session_state.referral_generated = True
            st.session_state.intake_generated = True
            retrieved, status = search_memories(
                st.session_state.memories,
                "Hi, I'm here for the medication evaluation.",
                limit=10,
                use_real_mem0=st.session_state.use_real_mem0,
            )
            st.session_state.retrieved_memories = retrieved
            st.session_state.search_status = status
            st.rerun()

    if st.session_state.referral_generated:
        referral_col, missed_col = st.columns([1, 1], gap="large")
        with referral_col:
            st.markdown("**Referral letter**")
            st.markdown(
                f'<div class="letter-card">{REFERRAL_LETTER.replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div class="compare-card">
                  <b>Memory:</b> 14 facts<br>
                  <b>Letter:</b> 4 sentences<br>
                  <b>Preserved:</b> ~15%
                </div>
                """,
                unsafe_allow_html=True,
            )
        with missed_col:
            st.markdown("**Missing from handoff**")
            for missed in MISSED_DETAILS[:4]:
                render_miss_card(missed)

        st.divider()
        st.markdown("**Patient message**")
        st.markdown(
            '<div class="query-chip">Hi, I\'m here for the medication evaluation.</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.referral_generated and st.session_state.intake_generated:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown(
                """
                <div class="panel panel-left">
                  <div class="panel-title">Without Mem0 - referral letter only</div>
                  <div class="response">
                    Welcome Alex. Can you tell me about your mental health history?
                    What medications have you tried before?
                  </div>
                  <br>
                  <b>Token count:</b> 89 input tokens<br>
                  <b>Context:</b> referral letter only<br>
                  <b>Result:</b> Patient has to repeat everything.
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                """
                <div class="panel panel-right">
                  <div class="panel-title">With Mem0 - shared patient memory</div>
                  <div class="response">
                    I can see you've been working with Dr. Chen on panic disorder and GAD.
                    Sertraline caused GI issues - nausea and diarrhea specifically.
                    Grounding techniques help with mild episodes but not severe ones.
                    Your attacks are down from 3 to about 2.4 per week, but sleep has been declining,
                    especially Sunday nights. Let's talk about medication options that avoid the GI side effects.
                  </div>
                  <br>
                  <b>Token count:</b> 312 input tokens<br>
                  <b>Memories retrieved:</b> 10<br>
                  <b>Result:</b> Patient does not repeat a single thing.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.caption("mem0.search() retrieved the relevant facts before the psychiatrist response.")
        if st.session_state.get("search_status") == "live_mem0_unavailable":
            st.caption("Live Mem0 search was requested but unavailable, so the local demo ranking was used.")
        with st.expander("Retrieved memories", expanded=False):
            retrieved = st.session_state.get("retrieved_memories", [])
            for index, fact in enumerate(retrieved, start=1):
                st.markdown(f"**{index}. {fact.display}**")
                st.caption(f"{fact.category} · {fact.source}")

def main():
    init_state()
    render_header()

    with st.sidebar:
        st.markdown("### Demo controls")
        st.toggle(
            "Mirror calls to live Mem0",
            key="use_real_mem0",
            help="Requires MEM0_API_KEY and network access. The demo remains deterministic either way.",
        )
        if st.button("Reset demo", use_container_width=True):
            for key in [
                "memories",
                "saved_sessions",
                "last_new_facts",
                "referral_generated",
                "intake_generated",
                "retrieved_memories",
            ]:
                st.session_state.pop(key, None)
            st.rerun()
        st.caption("Fictional patient data for demo use only.")

    tab1, tab2 = st.tabs(["Therapy Sessions", "Handoff"])
    with tab1:
        therapy_tab()
    with tab2:
        handoff_tab()


if __name__ == "__main__":
    main()
