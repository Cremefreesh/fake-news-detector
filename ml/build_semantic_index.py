from pathlib import Path
import pickle

import pandas as pd
from sentence_transformers import SentenceTransformer


PROCESSED_DATA_DIR = Path("ml/data/processed")
MODEL_DIR = Path("ml/models")

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
MAX_EXAMPLES_PER_CLASS = 1000


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")

    fake_df = df[df["label"] == 1].sample(
        n=MAX_EXAMPLES_PER_CLASS,
        random_state=42,
    )

    real_df = df[df["label"] == 0].sample(
        n=MAX_EXAMPLES_PER_CLASS,
        random_state=42,
    )

    index_df = pd.concat([fake_df, real_df], ignore_index=True)

    texts = index_df["clean_text"].tolist()
    labels = index_df["label"].tolist()

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    with open(MODEL_DIR / "semantic_index.pkl", "wb") as f:
        pickle.dump(
            {
                "texts": texts,
                "labels": labels,
                "embeddings": embeddings,
                "embedding_model_name": EMBEDDING_MODEL_NAME,
            },
            f,
        )

    print("Semantic index saved.")
    print(f"Indexed examples: {len(texts)}")
    print(MODEL_DIR / "semantic_index.pkl")


if __name__ == "__main__":
    main()