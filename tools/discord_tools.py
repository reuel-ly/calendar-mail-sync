"""
Discord tools for webhook messaging.
"""

import os
import httpx


class DiscordTools:
    """Handles Discord webhook interactions."""

    def send_to_discord(self, message: str) -> str:
        """
        Sends the final morning digest message to Discord via webhook.
        Call this after the digest is fully composed and ready to send.
        message: The complete formatted digest text to post to Discord.
        Returns 'success' or an error message.
        """
        webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        if not webhook_url:
            return "Error: DISCORD_WEBHOOK_URL not set in .env"

        try:
            # Discord 2000 char limit — split into chunks if needed
            chunks = [message[i:i + 1900] for i in range(0, len(message), 1900)]
            with httpx.Client() as client:
                for chunk in chunks:
                    response = client.post(webhook_url, json={"content": chunk})
                    response.raise_for_status()
            return "success"
        except Exception as e:
            return f"Error sending to Discord: {str(e)}"
