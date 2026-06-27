import pandas as pd
from pathlib import Path


RAW_DATA_DIR = Path("ml/data/raw")


def load_data():
    fake_path = RAW_DATA_DIR / "Fake.csv"
    true_path = RAW_DATA_DIR / "True.csv"

    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    fake_df["label"] = 1
    true_df["label"] = 0

    df = pd.concat([fake_df, true_df], ignore_index=True)

    return df


def main():
    df = load_data()

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nLabel counts:")
    print(df["label"].value_counts())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nExample row:")
    print(df.iloc[0])

    df["text_length"] = df["text"].astype(str).apply(len)

    print("\nText length statistics:")
    print(df["text_length"].describe())


if __name__ == "__main__":
    main()