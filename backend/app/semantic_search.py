from pathlib import Path
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INDEX_PATH = BASE_DIR / "ml" / "models" / "semantic_index.pkl"


class SemanticSearchService:
    def __init__(self):
        with open(INDEX_PATH, "rb") as f:
            index = pickle.load(f)

        self.texts = index["texts"]
        self.labels = index["labels"]
        self.embeddings = index["embeddings"]
        self.embedding_model_name = index["embedding_model_name"]

        self.model = SentenceTransformer(self.embedding_model_name)

    def find_similar(self, text: str, top_k: int = 3):
        query_embedding = self.model.encode(
            [text],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]

        similarities = np.dot(self.embeddings, query_embedding)

        top_indices = similarities.argsort()[-top_k:][::-1]

        matches = []

        for index in top_indices:
            matches.append(
                {
                    "label": "Potentially Fake" if self.labels[index] == 1 else "Likely Real",
                    "similarity": round(float(similarities[index]), 3),
                    "preview": self.texts[index][:250] + "...",
                }
            )

        return matches


semantic_search_service = SemanticSearchService()