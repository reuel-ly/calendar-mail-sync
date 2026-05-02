## Overview

This is a Morning Digest pipeline that fetches and summarizes emails from work and personal Gmail accounts, retrieves today's calendar events, combines them into a digest, and sends it to Discord.

# **File Structure**

```bash
.
├── .venv/
├── agents/
│   ├── calendar_agent.py
│   ├── discord_agent.py
│   ├── summarizer_agent.py
│   ├── root_coordinator_agent.py
│   ├── parallel_coordinator_agent.py
│   └── email_agents/
│       ├── __init__.py
│       ├── pers_email_reader.py
│       └── work_email_reader.py
├── core/
│   └── settings.py
├── tools/
│   ├── discord_tools.py
│   └── google_tools.py
├── credentials/
│   ├── credentials.json
│   ├── personal_token.json
│   ├── work_token.json
│   └── school_token.json
├── test/
│   ├── __init__.py
│   ├── exec_test.py
│   ├── test.py
│   └── validate_settings.py
├── .env
├── .gitignore
├── .python-version
├── LICENSE
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

### How It Works

1. **Email Agents**: Fetch recent/unread emails from work and personal Gmail accounts
2. **Calendar Agent**: Retrieves today's Google Calendar events
3. **Parallel Coordinator**: Runs email and calendar agents concurrently
4. **Summarizer Agent**: Combines all summaries into a single digest message
5. **Discord Agent**: Sends the final digest to Discord via webhook

### Components

- **agents/**: Contains all AI agents built with Google's Agent Development Kit (ADK)
- **core/**: Settings configuration using Pydantic
- **tools/**: Google API (Gmail/Calendar) and Discord webhook utilities
- **credentials/**: Stores OAuth token files and credentials
- **test/**: Unit tests and validation scripts
- **main.py**: Entry point that runs the pipeline

### Configuration

Environment variables are stored in `.env`:
- Discord webhook URL
- Google OAuth token file paths
- Vertex AI configuration

### Note on School Email Agent

The school_email_reader agent was removed for privacy and policy concerns (see commits 77aa326 and 2d50170 in git history). The school_token.json file remains in credentials/ for legacy purposes but is no longer used by any active agent.