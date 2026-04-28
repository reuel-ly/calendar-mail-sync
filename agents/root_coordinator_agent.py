from google.adk.agents import SequentialAgent

from .parallel_coordinator_agent import parallel_fetcher
from .summarizer_agent import summarizer_agent
from .discord_agent import discord_agent

root_coordinator_agent = SequentialAgent(
    name="MorningDigestPipeline",
    description="Full morning digest pipeline: fetch emails in parallel, merge, send to Discord.",
    sub_agents=[parallel_fetcher, summarizer_agent, discord_agent],
)