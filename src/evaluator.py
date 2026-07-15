from pathlib import Path
import json
from typing import Dict


class EvaluationReport:
    def __init__(self, metrics_dir: Path):
        self.metrics_dir = metrics_dir

    def save_metrics(
        self,
        baseline_metrics: Dict[str, float],
        early_metrics: Dict[str, float],
        late_metrics: Dict[str, float],
        created_at: str,
    ) -> None:
        output = {
            "created_at": created_at,
            "baseline": baseline_metrics,
            "early_fusion": early_metrics,
            "late_fusion": late_metrics,
        }
        with open(self.metrics_dir / "results.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
