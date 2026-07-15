# Línea Base de Desarrollo — Sistema de Triaje Multimodal IA

## Contexto de negocio
- Problema: saturación de urgencias y variabilidad subjetiva del triaje.
- Objetivo: apoyar la decisión clínica con un modelo multimodal offline.
- Alcance: clasificación I–V, explicabilidad SHAP, notebooks reproducibles.

## Stack y arquitectura propuesta
- Lenguaje: Python 3.10+.
- Frameworks: pandas, numpy, scikit-learn, xgboost, transformers/sentence-transformers, shap, joblib.
- Arquitectura: pipeline modular offline, con fusión temprana y tardía comparadas.

## Restricciones
- No producción ni integración EHR.
- Datos hospitalarios sujetos a autorización ética.
- Privacidad y anonimización obligatorias.

## Requisitos no funcionales
- F1 macro ≥ 0.82.
- Recall Nivel I ≥ 0.90; Nivel II ≥ 0.85.
- Reproducibilidad y trazabilidad.

## Supuestos de trabajo
- Se trabajará con datasets públicos y, si procede, con datos autorizados anonimizados.
- Se priorizará recall en niveles críticos y se documentarán limitaciones si no se alcanza el objetivo.
