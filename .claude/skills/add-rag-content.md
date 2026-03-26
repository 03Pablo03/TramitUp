Añade contenido legal al knowledge base RAG de TramitUp.

**Pasos:**

1. Lee `backend/app/ai/rag/retriever.py` para entender el sistema de embeddings
2. Prepara el contenido a indexar:
   - Dividir en chunks de 200-500 tokens (autocontenidos)
   - Cada chunk debe tener sentido por sí solo
   - Incluir referencias legales explícitas (artículo, ley, fecha)
3. Para cada chunk, definir metadata:
   ```python
   metadata = {
       "category": "laboral|vivienda|consumo|familia|trafico|administrativo|fiscal|penal",
       "source": "Estatuto de los Trabajadores / LAU / Código Civil / ...",
       "law_reference": "Art. 56 ET / Art. 36 LAU / ...",
       "document_type": "ley|jurisprudencia|guia|reglamento",
       "last_updated": "2024-01-01"
   }
   ```
4. Genera embeddings e inserta en Supabase:
   ```python
   from app.ai.rag.retriever import get_embedding
   from app.core.supabase_client import get_supabase_client

   embedding = get_embedding(chunk_content)
   supabase.table("embeddings").insert({
       "content": chunk_content,
       "metadata": metadata,
       "embedding": embedding
   }).execute()
   ```
5. Verifica la indexación con una query de prueba:
   ```python
   from app.ai.rag.retriever import retrieve_context
   results = retrieve_context("consulta de prueba sobre el tema indexado")
   ```
6. Confirma que los chunks aparecen en los primeros resultados con similarity > 0.6

**Contenido a añadir:** $ARGUMENTS
