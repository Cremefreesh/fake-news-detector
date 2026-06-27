import re
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


RAW_DATA_DIR = Path("ml/data/raw")
PROCESSED_DATA_DIR = Path("ml/data/processed")

RANDOM_STATE = 42


def clean_text(text: str) -> str:
    """
    Basic cleaning for classical ML / simple neural models.

    We keep this conservative:
    - lowercase text
    - remove URLs
    - remove extra whitespace
    """

    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_raw_data() -> pd.DataFrame:
    fake_df = pd.read_csv(RAW_DATA_DIR / "Fake.csv")
    true_df = pd.read_csv(RAW_DATA_DIR / "True.csv")

    fake_df["label"] = 1
    true_df["label"] = 0

    df = pd.concat([fake_df, true_df], ignore_index=True)

    return df


def prepare_dataset() -> None:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = load_raw_data()

    df["title"] = df["title"].astype(str)
    df["text"] = df["text"].astype(str)

    df["combined_text"] = df["title"] + " " + df["text"]
    df["clean_text"] = df["combined_text"].apply(clean_text)

    df = df[["clean_text", "label"]]

    df = df.drop_duplicates(subset=["clean_text"])
    df = df[df["clean_text"].str.len() > 20]

    train_df, temp_df = train_test_split(
        df,
        test_size=0.3,
        random_state=RANDOM_STATE,
        stratify=df["label"],
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.5,
        random_state=RANDOM_STATE,
        stratify=temp_df["label"],
    )

    train_df.to_csv(PROCESSED_DATA_DIR / "train.csv", index=False)
    val_df.to_csv(PROCESSED_DATA_DIR / "val.csv", index=False)
    test_df.to_csv(PROCESSED_DATA_DIR / "test.csv", index=False)

    print("Dataset prepared successfully.")
    print(f"Total rows after cleaning: {len(df)}")
    print(f"Train rows: {len(train_df)}")
    print(f"Validation rows: {len(val_df)}")
    print(f"Test rows: {len(test_df)}")

    print("\nTrain label distribution:")
    print(train_df["label"].value_counts(normalize=True))

    print("\nValidation label distribution:")
    print(val_df["label"].value_counts(normalize=True))

    print("\nTest label distribution:")
    print(test_df["label"].value_counts(normalize=True))


if __name__ == "__main__":
    prepare_dataset()