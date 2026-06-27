def generate_explanation(
    label: str,
    confidence: float,
    risk_level: str,
    influential_words: list[str],
) -> str:
    confidence_percent = round(confidence * 100)

    words = ", ".join(influential_words[:5])

    if label == "Potentially Fake":
        return (
            f"This content was classified as potentially fake with "
            f"{confidence_percent}% confidence. Risk level: {risk_level}. "
            f"The model paid attention to terms such as: {words}."
        )

    return (
        f"This content was classified as likely real with "
        f"{confidence_percent}% confidence. Risk level: {risk_level}. "
        f"The model paid attention to terms such as: {words}."
    )