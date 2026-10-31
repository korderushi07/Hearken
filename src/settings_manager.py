import json
from pathlib import Path


SETTINGS_FILE = Path(__file__).resolve().parent.parent / "settings.json"

DEFAULT_SETTINGS = {
    "user_name": "Rushikesh",
    "name_variations": [
        "Roshikesh",
        "Rishikesh",
        "Hushikesh",
        "Bushikesh",
        "Hrushikesh"
    ],
    "watched_keywords": [
        "deployment",
        "deadline",
        "project",
        "nehal"
    ],
    "name_alerts_enabled": True,
    "keyword_alerts_enabled": True
}


def load_settings():
    """Load settings from JSON or create defaults."""

    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            saved_settings = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(saved_settings)

        return settings

    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Save settings locally as JSON."""

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)
