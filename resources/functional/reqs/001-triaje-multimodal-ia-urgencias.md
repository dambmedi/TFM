---
id: 001
slug: triaje-multimodal-ia-urgencias
ia_cierre: 19/100
rondas: 2
estado: lista-para-diseno
fecha: 2026-07-13
---

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 EVOLUCIÓN DEL ÍNDICE DE AMBIGÜEDAD
 Ronda 0 (inicial): 48/100
 Ronda 1:           19/100  ← CIERRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**NECESIDAD DE NEGOCIO REFINADA**
Un sistema offline de apoyo a la decisión clínica que, a partir de datos estructurados y texto libre de admisión, clasifica a pacientes en urgencias en los 5 niveles de la Resolución 5596 de 2015 (I–V) y proporciona explicabilidad (SHAP) para respaldar la decisión humana durante el triaje.

**Justificación**
Los servicios de urgencias están saturados y la variabilidad subjetiva en el triaje ocasiona riesgos clínicos. Este sistema busca mejorar la detección de pacientes críticos (Niveles I–II) priorizando recall en esas clases para reducir falsos negativos críticos, manteniendo rendimiento aceptable en las demás clases.

**Actores**
| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Equipo TFM | Ejecutor | Preparar datos, entrenar modelos, documentar resultados y entregar notebooks/artefactos. |
| Directora (Damaris Fuentes Lorenzo) | Aprobador / Beneficiario académico | Validar criterios de aceptación y revisar entregables para la defensa del TFM. |
| Comité de Ética (Hospital San Juan de Dios) | Bloqueador / Validador | Autorizar uso de datos locales y validar procedimientos de anonimización. |
| Equipo de TI del hospital (si aplica) | Consultor | Proveer aclaraciones sobre formatos de datos si se necesita. |

**Alcance**
- ✅ IN SCOPE: Desarrollo offline del modelo multimodal (estructurado + texto), preprocesamiento, experimentos comparativos (early vs late fusion), evaluación por clase, generación de notebooks reproducibles, y módulo de explicabilidad con SHAP.
- ❌ OUT OF SCOPE: Integración en HCE/EHR en tiempo real, interfaz web o móvil, tratamiento de imágenes médicas, certificación regulatoria (INVIMA), despliegue en producción.

**Criterios de Aceptación**
- Metas agregadas (piso general): F1 ≥ 0,82; Precisión ≥ 0,85; Recall ≥ 0,80; AUC-ROC ≥ 0,87.
- Metas por clase (obligatorias):
  - Nivel I: Recall ≥ 0.90
  - Nivel II: Recall ≥ 0.85
  - Nivel III: Recall ≥ 0.80
  - Nivel IV: Recall ≥ 0.75
  - Nivel V: Recall ≥ 0.75

Ejemplos en formato Gherkin:
```
DADO un conjunto de validación etiquetado con niveles I–V
CUANDO se evalúa el modelo final
ENTONCES el Recall para Nivel I será ≥ 0.90
```
```
DADO un conjunto de validación etiquetado
CUANDO se calcula F1 macro
ENTONCES F1_macro será ≥ 0.82
```

**Restricciones y Supuestos**
- Restricciones:
  - Datos locales (Hospital San Juan de Dios) están sujetos a autorización ética; el equipo usará únicamente datos anonimizados y autorizados.
  - MIMIC-IV-ED requiere credenciales CITI y será usado solo cuando proceda; adaptaciones a contexto colombiano requieren fine-tuning con datos locales.
- Supuestos validados: el equipo TFM proveerá los archivos CSV/Parquet para el experimento y podrá obtener las descargas públicas (MinSalud, BDUA, Supersalud).
- Supuestos no validados: umbrales operativos definitivos para alertas I–II (se propone priorizar recall; la directora debe confirmar valores de tolerancia a falsas alarmas en contexto hospitalario).

**Métricas de Éxito**
| Métrica | Línea Base | Meta | Plazo |
|---------|-----------:|------:|------:|
| F1 (macro) | — | ≥ 0.82 | Entrega TFM (defensa) |
| Precisión (macro) | — | ≥ 0.85 | Entrega TFM |
| Recall (macro) | — | ≥ 0.80 | Entrega TFM |
| AUC-ROC (macro) | — | ≥ 0.87 | Entrega TFM |
| Recall Nivel I | — | ≥ 0.90 | Entrega TFM |
| Recall Nivel II | — | ≥ 0.85 | Entrega TFM |

**Prioridad (MoSCoW)**
- Must Have: Modelos entrenados offline, evaluación por clase, notebooks reproducibles, documentación de preprocesamiento y explicabilidad SHAP.
- Should Have: Comparativa early vs late fusion y análisis de técnicas para clases desbalanceadas (class weights, SMOTE, focal loss).
- Could Have: Script de generación de reportes automatizados (tabla con métricas por clase) y Jupyter Notebook con visualizaciones interactivas.
- Won't Have: Interfaz web, integración EHR, procesamiento de imágenes, certificación regulatoria.

**Dependencias**
- MIMIC‑IV‑ED (PhysioNet) — acceso CITI por los autores que lo posean.
- Datasets públicos de Min. Salud, BDUA, Supersalud — descargas por el equipo.
- Validación ética del Hospital San Juan de Dios — pendiente (En trámite).

**Brechas pendientes**
| Campo | Información faltante | Impacto |
|-------|---------------------|--------:|
| Validación ética | Estado final de la autorización del Comité de Ética | Bloqueante para entrenar/fine-tune con datos hospitalarios reales; si no se resuelve, se trabajará solo con datos públicos/MIMIC y se documentará limitación. |
| Sample anonimizado | CSV de muestra para pruebas de preprocesado | Necesario para tests replicables en contexto local — se solicita entrega por el equipo. |

**Entregables (MVP TFM)**
- Repositorio con notebooks reproducibles: preprocesamiento, experimentos baseline, multimodal (early/late), evaluación y SHAP.
- Artefactos de modelos (pesos/serialización) y scripts para evaluación por clase.
- Documento técnico (Cap.4) con metodología, resultados y discusión (Cap.5).

**Notas operativas**
- Alcance confirmado: entregable offline únicamente; el equipo TFM entregará los CSV/Parquet.
- Estrategia de optimización: priorizar recall en Niveles I–II, balanceado en III–V, con metas por clase definidas arriba.

✅ Lista para diseño/estimación

---
*Documento generado siguiendo el protocolo de clarificación del skill `epicureo`. Para continuar: ejecutar el plan técnico mínimo (stack, artefactos y cronograma) si se desea que proponga estimación de esfuerzo.*
