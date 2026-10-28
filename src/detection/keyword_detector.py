import re
from config import WATCHED_KEYWORDS


def detect_keywords(text: str) -> list[str]:
    """Return watched keywords found in the transcript."""
    found = []

    for keyword in WATCHED_KEYWORDS:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            found.append(keyword)

    return found


if __name__ == "__main__":
    tests = [
        "The project deployment deadline is tomorrow.",
        "Hello everyone!",
    ]

    for text in tests:
        print(f"{text} -> {detect_keywords(text)}")