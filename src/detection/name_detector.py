import re
from difflib import SequenceMatcher
from config import USER_NAME

NAME_VARIANTS = [
    USER_NAME,
    "Roshikesh",
    "Rishikesh",
    "Hushikesh",
    "Bushikesh",
    "Hrushikesh",
]

SIMILARITY_THRESHOLD = 0.88


def normalize(text: str) -> str:
    return re.sub(r"[^a-z]", "", text.lower())


def detect_name(text: str) -> bool:
    normalized_text = text.lower().strip()

    # Exact matching (single-word variants)
    for name in NAME_VARIANTS:
        pattern = rf"(?<!\w){re.escape(name.lower())}(?!\w)"

        if re.search(pattern, normalized_text):
            return True

    # Match split names like "Rishi Kesh" or "Rishi-Kesh"
    words = re.findall(r"[a-z]+", normalized_text)
    target_names = [normalize(name) for name in NAME_VARIANTS]

    for i in range(len(words) - 1):
        combined = words[i] + words[i + 1]

        if combined in target_names:
            return True

        for target in target_names:
            if SequenceMatcher(None, combined, target).ratio() >= SIMILARITY_THRESHOLD:
                return True

    # Fuzzy matching for single-word transcription mistakes
    for word in words:
        if len(word) < 7:
            continue

        for target in target_names:
            if SequenceMatcher(None, word, target).ratio() >= SIMILARITY_THRESHOLD:
                return True

    return False


if __name__ == "__main__":
    tests = [
        "Rushikesh, can you hear me?",
        "Roshikesh, can you hear me?",
        "Rishikesh, are you there?",
        "Hushikesh, can you hear me?",
        "Bushikesh, can you hear me?",
        "Hello everyone!",
        "I'm Oliver.",
        "Bush is here.",
        "Please finish the project.",
        "Can you hear me?",
        "Oliver is joining the meeting.",
        "Rishi is here.",
        "Hello, Rishi Kesh.",
        "Rushi Kesh, can you hear me?",
        "Rishi-Kesh, are you there?",
    ]

    for sentence in tests:
        print(f"{sentence} -> {detect_name(sentence)}")
