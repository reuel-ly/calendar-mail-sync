import os
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent

from tools.gmail_calendar_tools import (
    fetch_school_emails,
    fetch_work_emails,
    fetch_personal_emails,
    fetch_calendar_events,
    send_to_discord,
)

MODEL = "gemini-2.0-flash"

# -------------------------------------------------------------------
# Step 1: Sub-agents that run IN PARALLEL
# Each uses output_key to save their result into shared session state.
# The merger agent reads from state using {key} syntax in its instruction.
# -------------------------------------------------------------------

school_agent = LlmAgent(
    name="SchoolEmailAgent",
    model=MODEL,
    description="Fetches and summarizes school inbox emails.",
    instruction="""
You summarize emails from the user's school Gmail inbox.
Use the fetch_school_emails tool to get the emails.
Then write a concise bullet-point summary focusing on:
- Anything urgent or requiring action
- Deadlines or upcoming dates
- Important announcements

Keep it under 120 words. Start with: **School inbox**
Output ONLY the summary. Nothing else.
""",
    tools=[fetch_school_emails],
    output_key="school_summary",  # saves result to session state
)