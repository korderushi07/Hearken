import re
from difflib import SequenceMatcher

from src.settings_manager import load_settings


SIMILARITY_THRESHOLD = 0.88


def detect_name(text: str) -> bool:

    settings = load_settings()

    if not settings["name_alerts_enabled"]:
        return False

    # Get the primary name and saved variations
    name_variants = [
        settings["user_name"],
        *settings["name_variations"]
    ]

    words = re.findall(r"[a-zA-Z]+", text.lower())

    normalized_variants = [
        re.sub(r"[^a-z]", "", name.lower())
        for name in name_variants
        if name.strip()
    ]

    # Exact match and fuzzy match
    for word in words:

        for variant in normalized_variants:

            if word == variant:
                return True

            if (
                len(word) >= 7
                and SequenceMatcher(None, word, variant).ratio()
                >= SIMILARITY_THRESHOLD
            ):
                return True

    # Detect split names such as "Rishi Kesh"
    for i in range(len(words) - 1):

        combined = words[i] + words[i + 1]

        if combined in normalized_variants:
            return True

        for variant in normalized_variants:

            if (
                len(combined) >= 7
                and SequenceMatcher(
                    None, combined, variant
                ).ratio() >= SIMILARITY_THRESHOLD
            ):
                return True

    return False

if __name__ == "__main__":
    test_cases = [
        "Rushikesh",
        "Roshikesh",
        "Rishi Kesh",
        "Bush",
        "Oliver"
    ]

    for text in test_cases:
        print(f"{text}: {detect_name(text)}")