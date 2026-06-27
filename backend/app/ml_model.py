from pathlib import Path
import joblib
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTORIZER_PATH = PROJECT_ROOT / "ml" / "models" / "tfidf_vectorizer.joblib"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "baseline_logistic_regression.joblib"

vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)


def get_risk_level(label: str, confidence: float) -> str:
    if label == "Likely Real":
        return "Low"

    if confidence >= 0.85:
        return "High"

    if confidence >= 0.65:
        return "Medium"

    return "Low"


def get_influential_words(text_vector, top_n: int = 8) -> list[str]:
    feature_names = vectorizer.get_feature_names_out()
    non_zero_indices = text_vector.nonzero()[1]

    if len(non_zero_indices) == 0:
        return []

    scores = text_vector[0, non_zero_indices].toarray()[0]
    top_indices = np.argsort(scores)[-top_n:][::-1]

    return [feature_names[non_zero_indices[i]] for i in top_indices]


def predict_fake_news(text: str) -> dict:
    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]
    probabilities = model.predict_proba(text_vector)[0]

    confidence = float(max(probabilities))
    label = "Potentially Fake" if prediction == 1 else "Likely Real"

    return {
        "label": label,
        "confidence": round(confidence, 2),
        "risk_level": get_risk_level(label, confidence),
        "model_name": "TF-IDF + Logistic Regression",
        "influential_words": get_influential_words(text_vector),
    }