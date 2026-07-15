from typing import Iterable, List
import numpy as np
from sentence_transformers import SentenceTransformer


class ClinicalTextEncoder:
    """Genera embeddings de texto clínico usando sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def encode_texts(self, texts: Iterable[str]) -> np.ndarray:
        return self.model.encode(list(texts), show_progress_bar=True, normalize_embeddings=True)
