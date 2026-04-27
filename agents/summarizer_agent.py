summarizer_agent = LlmAgent(
    name="DigestMergerAgent",
    model=MODEL,
    description="Combines all summaries into a single morning digest.",
    instruction="""
You are combining summaries from 4 agents into one Discord morning digest.

Here are the summaries:

{school_summary}

{work_summary}

{personal_summary}

{calendar_summary}

Write one clean, readable digest message formatted for Discord:
- Start with: "Good morning! Here's your daily digest 🌅"
- Keep each section header bold using Discord markdown (**text**)
- Use bullet points (- ) for items
- Add a short **Today's focus** line at the end: the single most urgent thing
- Total length: under 400 words
- Tone: direct and helpful, no corporate language

Output ONLY the final digest message. Nothing else.
""",
    output_key="final_digest",
)
