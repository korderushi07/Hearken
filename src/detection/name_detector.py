import re
from config import USER_NAME

NAME_VARIANTS = [
    USER_NAME,
    "Roshikesh",
    "Roshi Gyesh",
    "Rushi Kesh",
]


def detect_name(text: str) -> bool:
    for name in NAME_VARIANTS:
        pattern = rf"\b{re.escape(name)}\b"

        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False


if __name__ == "__main__":
    tests = [
        "Hello, Rushikesh.",
        "Hello, Roshikesh.",
        "Roshi Gyesh, can you hear me?",
        "Hello everyone!",
    ]

    for text in tests:
        print(f"{text} -> {detect_name(text)}")