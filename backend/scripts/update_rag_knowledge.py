#!/usr/bin/env python3
"""
Script para actualizar la base de conocimiento RAG con normativa ampliada.
Carga todos los archivos JSON de seed_data y los procesa en la base de datos.
"""

import json
import os
import sys
from pathlib import Path

# Añadir el directorio raíz del backend al path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.ai.rag.retriever import get_embedding
from app.core.supabase_client import get_supabase_client


def load_knowledge_files():
    """Carga todos los archivos JSON de conocimiento."""
    seed_data_dir = backend_dir / "app" / "ai" / "rag" / "seed_data"
    knowledge_data = []
    
    # Archivos a procesar
    files_to_process = [
        "reclamaciones.json",
        "laboral.json", 
        "vivienda.json",
        "consumo_ampliado.json",
        "fiscal_tributario.json",
        "extranjeria_migracion.json"
    ]
    
    for filename in files_to_process:
        file_path = seed_data_dir / filename
        if file_path.exists():
            print(f"Cargando {filename}...")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    knowledge_data.extend(data)
                    print(f"  OK Cargados {len(data)} elementos de {filename}")
            except Exception as e:
                print(f"  ERROR cargando {filename}: {e}")
        else:
            print(f"  AVISO Archivo no encontrado: {filename}")
    
    return knowledge_data


def clear_existing_embeddings():
    """Limpia embeddings existentes para evitar duplicados."""
    print("Limpiando embeddings existentes...")
    try:
        supabase = get_supabase_client()
        result = supabase.table("embeddings").delete().neq("id", "").execute()
        print(f"  OK Eliminados embeddings existentes")
    except Exception as e:
        print(f"  AVISO Error limpiando embeddings: {e}")


def process_and_store_embeddings(knowledge_data):
    """Procesa el conocimiento y almacena los embeddings."""
    supabase = get_supabase_client()
    
    print(f"Procesando {len(knowledge_data)} elementos de conocimiento...")
    
    successful = 0
    failed = 0
    
    for i, item in enumerate(knowledge_data, 1):
        try:
            content = item.get("content", "")
            metadata = item.get("metadata", {})
            
            if not content:
                print(f"  AVISO Elemento {i}: contenido vacio, saltando...")
                continue
            
            # Generar embedding
            print(f"  Procesando {i}/{len(knowledge_data)}: {content[:50]}...")
            embedding = get_embedding(content)
            
            # Almacenar en base de datos
            supabase.table("embeddings").insert({
                "content": content,
                "metadata": metadata,
                "embedding": embedding
            }).execute()
            
            successful += 1
            
            # Progreso cada 5 elementos
            if i % 5 == 0:
                print(f"  OK Procesados {i}/{len(knowledge_data)} elementos")
                
        except Exception as e:
            print(f"  ERROR procesando elemento {i}: {e}")
            failed += 1
            continue
    
    print(f"\nOK Procesamiento completado:")
    print(f"  - Exitosos: {successful}")
    print(f"  - Fallidos: {failed}")
    print(f"  - Total: {len(knowledge_data)}")


def verify_embeddings():
    """Verifica que los embeddings se almacenaron correctamente."""
    print("\nVerificando embeddings almacenados...")
    try:
        supabase = get_supabase_client()
        result = supabase.table("embeddings").select("id, metadata").execute()
        
        if result.data:
            print(f"  OK Total embeddings en BD: {len(result.data)}")
            
            # Contar por categoría
            categories = {}
            ccaas = {}
            
            for item in result.data:
                metadata = item.get("metadata", {})
                category = metadata.get("categoria", "sin_categoria")
                ccaa = metadata.get("ccaa", "sin_ccaa")
                
                categories[category] = categories.get(category, 0) + 1
                ccaas[ccaa] = ccaas.get(ccaa, 0) + 1
            
            print("  Distribucion por categoria:")
            for cat, count in sorted(categories.items()):
                print(f"    - {cat}: {count}")
            
            print("  Distribucion por CCAA:")
            for ccaa, count in sorted(ccaas.items()):
                print(f"    - {ccaa}: {count}")
                
        else:
            print("  AVISO No se encontraron embeddings en la BD")
            
    except Exception as e:
        print(f"  ERROR verificando embeddings: {e}")


def test_retrieval():
    """Prueba el sistema de recuperación con consultas de ejemplo."""
    print("\nProbando sistema de recuperación...")
    
    test_queries = [
        "reclamar vuelo cancelado",
        "despido improcedente indemnización",
        "alquiler subida precio",
        "impuesto sucesiones Madrid",
        "tarjeta de residencia extranjeros"
    ]
    
    from app.ai.rag.retriever import retrieve_context
    
    for query in test_queries:
        try:
            results = retrieve_context(query, top_k=3, threshold=0.3)
            print(f"  Query: '{query}' -> {len(results)} resultados")
            
            if results:
                best_result = results[0]
                metadata = best_result.get("metadata", {})
                similarity = best_result.get("similarity", 0)
                print(f"    Mejor resultado: {metadata.get('categoria', 'N/A')} / {metadata.get('subcategoria', 'N/A')} (sim: {similarity:.3f})")
            
        except Exception as e:
            print(f"  ERROR probando '{query}': {e}")


def main():
    """Función principal del script."""
    print("ACTUALIZACION BASE DE CONOCIMIENTO RAG")
    print("=" * 50)
    
    try:
        # 1. Cargar archivos de conocimiento
        knowledge_data = load_knowledge_files()
        
        if not knowledge_data:
            print("❌ No se cargaron datos de conocimiento. Abortando.")
            return
        
        # 2. Limpiar embeddings existentes
        clear_existing_embeddings()
        
        # 3. Procesar y almacenar nuevos embeddings
        process_and_store_embeddings(knowledge_data)
        
        # 4. Verificar resultado
        verify_embeddings()
        
        # 5. Probar recuperación
        test_retrieval()
        
        print("\nActualizacion completada exitosamente!")
        print("La base de conocimiento RAG ha sido expandida con normativa actualizada.")
        
    except Exception as e:
        print(f"\nERROR durante la actualizacion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()