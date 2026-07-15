from pathlib import Path
from typing import Dict, Any
import numpy as np
import shap
import joblib
from sklearn.base import BaseEstimator


class TriajeExplainer:
    def __init__(self, shap_dir: Path):
        self.shap_dir = shap_dir
        self.shap_dir.mkdir(parents=True, exist_ok=True)

    def explain_best_model(self, trainer, splits, text_embeddings: np.ndarray) -> None:
        model = joblib.load(trainer.model_dir / "early_fusion_xgb.joblib")
        explainer = shap.TreeExplainer(model)
        X_test = self._build_early_features(splits, text_embeddings)
        shap_values = explainer.shap_values(X_test)
        self._save_explanations(shap_values)

    def _build_early_features(self, splits, text_embeddings: np.ndarray) -> np.ndarray:
        test_idx = splits["X_test"].index
        return np.hstack([splits["X_test"].values, text_embeddings[test_idx]])

    def _save_explanations(self, shap_values: Any) -> None:
        np.save(self.shap_dir / "shap_values.npy", shap_values)
