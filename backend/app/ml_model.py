from app.torch_inference import torch_predictor


def get_risk_level(label: str, confidence: float) -> str:
    if label == "Likely Real":
        return "Low"

    if label == "Uncertain":
        return "Medium"

    if confidence >= 0.85:
        return "High"

    if confidence >= 0.65:
        return "Medium"

    return "Low"


def predict_fake_news(text: str) -> dict:
    result = torch_predictor.predict(text)

    risk_level = get_risk_level(
        label=result["label"],
        confidence=result["confidence"],
    )

    return {
        "label": result["label"],
        "confidence": result["confidence"],
        "risk_level": risk_level,
        "model_name": result["model_name"],
        "influential_words": [],
    }