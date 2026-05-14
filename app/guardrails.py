OFF_TOPIC_KEYWORDS = [
    "movie",
    "movies",
    "netflix",
    "football",
    "cricket",
    "bitcoin",
    "crypto",
    "politics",
    "election",
    "religion",
    "legal advice",
    "medical advice",
    "stock market",
    "dating",
    "music",
    "song"
]


def is_off_topic(text):

    if not text:
        return False

    text = text.lower()

    for keyword in OFF_TOPIC_KEYWORDS:

        if keyword in text:
            return True

    return False