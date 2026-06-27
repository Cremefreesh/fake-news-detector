from pathlib import Path
import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTORIZER_PATH = PROJECT_ROOT / "ml" / "models" / "tfidf_vectorizer.joblib"
MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "baseline_logistic_regression.joblib"


vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)


def predict_fake_news(text: str) -> dict:
    text_vector = vectorizer.transform([text])

    prediction = model.predict(text_vector)[0]
    probabilities = model.predict_proba(text_vector)[0]

    confidence = float(max(probabilities))

    if prediction == 1:
        label = "Potentially Fake"
    else:
        label = "Likely Real"

    return {
        "label": label,
        "confidence": round(confidence, 2),
    }