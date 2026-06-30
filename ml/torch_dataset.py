import re
from collections import Counter

import torch
from torch.utils.data import Dataset


PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"


def tokenize(text: str) -> list[str]:
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.split()


def build_vocab(texts, max_vocab_size: int = 50000, min_freq: int = 2):
    counter = Counter()

    for text in texts:
        counter.update(tokenize(text))

    vocab = {
        PAD_TOKEN: 0,
        UNK_TOKEN: 1,
    }

    for word, freq in counter.most_common(max_vocab_size):
        if freq < min_freq:
            continue

        if word not in vocab:
            vocab[word] = len(vocab)

    return vocab


def encode_text(text: str, vocab: dict, max_length: int = 300):
    tokens = tokenize(text)

    ids = [
        vocab.get(token, vocab[UNK_TOKEN])
        for token in tokens[:max_length]
    ]

    if len(ids) < max_length:
        ids += [vocab[PAD_TOKEN]] * (max_length - len(ids))

    return ids


class FakeNewsDataset(Dataset):
    def __init__(self, dataframe, vocab, max_length: int = 300):
        self.texts = dataframe["clean_text"].tolist()
        self.labels = dataframe["label"].tolist()
        self.vocab = vocab
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        input_ids = encode_text(
            self.texts[index],
            self.vocab,
            self.max_length,
        )

        label = self.labels[index]

        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "label": torch.tensor(label, dtype=torch.long),
        }