# Triaje Multimodal IA

Sistema de apoyo a la decisión clínica para triaje en urgencias médicas. Este proyecto implementa un pipeline de aprendizaje automático multimodal que integra datos estructurados y texto libre para clasificar pacientes en los 5 niveles de la Resolución 5596 de 2015.

## Estructura del proyecto

- `src/`: código fuente del pipeline.
- `resources/functional/datasets/`: datasets de entrada disponibles.
- `pyproject.toml` / `requirements.txt`: dependencias del proyecto.
- `README.md`: instrucciones de uso.

## Uso

1. Instalar dependencias:
   - Con Poetry: `poetry install`
   - Con pip: `pip install -r requirements.txt`

2. Ejecutar el pipeline de entrenamiento:
   `python -m src.main`

3. Resultados y artefactos:
   - Modelos guardados en `artifacts/models/`
   - Métricas en `artifacts/metrics/`
   - Explicaciones SHAP en `artifacts/shap/`

## Requisitos mínimos

- Python 3.11
- Espacio para dataset y artefactos
- GPU opcional para embeddings de transformers

## Datos

Los datasets están en `resources/functional/datasets/` y se usan para construir los modelos de triaje. El script carga la fuente local disponible y crea un pipeline reproducible.
