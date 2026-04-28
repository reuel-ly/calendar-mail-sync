from google.adk.agents import ParallelAgent

from .email_agents.school_email_reader import school_agent
from .email_agents.work_email_reader import work_agent
from .email_agents.pers_email_reader import personal_agent
from .calendar_agent import calendar_agent


parallel_fetcher = ParallelAgent(
    name="ParallelEmailCalendarFetcher",
    description="Runs all inbox and calendar agents concurrently.",
    sub_agents=[school_agent, work_agent, personal_agent, calendar_agent],
)
