from google.adk.agents import LlmAgent

from tools.google_tools import GoogleTools
from core.settings import settings

google_tools = GoogleTools()

personal_agent = LlmAgent(
    name="PersonalEmailAgent",
    model=settings.personal_email_model,
    description="Fetches and summarizes personal inbox emails.",
    instruction=settings.personal_email_instruction,
    tools=[google_tools.fetch_personal_emails],
    output_key="personal_summary",
)
