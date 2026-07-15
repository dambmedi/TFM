from pathlib import Path
from typing import Dict
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.utils.class_weight import compute_class_weight

from src.models import EarlyFusionModel, LateFusionModel
from xgboost import XGBClassifier


class ModelTrainer:
    def __init__(self, model_dir: Path):
        self.model_dir = model_dir

    def split_dataset(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        X = df.drop(columns=["nivel", "diagnostico", "codigo_diagnostico"])
        y = df["nivel"].astype(int)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

    def train_baseline(self, splits: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        class_weights = compute_class_weight("balanced", classes=np.unique(splits["y_train"]), y=splits["y_train"])
        model = XGBClassifier(
            eval_metric="mlogloss",
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.9,
            colsample_bytree=0.9,
            scale_pos_weight=1.0,
        )
        model.fit(splits["X_train"], splits["y_train"], sample_weight=self._class_weight_vector(splits["y_train"], class_weights))
        preds = model.predict(splits["X_test"])
        probs = model.predict_proba(splits["X_test"])
        self._save_model(model, "baseline_xgb")
        return self._score(splits["y_test"], preds, probs)

    def train_early_fusion(self, splits: Dict[str, pd.DataFrame], text_embeddings: np.ndarray) -> Dict[str, float]:
        train_idx = splits["X_train"].index
        test_idx = splits["X_test"].index
        X_train = np.hstack([splits["X_train"].values, text_embeddings[train_idx]])
        X_test = np.hstack([splits["X_test"].values, text_embeddings[test_idx]])
        model = EarlyFusionModel(params={"max_depth": 5, "n_estimators": 200, "eval_metric": "mlogloss"})
        model.fit(X_train, splits["y_train"].values)
        preds = model.predict(X_test)
        probs = model.predict_proba(X_test)
        self._save_model(model.model, "early_fusion_xgb")
        return self._score(splits["y_test"], preds, probs)

    def train_late_fusion(self, splits: Dict[str, pd.DataFrame], text_embeddings: np.ndarray) -> Dict[str, float]:
        train_idx = splits["X_train"].index
        test_idx = splits["X_test"].index
        X_struct_train = splits["X_train"].values
        X_struct_test = splits["X_test"].values
        X_text_train = text_embeddings[train_idx]
        X_text_test = text_embeddings[test_idx]
        model = LateFusionModel()
        model.fit(X_struct_train, X_text_train, splits["y_train"].values)
        preds = model.predict(X_struct_test, X_text_test)
        probs = model.predict_proba(X_struct_test, X_text_test)
        self._save_model(model.meta_model, "late_fusion_meta")
        return self._score(splits["y_test"], preds, probs)

    def _save_model(self, model, name: str) -> None:
        import joblib

        joblib.dump(model, self.model_dir / f"{name}.joblib")

    def _class_weight_vector(self, y, class_weights: np.ndarray) -> np.ndarray:
        classes = np.unique(y)
        return np.array([class_weights[np.where(classes == c)[0][0]] for c in y])

    def _score(self, y_true, preds, probs) -> Dict[str, float]:
        return {
            "precision_macro": precision_score(y_true, preds, average="macro", zero_division=0),
            "recall_macro": recall_score(y_true, preds, average="macro", zero_division=0),
            "f1_macro": f1_score(y_true, preds, average="macro", zero_division=0),
        }
