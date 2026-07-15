# Plan técnico mínimo — Triaje Multimodal IA (MVP offline)

## Resumen corto
Plan mínimo para entregar un MVP offline: modelos entrenados y evaluados (estructurado + texto), notebooks reproducibles, artefactos de modelo y documentación técnica.

## Stack recomendado
- Lenguaje: Python 3.10+ (3.11 recomendado)
- Entorno: `venv` o `poetry` (recomiendo `poetry` para gestión de dependencias)
- Principales librerías:
  - Data: `pandas`, `numpy`, `scikit-learn`, `imbalanced-learn`
  - Boosted trees: `xgboost`
  - NLP / embeddings: `transformers`, `sentence-transformers` (modelo clínico en español si disponible)
  - Deep learning (si aplica): `tensorflow` o `torch` (preferencia por `torch` si se usan BERTs)
  - Explicabilidad: `shap`
  - Utilidades: `joblib`, `pyyaml`, `tqdm`
  - Notebooks: `jupyterlab`, `nbformat`
- Infra/ejecución: GPU opcional para entrenamiento de BERT (NVIDIA with CUDA); CPU suficiente para XGBoost
- Repositorio: Git (GitHub/GitLab), `.gitignore`, `requirements.txt` o `pyproject.toml`
- Contenerización (opcional): `Dockerfile` para reproducibilidad

## Artefactos entregables
- `notebooks/`:
  - `01-data-ingest-and-eda.ipynb`
  - `02-preprocessing.ipynb`
  - `03-baseline-models.ipynb`
  - `04-multimodal-training.ipynb`
  - `05-evaluation-and-shap.ipynb`
- `src/`:
  - `preprocess.py`, `train.py`, `evaluate.py`, `embeddings.py`
- `artifacts/`:
  - Modelos serializados (`model_xgb.joblib`, `bert_model/`)
  - `metrics/` CSV con métricas por clase
  - `reports/` PDF o Markdown con tablas y figuras
- `data/`:
  - `README` con esquema de datasets y scripts de ingest
- Documentación: `README.md`, `Cap4.md` (borrador de Capítulo 4), `deployment-notes.md` (opcional)

## Requisitos de cómputo
- Desarrollo local: CPU multicore (>=4), 16 GB RAM
- Entrenamiento BERT: GPU con >=8GB VRAM (p. ej. RTX 3060) o Colab Pro
- Almacenamiento: dependencia del dataset; estimado mínimo 10–50 GB

## Cronograma estimado (6 semanas) — equipo TFM (3 integrantes)
Semana 1 — Datos y EDA (3--5 días)
- Descargar/organizar CSV/Parquet
- EDA por dataset y esquema de features
Entrega: `notebooks/01-data-ingest-and-eda.ipynb`

Semana 2 — Preprocesamiento y pipeline (5 días)
- Limpieza, imputación, normalización, tokenización de texto
- Definir pipeline reproducible y splits
Entrega: `notebooks/02-preprocessing.ipynb`, `src/preprocess.py`

Semana 3 — Modelos baseline (5 días)
- Entrenar Regresión Logística, RF, XGBoost (estructurado)
- Métricas por clase, handling class imbalance
Entrega: `notebooks/03-baseline-models.ipynb`, artefactos iniciales

Semana 4 — Multimodal (5–7 días)
- Embeddings de texto con `sentence-transformers` o BERT
- Implementar fusión temprana y tardía, entrenar modelos
Entrega: `notebooks/04-multimodal-training.ipynb`, `src/embeddings.py`

Semana 5 — Evaluación y XAI (5 días)
- Calcular métricas por clase (Recall objetivos), AUPRC/AUROC
- SHAP explanations y ejemplos clínicos traducidos
Entrega: `notebooks/05-evaluation-and-shap.ipynb`, reportes en `reports/`

Semana 6 — Consolidación y documentación (3–5 días)
- Pulir notebooks, escribir Cap.4 borrador, empaquetar artefactos reproducibles
Entrega: `Cap4.md`, `README.md`, `artifacts/` final

Total estimado: 6 semanas calendario (18 persona-semanas si 3 integrantes trabajaran ~full-time coordinado). Ajustar si hay limitaciones de tiempo/horas disponibles.

## Hitos y criterios de aceptación
- Hito 1 (fin Semana 2): Pipelines de ingest y preprocesamiento reproducibles
- Hito 2 (fin Semana 3): Modelos baseline con métricas iniciales
- Hito 3 (fin Semana 4): Multimodal entrenado y comparado (early vs late)
- Hito 4 (fin Semana 5): Cumplimiento de criterios por clase o documentación de por qué no se alcanzan
- Hito 5 (fin Semana 6): Entregables finales y borrador Cap.4/5

## Riesgos y mitigaciones
- Acceso a datos hospitalarios (bloqueante): Mitigación — trabajar con MIMIC + datasets públicos y documentar limitación.
- Clases altamente desbalanceadas: Mitigación — usar class weights, resampling (SMOTE), y métricas por clase; priorizar recall en I–II.
- Recursos GPU limitados: Mitigación — usar embeddings precomputados o servicios cloud (Colab/OCI/GCP/Azure)

## Siguientes pasos inmediatos
1. Confirmar acceso y ubicación de los CSV/Parquet en el equipo.
2. Crear repositorio/estructura de carpetas y archivo `pyproject.toml` o `requirements.txt`.
3. Asignar tareas semanales entre los integrantes.

---
Fecha: 2026-07-13
Autor: Equipo TFM
