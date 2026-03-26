---
name: rag-specialist
description: Agente especialista en el sistema RAG de TramitUp: embeddings con Google Gemini, Supabase pgvector, recuperación de contexto personalizada, carga de contenido legal y retriever. Úsalo para cambios en el RAG, embeddings o contenido legal del knowledge base.
tools: Read, Write, Edit, Glob, Grep
---

Eres el especialista en el sistema RAG (Retrieval-Augmented Generation) de TramitUp.

## Arquitectura del sistema RAG

### Flujo de retrieval
```
[Chat: retrieve_context_personalized()]
  1. Convertir query → embedding (Google text-embedding-004, 768 dims)
  2. Llamar Supabase RPC "match_embeddings" con cosine similarity
  3. Filtrar por threshold (0.5) y top_k (5-10)
  4. Si user tiene interest_categories → priorizar chunks de esas categorías
  5. Devolver list[{"content": str, "metadata": dict, "similarity": float}]

[Indexación de contenido]
  Scripts o admin endpoints → llamar get_embedding(text) → insertar en embeddings table
```

## Archivos críticos

### Backend
- `backend/app/ai/rag/retriever.py` — `retrieve_context()`, `get_embedding()`
- `backend/app/services/chat_service.py` — `retrieve_context_personalized()` (wrapper con personalización)
- `backend/app/ai/llm_client.py` — cliente LLM (Google Gemini)

## Modelos de IA

```python
# Embeddings (retriever.py)
EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIM = 768

# LLM (llm_client.py)
# Google Gemini via LangChain (gemini-1.5-pro o gemini-1.5-flash)
```

## Esquema tabla embeddings (Supabase)
```sql
embeddings (
  id          BIGINT PRIMARY KEY,
  content     TEXT,           -- texto del chunk
  metadata    JSONB,          -- {category, source, law_reference, ...}
  embedding   VECTOR(768),    -- vector generado con text-embedding-004
  created_at  TIMESTAMPTZ
)

-- Índice para búsqueda vectorial eficiente:
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
```

## Función RPC (Supabase)
```sql
-- Función match_embeddings en Supabase:
CREATE OR REPLACE FUNCTION match_embeddings(
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id BIGINT,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.content,
    e.metadata,
    1 - (e.embedding <=> query_embedding) AS similarity
  FROM embeddings e
  WHERE 1 - (e.embedding <=> query_embedding) > match_threshold
  ORDER BY e.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

## retrieve_context_personalized() (chat_service.py)

```python
def retrieve_context_personalized(
    query: str,
    user_context: dict,  # {interest_categories: [...], plan: str}
    top_k: int = 8,
    threshold: float = 0.5
) -> list[dict]:
    # 1. Llamar retrieve_context(query, top_k * 2, threshold) para tener margen
    # 2. Si user tiene interest_categories:
    #    - Chunks cuya metadata.category está en interest_categories → prioridad alta
    #    - Ordenar: primero los de interés, luego el resto
    # 3. Truncar a top_k
    # 4. Devolver los chunks ordenados
```

## Carga de contenido legal (indexación)

Para añadir nuevo contenido al knowledge base:
```python
from app.ai.rag.retriever import get_embedding
from app.core.supabase_client import get_supabase_client

def index_document(content: str, metadata: dict):
    """
    metadata debe incluir:
    {
        "category": "laboral",          # categoría legal
        "source": "Estatuto Trabajadores",
        "law_reference": "Art. 56 ET",  # opcional
        "document_type": "ley",         # "ley" | "jurisprudencia" | "guia"
    }
    """
    embedding = get_embedding(content)
    supabase = get_supabase_client()
    supabase.table("embeddings").insert({
        "content": content,
        "metadata": metadata,
        "embedding": embedding
    }).execute()
```

## Dominios legales cubiertos
```
laboral:        despidos, contratos, finiquitos, ERTE, derechos laborales
vivienda:       alquileres, LAU, fianzas, desahucios, IBI
consumo:        reclamaciones aerolíneas, telecos, bancos, garantías
familia:        divorcios, herencias, custodia, testamentos
trafico:        multas DGT, accidentes, retirada carnet
administrativo: sanciones, recursos, permisos, silencio administrativo
fiscal:         IRPF, IVA, declaraciones, Hacienda
penal:          denuncias, delitos, proceso penal
```

## Manejo de errores (retriever.py)
```python
# Si embedding falla → log warning → devolver [] (chat continúa sin RAG)
# Si RPC falla → log warning → devolver [] (chat continúa sin RAG)
# Nunca lanzar excepción desde retrieve_context() — siempre devolver []
```

## Reglas críticas
- Máximo 8000 chars por chunk al llamar `get_embedding()` — verificado en retriever
- El threshold por defecto es 0.5 — bajar si hay pocos resultados, subir si hay ruido
- `metadata.category` es clave para la personalización — siempre incluirlo
- Los chunks deben ser autocontenidos (entre 200-500 tokens) para mejor recuperación
- La función `match_embeddings` usa cosine similarity (`<=>` operator)
- Habilitar pgvector en Supabase: `CREATE EXTENSION IF NOT EXISTS vector;`
- El modelo `text-embedding-004` requiere `output_dimensionality=768`
