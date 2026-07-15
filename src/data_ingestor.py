from pathlib import Path
import pandas as pd


class DataIngestor:
    """Carga y unifica los datasets clínicos disponibles para el sistema de triaje."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _read_csv(self, filename: str, **kwargs) -> pd.DataFrame:
        path = self.base_dir / filename
        try:
            return pd.read_csv(path, encoding="utf-8", **kwargs)
        except UnicodeDecodeError:
            return pd.read_csv(path, encoding="latin-1", **kwargs)

    def load_sanjuan_de_dios_dataset(self) -> pd.DataFrame:
        df = self._read_csv("dataset_urgencias_san_juan_de_dios_custom.csv")
        df = df.rename(
            columns={
                "triage": "nivel",
                "codigo de diagnostico": "codigo_diagnostico",
                "diagnostico": "diagnostico",
                "eps o ips": "institucion",
                "fecha": "fecha_ingreso",
                "hora de entrada": "hora_ingreso",
                "hora de salida": "hora_egreso",
                "edad": "edad_raw",
            }
        )
        df["source"] = "san_juan_de_dios"
        return df

    def load_public_triage_dataset(self) -> pd.DataFrame:
        df = self._read_csv("Clasificación_en_Triage_Urgencias_20260713.csv")
        df = df.rename(
            columns={
                "Triage": "nivel",
                "Ips": "institucion",
                "Fecha_Ing": "fecha_ingreso",
                "Hora_Ingre": "hora_ingreso",
                "Fecha_Atencion": "fecha_atencion",
                "Hora_Atencion": "hora_atencion",
                "CodAdminis": "codigo_administrativo",
                "Nom_Admini": "nombre_administrador",
                "Red": "red",
            }
        )
        df["diagnostico"] = df.get("diagnostico", "")
        df["codigo_diagnostico"] = ""
        df["edad_raw"] = ""
        df["fecha_egreso"] = pd.NA
        df["hora_egreso"] = pd.NA
        df["source"] = "public_triage"
        return df

    def load_combined_dataset(self) -> pd.DataFrame:
        san_juan = self.load_sanjuan_de_dios_dataset()
        public = self.load_public_triage_dataset()
        return pd.concat([san_juan, public], ignore_index=True, axis=0)
