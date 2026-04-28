from google.adk.agents import LlmAgent

from tools import GoogleTools
from core.settings import settings

google_tools = GoogleTools()

calendar_agent = LlmAgent(
    name="CalendarAgent",
    model=settings.calendar_model,
    description="Fetches and summarizes today's calendar events.",
    instruction=settings.calendar_instruction,
    tools=[google_tools.fetch_calendar_events],
    output_key="calendar_summary",
)