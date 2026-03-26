---
name: document-specialist
description: Agente especialista en el sistema de documentos de TramitUp: generación de cartas/documentos con IA, análisis de PDFs subidos, extracción de información, pipeline de documentos y gestión de adjuntos. Úsalo para cambios en documentos, PDFs o el flujo de generación.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el sistema de documentos de TramitUp.

## Arquitectura del sistema de documentos

### Dos subsistemas
```
1. GENERACIÓN DE DOCUMENTOS (cartas, reclamaciones, recursos)
   POST /api/v1/document/generate → genera carta con IA

2. ANÁLISIS DE DOCUMENTOS (PDFs del usuario)
   POST /api/v1/document/analyze → analiza PDF subido por el usuario
   POST /api/v1/attachments/upload → sube adjunto para el chat
   GET  /api/v1/documents → lista documentos del usuario
```

## Archivos críticos

### Backend
- `backend/app/services/document_service.py` — generación de documentos
- `backend/app/services/document_pipeline_service.py` — pipeline completo de análisis
- `backend/app/services/document_analysis_service.py` — análisis de contenido
- `backend/app/ai/chains/document_chain.py` — chain LLM para documentos
- `backend/app/ai/chains/document_generate_chain.py` — generación de texto
- `backend/app/ai/chains/document_extract_chain.py` — extracción de datos
- `backend/app/ai/prompts/document.py` — prompts base para documentos
- `backend/app/ai/prompts/document_templates.py` — plantillas de documentos legales
- `backend/app/ai/prompts/document_extract.py` — prompts de extracción
- `backend/app/ai/prompts/document_generate.py` — prompts de generación
- `backend/app/api/v1/endpoints/document.py` — endpoints de documentos
- `backend/app/api/v1/endpoints/attachments.py` — upload de adjuntos
- `backend/app/api/v1/endpoints/document_search.py` — búsqueda en documentos
- `backend/app/api/v1/endpoints/contract_analysis.py` — análisis de contratos

### Frontend
- `frontend/app/documents/page.tsx` — lista y gestión de documentos
- `frontend/app/chat/page.tsx` — upload de adjuntos antes de enviar mensaje
- `frontend/app/contrato/page.tsx` — análisis de contratos

## Generación de documentos

### Tipos de documentos generables
Los prompts en `document_templates.py` definen plantillas para:
- Carta de reclamación a aerolínea (EU 261/2004)
- Carta de despido improcedente
- Recurso de multa de tráfico
- Reclamación de fianza de alquiler
- Carta de reclamación de factura energética
- Recurso ante Hacienda

### Flujo de generación
```python
# document_service.py
async def generate_document(
    user_id: str,
    document_type: str,
    form_data: dict,
    conversation_id: str | None
) -> dict:
    # 1. Obtener plantilla de document_templates.py
    # 2. Construir prompt con form_data
    # 3. Llamar a document_generate_chain.py → LLM
    # 4. Guardar en tabla documents
    # 5. Devolver {id, title, content, created_at}
```

## Análisis de adjuntos (attachments)

### Flujo de upload para chat
```python
# attachments.py endpoint
POST /api/v1/attachments/upload
  multipart/form-data: file (PDF, imagen, texto)
  → document_analysis_service.extract_text(file)
  → guardar en tabla attachments
  → devolver attachment_id

# El chat usa attachment_ids para incluir el contenido en el prompt
```

### Análisis de contratos
```python
# contract_analysis_service.py
POST /api/v1/contract-analysis
  file: PDF del contrato
  → extract text from PDF
  → contract_analysis prompts → LLM
  → devuelve: {
      summary, clauses_analysis, red_flags,
      recommendations, risk_level
    }
```

## Esquema tablas de documentos (Supabase)
```sql
documents (
  id              UUID PRIMARY KEY,
  user_id         UUID REFERENCES profiles(id),
  title           TEXT,
  document_type   TEXT,           -- "carta_reclamacion", "recurso_multa", etc.
  content         TEXT,           -- contenido generado por IA
  form_data       JSONB,          -- datos del formulario usados para generar
  conversation_id UUID NULLABLE,
  created_at      TIMESTAMPTZ
)

attachments (
  id              UUID PRIMARY KEY,
  user_id         UUID REFERENCES profiles(id),
  filename        TEXT,
  content_type    TEXT,           -- "application/pdf", "image/jpeg", etc.
  extracted_text  TEXT,           -- texto extraído para usar en chat
  file_url        TEXT,           -- URL en Supabase Storage
  created_at      TIMESTAMPTZ
)
```

## Document extraction chain
```python
# document_extract_chain.py
# Extrae datos estructurados de un documento:
# - Fechas, plazos, importes
# - Partes involucradas
# - Obligaciones y derechos
# - Cláusulas relevantes
```

## Reglas críticas
- Los documentos generados son solo para plan `document` y `pro` — verificar plan
- Máximo tamaño de adjunto: verificar en `attachments.py` (ej. 10MB)
- Los PDFs se procesan con extracción de texto — si falla, usar OCR alternativo
- `extracted_text` de attachments se incluye en el prompt del chat como contexto
- Guardar `form_data` junto con el documento para permitir re-generación
- Los documentos pertenecen al usuario — siempre filtrar por `user_id`
