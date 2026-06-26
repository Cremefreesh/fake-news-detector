import random


def predict_fake_news(text: str) -> dict:
    """
    Temporary dummy model.
    Later we will replace this with a real PyTorch model.
    """

    suspicious_words = [
        "shocking",
        "secret",
        "exposed",
        "miracle",
        "urgent",
        "they don't want you to know",
        "breaking",
    ]

    text_lower = text.lower()

    score = 0

    for word in suspicious_words:
        if word in text_lower:
            score += 1

    if score > 0:
        label = "Potentially Fake"
        confidence = min(0.65 + score * 0.08, 0.95)
    else:
        label = "Likely Real"
        confidence = random.uniform(0.55, 0.75)

    return {
        "label": label,
        "confidence": round(confidence, 2),
    }