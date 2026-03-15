#!/usr/bin/env python3
"""
Seed RAG embeddings from JSON files (Google AI / Gemini).
Run from backend/ with: python -m scripts.seed_rag

Si tenías embeddings de OpenAI, vacía la tabla antes de re-seed:
  DELETE FROM embeddings;

Requisitos: .env con SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY y GOOGLE_API_KEY
"""
import json
import pathlib
import sys

backend_dir = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Asegurar que pydantic encuentre .env (desde backend/)
import os
if not (backend_dir / ".env").exists():
    print("Error: No existe backend/.env. Copia .env.example y rellena SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY y GOOGLE_API_KEY.")
    sys.exit(1)
os.chdir(backend_dir)

from app.core.config import get_settings
from app.core.supabase_client import get_supabase_client
from app.ai.rag.retriever import get_embedding


def load_seed_files():
    base = pathlib.Path(__file__).parent.parent / "app" / "ai" / "rag" / "seed_data"
    items = []
    for f in base.glob("*.json"):
        with open(f, encoding="utf-8") as fp:
            data = json.load(fp)
            items.extend(data)
    return items


def main():
    settings = get_settings()
    if not settings.supabase_url or not settings.supabase_service_role_key:
        print("Error: Faltan credenciales de Supabase en .env")
        print("  - SUPABASE_URL=https://tu-proyecto.supabase.co")
        print("  - SUPABASE_SERVICE_ROLE_KEY=eyJ...")
        print("  Obtén los valores en: Supabase Dashboard > Project Settings > API")
        sys.exit(1)
    if not settings.google_api_key:
        print("Error: Falta GOOGLE_API_KEY en .env (para embeddings)")
        sys.exit(1)

    items = load_seed_files()
    supabase = get_supabase_client()
    print(f"Processing {len(items)} chunks...")

    for i, item in enumerate(items):
        content = item["content"]
        metadata = item.get("metadata", {})
        embedding = get_embedding(content)
        supabase.table("embeddings").insert(
            {"content": content, "metadata": metadata, "embedding": embedding}
        ).execute()
        print(f"  [{i+1}/{len(items)}] Ingested: {content[:60]}...")
    print("Done.")


if __name__ == "__main__":
    main()
