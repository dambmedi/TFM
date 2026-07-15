from typing import Optional
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator
from xgboost import XGBClassifier


class EarlyFusionModel:
    def __init__(
        self,
        params: Optional[dict] = None,
    ):
        self.params = params or {"max_depth": 6, "n_estimators": 100, "use_label_encoder": False, "eval_metric": "mlogloss"}
        self.model = XGBClassifier(**self.params)

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)


class LateFusionModel:
    def __init__(self, meta_model: Optional[BaseEstimator] = None):
        self.structured_model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
        self.text_model = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
        self.meta_model = meta_model or LogisticRegression(max_iter=1000)

    def fit(self, X_struct: np.ndarray, X_text: np.ndarray, y: np.ndarray) -> None:
        self.structured_model.fit(X_struct, y)
        self.text_model.fit(X_text, y)
        structured_probs = self.structured_model.predict_proba(X_struct)
        text_probs = self.text_model.predict_proba(X_text)
        meta_features = np.hstack([structured_probs, text_probs])
        self.meta_model.fit(meta_features, y)

    def predict(self, X_struct: np.ndarray, X_text: np.ndarray) -> np.ndarray:
        probs = self.predict_proba(X_struct, X_text)
        return np.argmax(probs, axis=1) + 1

    def predict_proba(self, X_struct: np.ndarray, X_text: np.ndarray) -> np.ndarray:
        structured_probs = self.structured_model.predict_proba(X_struct)
        text_probs = self.text_model.predict_proba(X_text)
        meta_features = np.hstack([structured_probs, text_probs])
        return self.meta_model.predict_proba(meta_features)
