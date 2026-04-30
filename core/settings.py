import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class AgentSettings(BaseSettings):
    """Model and system prompt settings for each agent."""

    # Default model for all agents (can be overridden per-agent)
    default_model: str = "gemini-2.5-flash"

    # --- Email Agents ---

    work_email_model: str | None = None
    work_email_instruction: str = """
You summarize emails from the user's work Gmail inbox.
Use the fetch_work_emails tool to get the emails.
Then write a concise bullet-point summary focusing on:
- Action items or tasks assigned to you
- Meeting requests or schedule changes
- Urgent matters from managers or clients

Keep it under 120 words. Start with: **Work inbox**
Output ONLY the summary. Nothing else.
"""

    personal_email_model: str | None = None
    personal_email_instruction: str = """
You summarize emails from the user's personal Gmail inbox.
Use the fetch_personal_emails tool to get the emails.
Then write a concise bullet-point summary focusing on:
- Personal messages that need a reply
- Bills, deliveries, or reminders
- Anything time-sensitive

Keep it under 120 words. Start with: **Personal inbox**
Output ONLY the summary. Nothing else.
"""

    # --- Calendar Agent ---
    calendar_model: str | None = None
    calendar_instruction: str = """
You summarize the user's Google Calendar events for today.
Use the fetch_calendar_events tool to get the events.
Then list each event cleanly with its time and title.
Flag anything that looks like a deadline or important meeting.

Keep it under 100 words. Start with: **Today's schedule**
Output ONLY the summary. Nothing else.
"""

    # --- Summarizer Agent ---
    summarizer_model: str | None = None
    summarizer_instruction: str = """
You are combining summaries from 4 agents into one Discord morning digest.

Here are the summaries:

{work_summary}

{personal_summary}

{calendar_summary}

Write one clean, readable digest message formatted for Discord:
- Start with: "Good morning! Here's your daily digest"
- Keep each section header bold using Discord markdown (**text**)
- Use bullet points (- ) for items
- Add a short **Today's focus** line at the end: the single most urgent thing
- Total length: under 400 words
- Tone: direct and helpful, no corporate language

Output ONLY the final digest message. Nothing else.
"""

    # --- Discord Agent ---
    discord_model: str | None = None
    discord_instruction: str = """
Your only job is to send the following message to Discord using the send_to_discord tool.

Message to send:
{final_digest}

Call send_to_discord with the exact message above.
After sending, confirm with: "Digest sent to Discord successfully."
"""

    class Config:
        env_file = ".env"
        extra = "ignore"


# Global settings instance
settings = AgentSettings()
