from google.adk.agents import LlmAgent

from tools.google_tools import GoogleTools
from core.settings import settings

google_tools = GoogleTools()

school_agent = LlmAgent(
    name="SchoolEmailAgent",
    model=settings.school_email_model or settings.default_model,
    description="Fetches and summarizes school inbox emails.",
    instruction=settings.school_email_instruction,
    tools=[google_tools.fetch_school_emails],
    output_key="school_summary",
)