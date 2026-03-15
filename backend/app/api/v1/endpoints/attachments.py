"""
Endpoints para manejo de archivos adjuntos en conversaciones.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import List, Optional

from app.core.auth import require_auth
from app.services.document_analysis_service import document_analysis_service


router = APIRouter()


@router.post("/upload")
async def upload_attachment(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = Form(None),
    user_id: str = Depends(require_auth)
):
    """
    Sube un archivo adjunto y lo analiza.
    
    Args:
        file: Archivo a subir
        conversation_id: ID de la conversación (opcional)
        user_id: ID del usuario autenticado
        
    Returns:
        Información del archivo subido y análisis
    """
    try:
        # Validar tipo de archivo
        if not file.content_type:
            raise HTTPException(status_code=400, detail="Tipo de archivo no válido")
        
        # Leer contenido del archivo
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="El archivo está vacío")
        
        # Procesar y analizar archivo
        result = await document_analysis_service.upload_and_analyze_file(
            file_content=file_content,
            filename=file.filename or "archivo_sin_nombre",
            content_type=file.content_type,
            user_id=user_id,
            conversation_id=conversation_id
        )
        
        return {
            "success": True,
            "attachment_id": result["attachment_id"],
            "filename": result["filename"],
            "file_size": result["file_size"],
            "file_type": result["file_type"],
            "analysis_summary": result["analysis_summary"],
            "legal_entities": result.get("legal_entities", {}),
            "message": f"Archivo '{result['filename']}' subido y analizado exitosamente"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando archivo: {str(e)}"
        )


@router.get("/{attachment_id}")
async def get_attachment_info(
    attachment_id: str,
    user_id: str = Depends(require_auth)
):
    """
    Obtiene información de un archivo adjunto.
    
    Args:
        attachment_id: ID del archivo adjunto
        user_id: ID del usuario autenticado
        
    Returns:
        Información detallada del archivo
    """
    try:
        attachment_info = document_analysis_service.get_attachment_info(
            attachment_id, user_id
        )
        
        if not attachment_info:
            raise HTTPException(status_code=404, detail="Archivo adjunto no encontrado")
        
        return {
            "success": True,
            "attachment": attachment_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo información del archivo: {str(e)}"
        )


@router.get("/conversation/{conversation_id}")
async def get_conversation_attachments(
    conversation_id: str,
    user_id: str = Depends(require_auth)
):
    """
    Obtiene todos los archivos adjuntos de una conversación.
    
    Args:
        conversation_id: ID de la conversación
        user_id: ID del usuario autenticado
        
    Returns:
        Lista de archivos adjuntos de la conversación
    """
    try:
        attachments = document_analysis_service.get_conversation_attachments(
            conversation_id, user_id
        )
        
        return {
            "success": True,
            "attachments": attachments,
            "total": len(attachments)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo archivos de la conversación: {str(e)}"
        )


@router.delete("/{attachment_id}")
async def delete_attachment(
    attachment_id: str,
    user_id: str = Depends(require_auth)
):
    """
    Elimina un archivo adjunto.
    
    Args:
        attachment_id: ID del archivo adjunto
        user_id: ID del usuario autenticado
        
    Returns:
        Confirmación de eliminación
    """
    try:
        from app.core.supabase_client import get_supabase_client
        
        supabase = get_supabase_client()
        
        # Verificar que el archivo pertenece al usuario
        result = supabase.table("conversation_attachments").select(
            "id, storage_path"
        ).eq("id", attachment_id).eq("user_id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Archivo adjunto no encontrado")
        
        attachment = result.data[0]
        storage_path = attachment.get("storage_path")
        
        # Eliminar archivo del storage
        if storage_path:
            try:
                supabase.storage.from_("documents").remove([storage_path])
            except Exception as e:
                print(f"Warning: Could not delete file from storage: {e}")
        
        # Eliminar registro de la base de datos
        supabase.table("conversation_attachments").delete().eq(
            "id", attachment_id
        ).eq("user_id", user_id).execute()
        
        return {
            "success": True,
            "message": "Archivo adjunto eliminado exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error eliminando archivo adjunto: {str(e)}"
        )