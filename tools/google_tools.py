"""
Google API tools for Gmail and Calendar.
"""

import json
import os
from google.cloud import secretmanager
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

    def _get_secret(self, secret_name: str) -> str:
        """Fetch a secret from GCP Secret Manager."""
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")


    def _get_credentials(self, token_secret_name: str) -> Credentials:
        """Load OAuth credentials — from Secret Manager in prod, local file in dev."""
        
        # Local development — read from file
        local_path = f"tokens/{token_secret_name}.json"
        if os.path.exists(local_path):
            with open(local_path) as f:
                token_data = json.load(f)
        else:
            # Production — read from Secret Manager
            token_json = self._get_secret(token_secret_name)
            token_data = json.loads(token_json)

        creds = Credentials.from_authorized_user_info(token_data, SCOPES)
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


    def fetch_work_emails(self) -> str:
        """
        Fetches recent and unread emails from the work Gmail inbox.
        Returns a formatted string of emails including sender, subject, and preview.
        Call this to get work-related emails.
        """
        return self._fetch_emails("work_token", label="work")

    def fetch_personal_emails(self) -> str:
        """
        Fetches recent and unread emails from the personal Gmail inbox.
        Returns a formatted string of emails including sender, subject, and preview.
        Call this to get personal emails.
        """
        return self._fetch_emails("personal_token", label="personal")

    def fetch_calendar_events(self) -> str:
        """
        Fetches all Google Calendar events scheduled for today.
        Returns a formatted list of events with titles, times, and locations.
        Call this to get today's schedule.
        """
        token_path = os.getenv("GMAIL_WORK_TOKEN", "tokens/work_token.json")

        try:
            creds = self._get_credentials("work_token") 
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
