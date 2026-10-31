import re

from src.settings_manager import load_settings


def detect_keywords(text: str) -> list[str]:

    settings = load_settings()

    if not settings["keyword_alerts_enabled"]:
        return []

    found = []

    for keyword in settings["watched_keywords"]:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(keyword)

    return found
