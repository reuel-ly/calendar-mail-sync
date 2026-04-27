"""
Google API tools for Gmail and Calendar.
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


class GoogleTools:
    """Handles Google API interactions for Gmail and Calendar."""

    def __init__(self):
        self.scopes = SCOPES

    def _get_credentials(self, token_path: str) -> Credentials:
        """Handles OAuth for a specific Gmail account token file."""
        creds = None
        credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, self.scopes)
                creds = flow.run_local_server(port=0)

            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, "w") as f:
                f.write(creds.to_json())

        return creds

    def _fetch_emails(self, token_path: str, label: str) -> str:
        """Shared logic for fetching emails from any Gmail account."""
        try:
            creds = self._get_credentials(token_path)
            service = build("gmail", "v1", credentials=creds)

            result = service.users().messages().list(
                userId="me",
                maxResults=15,
                labelIds=["INBOX"],
                q="is:unread OR newer_than:1d",
            ).execute()

            messages = result.get("messages", [])

            if not messages:
                return f"No new emails in {label} inbox."

            emails = []
            for msg in messages:
                msg_data = service.users().messages().get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["Subject", "From", "Date"],
                ).execute()

                headers = {h["name"]: h["value"] for h in msg_data["payload"]["headers"]}
                snippet = msg_data.get("snippet", "")

                emails.append(
                    f"From: {headers.get('From', 'Unknown')}\n"
                    f"Subject: {headers.get('Subject', '(No subject)')}\n"
                    f"Preview: {snippet[:250]}"
                )

            return f"{len(emails)} emails found:\n\n" + "\n\n---\n\n".join(emails)

        except Exception as e:
            return f"Error fetching {label} emails: {str(e)}"

    def fetch_school_emails(self) -> str:
        """
        Fetches recent and unread emails from the school Gmail inbox.
        Returns a formatted string of emails including sender, subject, and preview.
        Call this to get school-related emails.
        """
        token_path = os.getenv("GMAIL_SCHOOL_TOKEN", "tokens/school_token.json")
        return self._fetch_emails(token_path, label="school")

    def fetch_work_emails(self) -> str:
        """
        Fetches recent and unread emails from the work Gmail inbox.
        Returns a formatted string of emails including sender, subject, and preview.
        Call this to get work-related emails.
        """
        token_path = os.getenv("GMAIL_WORK_TOKEN", "tokens/work_token.json")
        return self._fetch_emails(token_path, label="work")

    def fetch_personal_emails(self) -> str:
        """
        Fetches recent and unread emails from the personal Gmail inbox.
        Returns a formatted string of emails including sender, subject, and preview.
        Call this to get personal emails.
        """
        token_path = os.getenv("GMAIL_PERSONAL_TOKEN", "tokens/personal_token.json")
        return self._fetch_emails(token_path, label="personal")

    def fetch_calendar_events(self) -> str:
        """
        Fetches all Google Calendar events scheduled for today.
        Returns a formatted list of events with titles, times, and locations.
        Call this to get today's schedule.
        """
        token_path = os.getenv("GMAIL_SCHOOL_TOKEN", "tokens/school_token.json")

        try:
            creds = self._get_credentials(token_path)
            service = build("calendar", "v3", credentials=creds)

            now = datetime.now(timezone.utc)
            start_of_day = now.replace(hour=0, minute=0, second=0).isoformat()
            end_of_day = now.replace(hour=23, minute=59, second=59).isoformat()

            events_result = service.events().list(
                calendarId="primary",
                timeMin=start_of_day,
                timeMax=end_of_day,
                singleEvents=True,
                orderBy="startTime",
            ).execute()

            events = events_result.get("items", [])

            if not events:
                return "No events scheduled for today."

            lines = []
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date", ""))
                title = event.get("summary", "(No title)")
                location = event.get("location", "")
                loc_str = f" @ {location}" if location else ""
                lines.append(f"- {start}: {title}{loc_str}")

            return f"{len(events)} events today:\n" + "\n".join(lines)

        except Exception as e:
            return f"Error fetching calendar: {str(e)}"
