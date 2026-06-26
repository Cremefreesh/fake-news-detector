def generate_explanation(text: str, label: str, confidence: float) -> str:
    """
    Temporary explanation function.
    Later this can call an LLM API.
    """

    if label == "Potentially Fake":
        return (
            f"This content was flagged with {confidence * 100:.0f}% confidence because "
            "it contains language often associated with exaggerated or misleading claims."
        )

    return (
        f"This content was classified as likely reliable with {confidence * 100:.0f}% confidence. "
        "The current dummy model did not detect obvious suspicious wording."
    )