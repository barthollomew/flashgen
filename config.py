import os

from utils.openai_api import DEFAULT_MODEL, get_client


class Config:
    """Configuration class to handle API keys and other settings."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please set the OPENAI_API_KEY environment variable.")
        self.client = get_client(self.api_key)
        self.model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

