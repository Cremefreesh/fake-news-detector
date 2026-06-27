from pathlib import Path
import json
import joblib

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report


PROCESSED_DATA_DIR = Path("ml/data/processed")
MODEL_DIR = Path("ml/models")
REPORT_DIR = Path("ml/reports")


def evaluate_model(model, x, y):
    predictions = model.predict(x)

    return {
        "accuracy": accuracy_score(y, predictions),
        "precision": precision_score(y, predictions),
        "recall": recall_score(y, predictions),
        "f1": f1_score(y, predictions),
        "classification_report": classification_report(y, predictions),
    }


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")

    x_train = train_df["clean_text"]
    y_train = train_df["label"]

    x_val = val_df["clean_text"]
    y_val = val_df["label"]

    x_test = test_df["clean_text"]
    y_test = test_df["label"]

    vectorizer = TfidfVectorizer(
        max_features=50000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
    )

    x_train_vec = vectorizer.fit_transform(x_train)
    x_val_vec = vectorizer.transform(x_val)
    x_test_vec = vectorizer.transform(x_test)

    model = LogisticRegression(
        max_iter=1000,
        n_jobs=-1,
    )

    model.fit(x_train_vec, y_train)

    val_metrics = evaluate_model(model, x_val_vec, y_val)
    test_metrics = evaluate_model(model, x_test_vec, y_test)

    print("\nValidation metrics:")
    print(json.dumps({k: v for k, v in val_metrics.items() if k != "classification_report"}, indent=2))

    print("\nTest metrics:")
    print(json.dumps({k: v for k, v in test_metrics.items() if k != "classification_report"}, indent=2))

    print("\nTest classification report:")
    print(test_metrics["classification_report"])

    joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(model, MODEL_DIR / "baseline_logistic_regression.joblib")

    with open(REPORT_DIR / "baseline_metrics.json", "w") as f:
        json.dump(
            {
                "validation": {k: v for k, v in val_metrics.items() if k != "classification_report"},
                "test": {k: v for k, v in test_metrics.items() if k != "classification_report"},
                "test_classification_report": test_metrics["classification_report"],
            },
            f,
            indent=2,
        )

    print("\nSaved:")
    print(MODEL_DIR / "tfidf_vectorizer.joblib")
    print(MODEL_DIR / "baseline_logistic_regression.joblib")
    print(REPORT_DIR / "baseline_metrics.json")


if __name__ == "__main__":
    main()