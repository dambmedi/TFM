from pathlib import Path
import logging
from datetime import datetime

from src.data_ingestor import DataIngestor
from src.preprocessor import ClinicalPreprocessor
from src.embeddings import ClinicalTextEncoder
from src.trainer import ModelTrainer
from src.explainer import TriajeExplainer
from src.evaluator import EvaluationReport
from src.utils import set_seed


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "resources" / "functional" / "datasets"
    artifacts_dir = root / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    (artifacts_dir / "models").mkdir(exist_ok=True)
    (artifacts_dir / "metrics").mkdir(exist_ok=True)
    (artifacts_dir / "shap").mkdir(exist_ok=True)

    set_seed(42)

    logger.info("Iniciando pipeline de triaje multimodal")
    logger.info(f"Directorio de datos: {data_dir}")
    logger.info(f"Directorio de artefactos: {artifacts_dir}")

    ingestor = DataIngestor(data_dir)
    data = ingestor.load_combined_dataset()

    preprocessor = ClinicalPreprocessor()
    data = preprocessor.prepare_dataset(data)

    text_encoder = ClinicalTextEncoder(model_name="sentence-transformers/all-mpnet-base-v2")
    text_embeddings = text_encoder.encode_texts(data["diagnostico"].fillna(""))

    trainer = ModelTrainer(artifacts_dir / "models")
    splits = trainer.split_dataset(data)

    baseline_metrics = trainer.train_baseline(splits)
    early_metrics = trainer.train_early_fusion(splits, text_embeddings)
    late_metrics = trainer.train_late_fusion(splits, text_embeddings)

    logger.info("Generando reportes de evaluación")
    evaluator = EvaluationReport(artifacts_dir / "metrics")
    evaluator.save_metrics(
        baseline_metrics=baseline_metrics,
        early_metrics=early_metrics,
        late_metrics=late_metrics,
        created_at=datetime.now().isoformat(),
    )

    logger.info("Generando explicaciones SHAP para el mejor modelo")
    explainer = TriajeExplainer(artifacts_dir / "shap")
    explainer.explain_best_model(
        trainer=trainer,
        splits=splits,
        text_embeddings=text_embeddings,
    )

    logger.info("Pipeline completado")


if __name__ == "__main__":
    main()
