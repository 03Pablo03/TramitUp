"""
Servicio mejorado de análisis de documentos con extracción de entidades legales.
Procesa archivos PDF, DOCX e imágenes con análisis estructurado.
"""

import io
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
import PyPDF2
import pdfplumber
from docx import Document as DocxDocument
from PIL import Image
import pytesseract
try:
    from pdf2image import convert_from_bytes
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False

from app.core.supabase_client import get_supabase_client
from app.ai.llm_client import get_llm
from app.services.legal_entity_extractor import legal_entity_extractor


class DocumentAnalysisService:
    """Servicio mejorado de análisis de documentos con extracción de entidades legales."""
    
    def __init__(self):
        self.supported_types = {
            'application/pdf': self._extract_pdf_text,
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': self._extract_docx_text,
            'image/jpeg': self._extract_image_text,
            'image/png': self._extract_image_text,
            'image/jpg': self._extract_image_text
        }
        self.max_text_length = 10000  # Máximo caracteres a procesar
        self.max_file_size = 10 * 1024 * 1024  # 10MB máximo
    
    async def upload_and_analyze_file(
        self, 
        file_content: bytes, 
        filename: str, 
        content_type: str, 
        user_id: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Sube un archivo y lo analiza completamente con extracción de entidades legales.
        
        Args:
            file_content: Contenido del archivo en bytes
            filename: Nombre del archivo
            content_type: Tipo MIME del archivo
            user_id: ID del usuario
            conversation_id: ID de la conversación (opcional)
            
        Returns:
            Diccionario con información del archivo y análisis completo
        """
        # Validaciones iniciales
        if len(file_content) > self.max_file_size:
            raise ValueError(f"Archivo demasiado grande. Máximo {self.max_file_size/1024/1024}MB")

        # Convertir cadena vacía a None para compatibilidad con UUID en BD
        if not conversation_id:
            conversation_id = None
        
        if content_type not in self.supported_types:
            raise ValueError(f"Tipo de archivo no soportado: {content_type}")
        
        # Generar ID único para el archivo
        attachment_id = str(uuid.uuid4())
        
        # Subir archivo a Supabase Storage
        try:
            supabase = get_supabase_client()
            storage_path = f"attachments/{user_id}/{attachment_id}_{filename}"
            
            # Subir archivo
            supabase.storage.from_("documents").upload(
                storage_path, file_content, {"content-type": content_type}
            )
            
            # Generar URL firmada
            url_response = supabase.storage.from_("documents").create_signed_url(
                storage_path, expires_in=86400
            )
            
            upload_url = url_response.get("signedURL", "")
            
        except Exception as e:
            raise ValueError(f"Error subiendo archivo: {str(e)}")
        
        # Extraer texto del archivo
        try:
            print(f"Extracting text from {filename} ({content_type}, {len(file_content)} bytes)")
            extracted_text = self._extract_text_from_file(file_content, content_type)
            print(f"Extracted {len(extracted_text)} characters from {filename}")
        except Exception as e:
            print(f"Error extracting text from {filename}: {e}")
            extracted_text = ""
        
        # Análisis básico con IA
        analysis_summary = ""
        if extracted_text.strip():
            try:
                analysis_summary = await self._analyze_document_with_ai(
                    extracted_text, filename, content_type
                )
                print(f"AI analysis completed for {filename}: {len(analysis_summary)} chars")
            except Exception as e:
                print(f"Error analyzing document with AI: {e}")
                analysis_summary = f"Documento '{filename}' subido correctamente. Texto extraído ({len(extracted_text)} caracteres) pero análisis IA no disponible."
        else:
            analysis_summary = f"Archivo '{filename}' subido correctamente. No se pudo extraer texto para análisis automático."
        
        # NUEVA FUNCIONALIDAD: Extracción de entidades legales
        legal_entities = {}
        if extracted_text.strip():
            try:
                print(f"Extracting legal entities from {filename}...")
                legal_entities = legal_entity_extractor.extract_entities(extracted_text)
                print(f"Legal entities extracted: {legal_entities['extraction_metadata']['total_entities']} entities")
            except Exception as e:
                print(f"Error extracting legal entities: {e}")
                legal_entities = {}
        
        # Guardar información completa en base de datos
        try:
            supabase.table("conversation_attachments").insert({
                "id": attachment_id,
                "user_id": user_id,
                "conversation_id": conversation_id,
                "filename": filename,
                "file_size": len(file_content),
                "file_type": content_type,
                "storage_path": storage_path,
                "analysis_summary": analysis_summary,
                "extracted_text": extracted_text[:8000],  # Primeros 8000 caracteres
                "legal_entities": legal_entities,  # NUEVO: entidades legales extraídas
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }).execute()
            
            print(f"Document analysis saved to database for {filename}")
            
        except Exception as e:
            print(f"Error saving to database: {e}")
            # Continuar aunque falle el guardado en BD
        
        return {
            "attachment_id": attachment_id,
            "filename": filename,
            "file_size": len(file_content),
            "file_type": content_type,
            "upload_url": upload_url,
            "analysis_summary": analysis_summary,
            "extracted_text": extracted_text,
            "legal_entities": legal_entities  # NUEVO: incluir entidades en respuesta
        }
    
    def _extract_text_from_file(self, file_content: bytes, content_type: str) -> str:
        """Extrae texto de un archivo según su tipo."""
        extractor = self.supported_types.get(content_type)
        if not extractor:
            return ""
        
        return extractor(file_content)
    
    def _extract_pdf_text(self, file_content: bytes) -> str:
        """Extrae texto de un PDF usando múltiples métodos."""
        
        # Método 1: Intentar con pdfplumber (más robusto)
        try:
            pdf_file = io.BytesIO(file_content)
            text_parts = []
            
            with pdfplumber.open(pdf_file) as pdf:
                # Limitar a las primeras 10 páginas
                max_pages = min(10, len(pdf.pages))
                
                for page_num in range(max_pages):
                    page = pdf.pages[page_num]
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        text_parts.append(page_text)
            
            if text_parts:
                extracted_text = "\n".join(text_parts)
                print(f"PDF text extracted with pdfplumber: {len(extracted_text)} chars")
                return extracted_text
            else:
                print("pdfplumber: No text found in PDF")
                
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Método 2: Intentar con PyPDF2 (fallback)
        try:
            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text_parts = []
            max_pages = min(10, len(pdf_reader.pages))
            
            for page_num in range(max_pages):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                if page_text and page_text.strip():
                    text_parts.append(page_text)
            
            if text_parts:
                extracted_text = "\n".join(text_parts)
                print(f"PDF text extracted with PyPDF2: {len(extracted_text)} chars")
                return extracted_text
            else:
                print("PyPDF2: No text found in PDF")
                
        except Exception as e:
            print(f"PyPDF2 failed: {e}")
        
        # Método 3: OCR como último recurso (si pdf2image está disponible)
        if PDF2IMAGE_AVAILABLE:
            try:
                print("Attempting OCR extraction from PDF...")
                # Convertir PDF a imágenes
                images = convert_from_bytes(file_content, first_page=1, last_page=3)  # Solo primeras 3 páginas para OCR
                
                text_parts = []
                for i, image in enumerate(images):
                    try:
                        # Usar OCR en cada página
                        page_text = pytesseract.image_to_string(image, lang='spa+eng')
                        if page_text and page_text.strip():
                            text_parts.append(f"--- Página {i+1} (OCR) ---\n{page_text}")
                    except Exception as ocr_e:
                        print(f"OCR failed for page {i+1}: {ocr_e}")
                        continue
                
                if text_parts:
                    extracted_text = "\n".join(text_parts)
                    print(f"PDF text extracted with OCR: {len(extracted_text)} chars")
                    return extracted_text
                    
            except Exception as e:
                print(f"OCR extraction failed: {e}")
        
        print("All PDF extraction methods failed")
        return "No se pudo extraer texto del PDF. El archivo se ha subido correctamente pero requiere revisión manual."
    
    def _extract_docx_text(self, file_content: bytes) -> str:
        """Extrae texto de un documento DOCX."""
        try:
            doc_file = io.BytesIO(file_content)
            doc = DocxDocument(doc_file)
            
            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)
            
            return "\n".join(text_parts)
        except Exception as e:
            print(f"Error extracting DOCX text: {e}")
            return ""
    
    def _extract_image_text(self, file_content: bytes) -> str:
        """Extrae texto de una imagen usando OCR."""
        try:
            image = Image.open(io.BytesIO(file_content))
            # Usar OCR con idiomas español e inglés
            text = pytesseract.image_to_string(image, lang='spa+eng')
            return text
        except Exception as e:
            print(f"Error extracting image text: {e}")
            return ""
    
    async def _analyze_document_with_ai(
        self, 
        text: str, 
        filename: str, 
        content_type: str
    ) -> str:
        """Analiza el documento con IA para generar un resumen mejorado."""
        
        if not text or len(text.strip()) < 10:
            return f"Documento '{filename}' subido correctamente. No se pudo extraer texto para análisis automático."
        
        prompt = f"""Analiza este documento legal/administrativo y extrae información clave:

ARCHIVO: {filename}
TIPO: {content_type}

CONTENIDO:
{text[:3000]}

INSTRUCCIONES:
1. Identifica el tipo de documento (factura, multa, contrato, notificación, etc.)
2. Extrae datos clave: fechas, importes, números de referencia, nombres, direcciones
3. Identifica si hay plazos o fechas límite mencionados
4. Resume el contenido en 2-3 frases útiles para trámites legales

FORMATO DE RESPUESTA:
Tipo: [tipo de documento]
Datos clave: [información relevante]
Resumen: [descripción concisa]
Plazos detectados: [si hay fechas límite o plazos]

Responde en español, sé preciso y enfócate en información útil para reclamaciones o trámites."""

        try:
            llm = get_llm(temperature=0.2, max_output_tokens=1500)
            response = llm.invoke(prompt)
            
            # Extraer contenido de la respuesta
            content = response.content if hasattr(response, 'content') else str(response)
            return content.strip()
            
        except Exception as e:
            print(f"Error in AI document analysis: {e}")
            return f"Documento '{filename}' analizado. Texto extraído correctamente pero análisis detallado no disponible."
    
    def get_attachment_info(self, attachment_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información completa de un archivo adjunto."""
        try:
            supabase = get_supabase_client()
            result = supabase.table("conversation_attachments").select(
                "id, filename, file_size, file_type, analysis_summary, extracted_text, legal_entities, created_at"
            ).eq("id", attachment_id).eq("user_id", user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            print(f"Error getting attachment info: {e}")
            return None
    
    def get_conversation_attachments(self, conversation_id: str, user_id: str) -> List[Dict[str, Any]]:
        """Obtiene todos los archivos adjuntos de una conversación."""
        try:
            supabase = get_supabase_client()
            result = supabase.table("conversation_attachments").select(
                "id, filename, file_size, file_type, analysis_summary, created_at"
            ).eq("conversation_id", conversation_id).eq("user_id", user_id).order("created_at", desc=True).execute()
            
            return result.data or []
            
        except Exception as e:
            print(f"Error getting conversation attachments: {e}")
            return []
    
    def get_attachment_texts(self, attachment_ids: List[str], user_id: str) -> List[str]:
        """Devuelve el texto extraído de cada adjunto (solo los que tienen texto)."""
        if not attachment_ids:
            return []
        try:
            supabase = get_supabase_client()
            result = supabase.table("conversation_attachments").select(
                "extracted_text"
            ).in_("id", attachment_ids).eq("user_id", user_id).execute()
            return [
                row["extracted_text"]
                for row in (result.data or [])
                if row.get("extracted_text") and row["extracted_text"].strip()
            ]
        except Exception:
            return []

    def get_enhanced_document_context(self, attachment_ids: List[str], user_id: str) -> str:
        """
        NUEVA FUNCIONALIDAD: Obtiene contexto enriquecido de documentos con entidades legales.
        
        Args:
            attachment_ids: Lista de IDs de archivos adjuntos
            user_id: ID del usuario
            
        Returns:
            Contexto enriquecido con entidades legales extraídas
        """
        if not attachment_ids:
            return ""
        
        context_parts = []
        
        for attachment_id in attachment_ids:
            attachment_info = self.get_attachment_info(attachment_id, user_id)
            
            if attachment_info:
                filename = attachment_info['filename']
                analysis = attachment_info.get('analysis_summary', '')
                extracted_text = attachment_info.get('extracted_text', '')
                legal_entities = attachment_info.get('legal_entities', {})

                context_part = f"DOCUMENTO ADJUNTO: {filename}\n"

                # Incluir el texto real del documento (prioridad máxima)
                if extracted_text and extracted_text.strip():
                    context_part += f"CONTENIDO DEL DOCUMENTO:\n{extracted_text}\n"

                if analysis:
                    context_part += f"\nResumen del análisis: {analysis}\n"

                # Añadir entidades legales extraídas
                if legal_entities and legal_entities.get('entities'):
                    context_part += "Entidades detectadas:\n"

                    entities = legal_entities['entities']
                    for entity in entities[:10]:  # Limitar a 10 entidades más relevantes
                        entity_type = entity.get('type', 'unknown')
                        entity_value = entity.get('value', '')
                        confidence = entity.get('confidence', 0)

                        if confidence > 0.5:  # Solo entidades con confianza alta
                            context_part += f"- {entity_type}: {entity_value}\n"

                # Añadir datos específicos del documento
                specific_data = legal_entities.get('specific_data', {})
                if specific_data:
                    context_part += "Datos específicos:\n"
                    for key, value in specific_data.items():
                        context_part += f"- {key}: {value}\n"

                context_parts.append(context_part)
        
        if context_parts:
            return "\n=== DOCUMENTOS ADJUNTOS POR EL USUARIO ===\nEl usuario ha adjuntado los siguientes documentos. Usa su contenido para responder con precisión:\n\n" + "\n\n".join(context_parts) + "\n=== FIN DOCUMENTOS ADJUNTOS ===\n"
        
        return ""


# Instancia global del servicio
document_analysis_service = DocumentAnalysisService()