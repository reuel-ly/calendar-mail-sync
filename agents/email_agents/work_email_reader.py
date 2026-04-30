from google.adk.agents import LlmAgent

from tools.google_tools import GoogleTools
from core.settings import settings

google_tools = GoogleTools()

work_agent = LlmAgent(
    name="WorkEmailAgent",
    model=settings.work_email_model or settings.default_model,
    description="Fetches and summarizes work inbox emails.",
    instruction=settings.work_email_instruction,
    tools=[google_tools.fetch_work_emails],
    output_key="work_summary",
)