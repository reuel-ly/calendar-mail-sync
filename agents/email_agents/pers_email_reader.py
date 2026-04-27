personal_agent = LlmAgent(
    name="PersonalEmailAgent",
    model=MODEL,
    description="Fetches and summarizes personal inbox emails.",
    instruction="""
You summarize emails from the user's personal Gmail inbox.
Use the fetch_personal_emails tool to get the emails.
Then write a concise bullet-point summary focusing on:
- Personal messages that need a reply
- Bills, deliveries, or reminders
- Anything time-sensitive

Keep it under 120 words. Start with: **Personal inbox**
Output ONLY the summary. Nothing else.
""",
    tools=[fetch_personal_emails],
    output_key="personal_summary",
)
