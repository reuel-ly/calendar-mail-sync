root_agent = SequentialAgent(
    name="MorningDigestPipeline",
    description="Full morning digest pipeline: fetch emails in parallel, merge, send to Discord.",
    sub_agents=[parallel_fetcher, merger_agent, discord_agent],
)