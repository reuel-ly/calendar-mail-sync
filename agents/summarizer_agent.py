from google.adk.agents import LlmAgent

from core.settings import settings

summarizer_agent = LlmAgent(
    name="DigestMergerAgent",
    model=settings.summarizer_model,
    description="Combines all summaries into a single morning digest.",
    instruction=settings.summarizer_instruction,
    output_key="final_digest",
)
