from pathlib import Path
import pickle
import re

import torch
import torch.nn.functional as F

# Import the same model architecture used during training
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "ml"))

from torch_model import FakeNewsLSTM  # noqa: E402


MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "pytorch_lstm_fake_news.pt"
VOCAB_PATH = PROJECT_ROOT / "ml" / "models" / "pytorch_vocab.pkl"

MAX_LENGTH = 300
PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"


def get_device():
    return torch.device("cpu")


def tokenize(text: str) -> list[str]:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.split()


def encode_text(text: str, vocab: dict) -> list[int]:
    tokens = tokenize(text)

    ids = [
        vocab.get(token, vocab[UNK_TOKEN])
        for token in tokens[:MAX_LENGTH]
    ]

    if len(ids) < MAX_LENGTH:
        ids += [vocab[PAD_TOKEN]] * (MAX_LENGTH - len(ids))

    return ids


class TorchFakeNewsPredictor:
    def __init__(self):
        self.device = get_device()

        with open(VOCAB_PATH, "rb") as f:
            self.vocab = pickle.load(f)

        self.model = FakeNewsLSTM(vocab_size=len(self.vocab))
        self.model.load_state_dict(
            torch.load(MODEL_PATH, map_location=self.device)
        )
        self.model.to(self.device)
        self.model.eval()

    def predict(self, text: str) -> dict:
        input_ids = encode_text(text, self.vocab)

        input_tensor = torch.tensor(
            [input_ids],
            dtype=torch.long,
            device=self.device,
        )

        with torch.no_grad():
            logits = self.model(input_tensor)
            probabilities = F.softmax(logits, dim=1)[0]

        predicted_class = int(torch.argmax(probabilities).item())
        confidence = float(probabilities[predicted_class].item())

        fake_probability = float(probabilities[1].item())
        real_probability = float(probabilities[0].item())

        if fake_probability >= 0.75:
            label = "Potentially Fake"
            confidence = fake_probability
        elif real_probability >= 0.75:
            label = "Likely Real"
            confidence = real_probability
        else:
            label = "Uncertain"
            confidence = max(fake_probability, real_probability)

        return {
            "label": label,
            "confidence": round(confidence, 2),
            "model_name": "PyTorch Bidirectional LSTM",
        }


torch_predictor = TorchFakeNewsPredictor()