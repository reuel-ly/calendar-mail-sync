work_agent = LlmAgent(
    name="WorkEmailAgent",
    model=MODEL,
    description="Fetches and summarizes work inbox emails.",
    instruction="""
You summarize emails from the user's work Gmail inbox.
Use the fetch_work_emails tool to get the emails.
Then write a concise bullet-point summary focusing on:
- Action items or tasks assigned to you
- Meeting requests or schedule changes
- Urgent matters from managers or clients

Keep it under 120 words. Start with: **Work inbox**
Output ONLY the summary. Nothing else.
""",
    tools=[fetch_work_emails],
    output_key="work_summary",
)