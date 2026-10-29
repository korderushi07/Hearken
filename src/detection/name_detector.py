import re
from config import USER_NAME

NAME_VARIANTS = [
    USER_NAME,
    "Roshikesh",
    "Rishikesh",
    "Rushikesh",
    "Rushi Kesh",
    "Roshi Gyesh",
    "Rushi",
    "Hrushikesh",
    "Hrushi",
    "Rishi",
    "रुशिकेश",
    "ऋषिकेश",
    "रुशीकेश",
    "रुशी",
]

def detect_name(text: str) -> bool:
    normalized_text = re.sub(r"\s+", " ", text.lower()).strip()

    for name in NAME_VARIANTS:
        normalized_name = name.lower().strip()
        pattern = rf"(?<!\w){re.escape(normalized_name)}(?!\w)"

        if re.search(pattern, normalized_text):
            return True

    return False

if __name__ == "__main__":
    tests = [
        "Hello, Rushikesh.",
        "Hi, Rishikesh!",
        "रुशिकेश",
        "ऋषिकेश",
        "Hello everyone!",
    ]

    for text in tests:
        print(f"{text} -> {detect_name(text)}")