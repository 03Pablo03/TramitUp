from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import get_settings

EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIM = 768  # dimensión de text-embedding-004


def _get_embeddings_client() -> GoogleGenerativeAIEmbeddings:
    """Cliente de embeddings con Google AI Studio (Gemini)."""
    settings = get_settings()
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=settings.google_api_key,
        output_dimensionality=EMBEDDING_DIM,
    )


def get_embedding(text: str) -> list[float]:
    """Obtiene el vector de embedding para texto usando Google AI (Gemini)."""
    client = _get_embeddings_client()
    return client.embed_query(text[:8000])  # límite de longitud


def retrieve_context(query: str, top_k: int = 5, threshold: float = 0.5) -> list[dict]:
    """
    Retrieve relevant context from RAG.
    Returns list of {"content": str, "metadata": dict, "similarity": float}.
    Falls back to [] if embeddings or RPC are unavailable.
    """
    import logging
    logger = logging.getLogger(__name__)

    try:
        embedding = get_embedding(query)
    except Exception as e:
        logger.warning("RAG embedding failed, continuing without context: %s", e)
        return []

    try:
        from app.core.supabase_client import get_supabase_client
        supabase = get_supabase_client()
        result = supabase.rpc(
            "match_embeddings",
            {
                "query_embedding": embedding,
                "match_threshold": threshold,
                "match_count": top_k,
            },
        ).execute()

        if not result.data:
            return []
        return [{"content": r["content"], "metadata": r.get("metadata", {}), "similarity": r.get("similarity", 0)} for r in result.data]
    except Exception as e:
        logger.warning("RAG retrieval failed, continuing without context: %s", e)
        return []
