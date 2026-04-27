calendar_agent = LlmAgent(
    name="CalendarAgent",
    model=MODEL,
    description="Fetches and summarizes today's calendar events.",
    instruction="""
You summarize the user's Google Calendar events for today.
Use the fetch_calendar_events tool to get the events.
Then list each event cleanly with its time and title.
Flag anything that looks like a deadline or important meeting.

Keep it under 100 words. Start with: **Today's schedule**
Output ONLY the summary. Nothing else.
""",
    tools=[fetch_calendar_events],
    output_key="calendar_summary",
)