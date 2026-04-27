discord_agent = LlmAgent(
    name="DiscordSenderAgent",
    model=MODEL,
    description="Sends the final digest to Discord.",
    instruction="""
Your only job is to send the following message to Discord using the send_to_discord tool.

Message to send:
{final_digest}

Call send_to_discord with the exact message above.
After sending, confirm with: "Digest sent to Discord successfully."
""",
    tools=[send_to_discord],
)