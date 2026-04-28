from google.adk.agents import LlmAgent

from tools import DiscordTools
from core.settings import settings

discord_tools = DiscordTools()

discord_agent = LlmAgent(
    name="DiscordSenderAgent",
    model=settings.discord_model,
    description="Sends the final digest to Discord.",
    instruction=settings.discord_instruction,
    tools=[discord_tools.send_to_discord],
)