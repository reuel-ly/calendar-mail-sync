import asyncio
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
else:
    raise ValueError("No API key found. Set GOOGLE_API_KEY or GEMINI_API_KEY in .env")


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents import root_coordinator_agent

APP_NAME = "morning_digest"
USER_ID = "local_user"


async def run_digest():
    print("Starting morning digest pipeline...")

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    runner = Runner(
        agent=root_coordinator_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    trigger = types.Content(
        role="user",
        parts=[types.Part(text="Generate and send my morning digest now.")],
    )

    # Retry up to 5 times with increasing wait between attempts
    max_retries = 5
    for attempt in range(max_retries):
        try:
            async for event in runner.run_async(
                user_id=USER_ID,
                session_id=session.id,
                new_message=trigger,
            ):
                if event.content and event.content.parts:
                    author = event.author or "unknown"
                    text = event.content.parts[0].text if event.content.parts[0].text else ""
                    if text:
                        print(f"\n[{author}]:\n{text}")

            print("\nPipeline complete.")
            return  # success — exit

        except Exception as e:
            wait = 30 * (attempt + 1)  # 30s, 60s, 90s, 120s, 150s
            print(f"\nAttempt {attempt + 1} failed:")
            traceback.print_exc()
            if attempt < max_retries - 1:
                print(f"Retrying in {wait} seconds...")
                await asyncio.sleep(wait)
            else:
                print("All retries exhausted.")
                raise


if __name__ == "__main__":
    asyncio.run(run_digest())