import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


class ClinicalPreprocessor:
    """Preprocesa datos clínicos estructurados para el sistema de triaje."""

    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy="median")
        self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.fitted = False
        self.categorical_cols = ["institucion", "source"]
        self.numeric_cols = ["edad", "duracion_ingreso_mins"]

    def prepare_dataset(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df = self._clean_columns(df)
        df["edad"] = df["edad_raw"].astype(str).str.extract(r"(\d+)").astype(float)
        df["duracion_ingreso_mins"] = self._calculate_duration(df)
        df = df.drop(
            columns=[
                "edad_raw",
                "fecha_ingreso",
                "hora_ingreso",
                "hora_egreso",
                "fecha_egreso",
                "fecha_atencion",
                "hora_atencion",
                "codigo_administrativo",
                "nombre_administrador",
                "red",
                "codigo_diagnostico",
            ],
            errors="ignore",
        )
        df = df.dropna(subset=["nivel"])
        df["nivel"] = df["nivel"].astype(str).str.upper().map({"I": 0, "II": 1, "III": 2, "IV": 3, "V": 4})
        df = df.dropna(subset=["nivel"])
        df["institucion"] = df["institucion"].fillna("desconocida")
        df["source"] = df["source"].fillna("desconocida")
        df = self._fit_transform(df)
        return df

    def _clean_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        return df

    def _calculate_duration(self, df: pd.DataFrame) -> pd.Series:
        start = pd.to_datetime(df["fecha_ingreso"].astype(str) + " " + df["hora_ingreso"], errors="coerce")
        end = pd.to_datetime(df["fecha_ingreso"].astype(str) + " " + df.get("hora_egreso", pd.Series([None] * len(df))).astype(str), errors="coerce")
        duration = (end - start).dt.total_seconds() / 60.0
        return duration.fillna(0.0)

    def _fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        X_num = self.imputer.fit_transform(df[self.numeric_cols])
        X_num = self.scaler.fit_transform(X_num)
        X_cat = self.encoder.fit_transform(df[self.categorical_cols])
        cat_cols = self.encoder.get_feature_names_out(self.categorical_cols)
        df_num = pd.DataFrame(X_num, columns=self.numeric_cols, index=df.index)
        df_cat = pd.DataFrame(X_cat, columns=cat_cols, index=df.index)
        df_final = pd.concat([df.drop(columns=self.numeric_cols + self.categorical_cols), df_num, df_cat], axis=1)
        self.fitted = True
        return df_final

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df = self._clean_columns(df)
        df["edad"] = df["edad_raw"].astype(str).str.extract(r"(\d+)").astype(float)
        df["duracion_ingreso_mins"] = self._calculate_duration(df)
        df = df.drop(
            columns=[
                "edad_raw",
                "fecha_ingreso",
                "hora_ingreso",
                "hora_egreso",
                "fecha_egreso",
                "fecha_atencion",
                "hora_atencion",
                "codigo_administrativo",
                "nombre_administrador",
                "red",
                "codigo_diagnostico",
            ],
            errors="ignore",
        )
        df["institucion"] = df["institucion"].fillna("desconocida")
        df["source"] = df["source"].fillna("desconocida")
        X_num = self.imputer.transform(df[self.numeric_cols])
        X_num = self.scaler.transform(X_num)
        X_cat = self.encoder.transform(df[self.categorical_cols])
        cat_cols = self.encoder.get_feature_names_out(self.categorical_cols)
        df_num = pd.DataFrame(X_num, columns=self.numeric_cols, index=df.index)
        df_cat = pd.DataFrame(X_cat, columns=cat_cols, index=df.index)
        df_final = pd.concat([df.drop(columns=self.numeric_cols + self.categorical_cols), df_num, df_cat], axis=1)
        return df_final
