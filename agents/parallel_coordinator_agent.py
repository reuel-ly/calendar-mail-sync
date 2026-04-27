parallel_fetcher = ParallelAgent(
    name="ParallelEmailCalendarFetcher",
    description="Runs all inbox and calendar agents concurrently.",
    sub_agents=[school_agent, work_agent, personal_agent, calendar_agent],
)
