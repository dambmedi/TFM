import pandas as pd

from src.preprocessor import ClinicalPreprocessor


def test_prepare_dataset_keeps_diagnostico_for_embeddings():
    df = pd.DataFrame(
        {
            "nivel": ["I", "II"],
            "edad_raw": ["25 años", "30 años"],
            "fecha_ingreso": ["2024-01-01", "2024-01-02"],
            "hora_ingreso": ["10:00", "11:00"],
            "hora_egreso": ["12:00", "12:30"],
            "institucion": ["H1", "H2"],
            "source": ["s1", "s2"],
            "diagnostico": ["dolor abdominal", "fiebre"],
            "codigo_diagnostico": ["A1", "B2"],
        }
    )

    processed = ClinicalPreprocessor().prepare_dataset(df)

    assert "diagnostico" in processed.columns
    assert processed.loc[0, "diagnostico"] == "dolor abdominal"
