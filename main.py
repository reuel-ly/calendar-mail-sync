"""
Entry point. Uses ADK's Runner to execute the pipeline.

ADK requires:
- A session service (InMemorySessionService for local use)
- A Runner that ties the agent + session together
- A user message to kick off the pipeline (even if it's just a trigger string)
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import root_agent

APP_NAME = "morning_digest"
USER_ID = "local_user"


async def run_digest():
    print("Starting morning digest pipeline...")

    # ADK session service — InMemorySessionService is fine for a local daily runner
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # ADK Runner — connects the agent to the session
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Trigger message — the pipeline doesn't need input, this just kicks it off
    trigger = types.Content(
        role="user",
        parts=[types.Part(text="Generate and send my morning digest now.")],
    )

    # Stream events from the pipeline
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=trigger,
    ):
        # Print intermediate agent outputs as they stream in
        if event.content and event.content.parts:
            author = event.author or "unknown"
            text = event.content.parts[0].text if event.content.parts[0].text else ""
            if text:
                print(f"\n[{author}]:\n{text}")

    print("\nPipeline complete.")


if __name__ == "__main__":
    asyncio.run(run_digest())