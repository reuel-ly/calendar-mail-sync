import asyncio
import traceback
import warnings

from dotenv import load_dotenv
load_dotenv()

from core.settings import settings
from .validate_settings import validate_settings

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.email_agents import school_agent, work_agent, personal_agent
from agents.calendar_agent import calendar_agent
from agents.discord_agent import discord_agent
from tools.discord_tools import DiscordTools

APP_NAME = "digest_test"
USER_ID = "test_user"


async def run_agent(agent, prompt: str, label: str) -> str:
    """Run a single ADK agent through the proper Runner and return its output."""
    print(f"\n--- Running {label} ---")
    try:
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
        )

        runner = Runner(
            agent=agent,
            app_name=APP_NAME,
            session_service=session_service,
        )

        message = types.Content(
            role="user",
            parts=[types.Part(text=prompt)],
        )

        result_text = ""
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=message,
        ):
            if event.content and event.content.parts:
                text = event.content.parts[0].text if event.content.parts[0].text else ""
                if text:
                    result_text = text  # keep the last meaningful output

        print(result_text)
        return result_text

    except Exception as e:
        print(f"\n[ERROR] {label} failed:")
        traceback.print_exc()
        raise e
async def test_discord(digest_text: str):
    print("\n--- Running Discord Agent ---")
    discord = DiscordTools()
    result = await discord.send_to_discord(digest_text)
    print(f"Discord result: {result}")
    return result
async def main():
    # Step 1: Validate settings
    print("Validating settings...")
    errors, warning_list = validate_settings()

    if errors:
        raise ValueError(f"Settings validation failed:\n{errors}")
    elif warning_list:
        warnings.warn(f"Warnings:\n{warning_list}")

    print("Settings validation passed. Starting agent execution...\n")

    # Step 2: Run agents individually (sequential for easier debugging)
    school_summary = await run_agent(
        school_agent, "Summarize my school inbox.", "School Email Agent"
    )

    work_summary = await run_agent(
        work_agent, "Summarize my work inbox.", "Work Email Agent"
    )

    personal_summary = await run_agent(
        personal_agent, "Summarize my personal inbox.", "Personal Email Agent"
    )

    calendar_summary = await run_agent(
        calendar_agent, "Summarize my calendar events for today.", "Calendar Agent"
    )

    # Step 3: Send to Discord
    final_digest_prompt = f"""
Here are the summaries:

This just a test.
"""

    await test_discord(final_digest_prompt)

    print("\nAll agents completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())