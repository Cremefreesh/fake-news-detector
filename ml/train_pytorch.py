from pathlib import Path
import json
import pickle

import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from torch_dataset import FakeNewsDataset, build_vocab
from torch_model import FakeNewsLSTM


PROCESSED_DATA_DIR = Path("ml/data/processed")
MODEL_DIR = Path("ml/models")
REPORT_DIR = Path("ml/reports")

BATCH_SIZE = 64
EPOCHS = 4
LEARNING_RATE = 0.001
MAX_LENGTH = 300


def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")  # Apple Silicon GPU
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def train_one_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0

    for batch in dataloader:
        input_ids = batch["input_ids"].to(device)
        labels = batch["label"].to(device)

        optimizer.zero_grad()

        logits = model(input_ids)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)


def evaluate(model, dataloader, criterion, device):
    model.eval()
    total_loss = 0
    all_predictions = []
    all_labels = []

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            labels = batch["label"].to(device)

            logits = model(input_ids)
            loss = criterion(logits, labels)

            predictions = torch.argmax(logits, dim=1)

            total_loss += loss.item()
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    return {
        "loss": total_loss / len(dataloader),
        "accuracy": accuracy_score(all_labels, all_predictions),
        "precision": precision_score(all_labels, all_predictions),
        "recall": recall_score(all_labels, all_predictions),
        "f1": f1_score(all_labels, all_predictions),
    }


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    device = get_device()
    print(f"Using device: {device}")

    train_df = pd.read_csv(PROCESSED_DATA_DIR / "train.csv")
    val_df = pd.read_csv(PROCESSED_DATA_DIR / "val.csv")
    test_df = pd.read_csv(PROCESSED_DATA_DIR / "test.csv")

    vocab = build_vocab(train_df["clean_text"], max_vocab_size=50000, min_freq=2)

    print(f"Vocabulary size: {len(vocab)}")

    train_dataset = FakeNewsDataset(train_df, vocab, max_length=MAX_LENGTH)
    val_dataset = FakeNewsDataset(val_df, vocab, max_length=MAX_LENGTH)
    test_dataset = FakeNewsDataset(test_df, vocab, max_length=MAX_LENGTH)

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )

    model = FakeNewsLSTM(vocab_size=len(vocab)).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    history = []

    for epoch in range(EPOCHS):
        train_loss = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
        )

        val_metrics = evaluate(
            model,
            val_loader,
            criterion,
            device,
        )

        epoch_result = {
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "val_loss": val_metrics["loss"],
            "val_accuracy": val_metrics["accuracy"],
            "val_precision": val_metrics["precision"],
            "val_recall": val_metrics["recall"],
            "val_f1": val_metrics["f1"],
        }

        history.append(epoch_result)

        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        print(f"Train loss: {train_loss:.4f}")
        print(f"Val loss: {val_metrics['loss']:.4f}")
        print(f"Val accuracy: {val_metrics['accuracy']:.4f}")
        print(f"Val precision: {val_metrics['precision']:.4f}")
        print(f"Val recall: {val_metrics['recall']:.4f}")
        print(f"Val F1: {val_metrics['f1']:.4f}")

    test_metrics = evaluate(
        model,
        test_loader,
        criterion,
        device,
    )

    print("\nFinal test metrics:")
    print(json.dumps(test_metrics, indent=2))

    torch.save(
        model.state_dict(),
        MODEL_DIR / "pytorch_lstm_fake_news.pt",
    )

    with open(MODEL_DIR / "pytorch_vocab.pkl", "wb") as f:
        pickle.dump(vocab, f)

    with open(REPORT_DIR / "pytorch_lstm_metrics.json", "w") as f:
        json.dump(
            {
                "history": history,
                "test_metrics": test_metrics,
                "config": {
                    "batch_size": BATCH_SIZE,
                    "epochs": EPOCHS,
                    "learning_rate": LEARNING_RATE,
                    "max_length": MAX_LENGTH,
                    "vocab_size": len(vocab),
                    "model": "Bidirectional LSTM",
                },
            },
            f,
            indent=2,
        )

    print("\nSaved:")
    print(MODEL_DIR / "pytorch_lstm_fake_news.pt")
    print(MODEL_DIR / "pytorch_vocab.pkl")
    print(REPORT_DIR / "pytorch_lstm_metrics.json")


if __name__ == "__main__":
    main()