"""
Servicio de extracción de entidades legales de documentos.
Extrae información estructurada específica del dominio legal.
"""

import re
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from app.ai.llm_client import get_llm


@dataclass
class LegalEntity:
    """Entidad legal extraída de un documento."""
    type: str  # tipo de entidad (fecha, importe, dni, etc.)
    value: str  # valor extraído
    confidence: float  # confianza en la extracción (0-1)
    context: str  # contexto donde se encontró
    position: Optional[Tuple[int, int]] = None  # posición en el texto


@dataclass
class DocumentStructure:
    """Estructura identificada del documento."""
    document_type: str  # tipo de documento identificado
    sections: Dict[str, str]  # secciones identificadas
    confidence: float  # confianza en la identificación


class LegalEntityExtractor:
    """Extractor de entidades legales de documentos."""
    
    def __init__(self):
        self.patterns = self._load_extraction_patterns()
        self.document_types = self._load_document_types()
    
    def extract_entities(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Extrae entidades legales de un texto.
        
        Args:
            text: Texto del documento
            document_type: Tipo de documento si se conoce
            
        Returns:
            Diccionario con entidades extraídas y estructura del documento
        """
        # 1. Identificar tipo de documento si no se proporciona
        if not document_type:
            doc_structure = self._identify_document_structure(text)
            document_type = doc_structure.document_type
        else:
            doc_structure = DocumentStructure(document_type, {}, 1.0)
        
        # 2. Extraer entidades usando patrones regex
        regex_entities = self._extract_with_regex(text)
        
        # 3. Extraer entidades usando IA
        ai_entities = self._extract_with_ai(text, document_type)
        
        # 4. Combinar y validar resultados
        combined_entities = self._combine_and_validate(regex_entities, ai_entities)
        
        # 5. Extraer información específica por tipo de documento
        specific_data = self._extract_document_specific_data(text, document_type)
        
        return {
            "document_structure": doc_structure,
            "entities": combined_entities,
            "specific_data": specific_data,
            "extraction_metadata": {
                "total_entities": len(combined_entities),
                "confidence_avg": sum(e.confidence for e in combined_entities) / len(combined_entities) if combined_entities else 0,
                "extraction_methods": ["regex", "ai"],
                "document_type": document_type
            }
        }
    
    def _load_extraction_patterns(self) -> Dict[str, Dict[str, str]]:
        """Carga patrones regex para extracción de entidades."""
        return {
            "fechas": {
                "fecha_completa": r"(\d{1,2})[/\-\.](\d{1,2})[/\-\.](\d{2,4})",
                "fecha_texto": r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})",
                "fecha_iso": r"(\d{4})[/\-](\d{1,2})[/\-](\d{1,2})"
            },
            "importes": {
                "euros": r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*€?",
                "euros_texto": r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*euros?",
                "cantidad": r"(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*EUR"
            },
            "identificadores": {
                "dni": r"(\d{8}[A-Z])",
                "nie": r"([XYZ]\d{7}[A-Z])",
                "cif": r"([ABCDEFGHJNPQRSUVW]\d{7}[0-9A-J])",
                "nif": r"(\d{8}[A-Z]|[XYZ]\d{7}[A-Z])"
            },
            "referencias": {
                "expediente": r"(?:expediente|exp\.?)\s*:?\s*([A-Z0-9\-/]+)",
                "numero_factura": r"(?:factura|fact\.?)\s*n[úº]?\.?\s*:?\s*([A-Z0-9\-/]+)",
                "numero_contrato": r"(?:contrato|cto\.?)\s*n[úº]?\.?\s*:?\s*([A-Z0-9\-/]+)"
            },
            "contacto": {
                "telefono": r"(\d{3}\s?\d{3}\s?\d{3}|\d{3}\s?\d{2}\s?\d{2}\s?\d{2})",
                "email": r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
                "direccion": r"((?:calle|c/|avda|av\.|plaza|pl\.|paseo|p\.)\s+[^,\n]+(?:,\s*\d{5})?)"
            },
            "plazos": {
                "dias": r"(\d+)\s*días?\s*(?:hábiles|naturales|laborables)?",
                "meses": r"(\d+)\s*meses?",
                "plazo": r"plazo\s+de\s+(\d+)\s*(días?|meses?|años?)"
            }
        }
    
    def _load_document_types(self) -> Dict[str, Dict[str, Any]]:
        """Carga definiciones de tipos de documentos."""
        return {
            "factura": {
                "keywords": ["factura", "importe", "iva", "total", "cliente", "proveedor"],
                "required_fields": ["importe", "fecha", "numero_factura"],
                "sections": ["datos_emisor", "datos_cliente", "detalle", "totales"]
            },
            "contrato_alquiler": {
                "keywords": ["alquiler", "arrendamiento", "renta", "fianza", "inquilino", "arrendador"],
                "required_fields": ["importe_renta", "fecha_inicio", "duracion"],
                "sections": ["partes", "objeto", "precio", "duracion", "clausulas"]
            },
            "nomina": {
                "keywords": ["nómina", "salario", "cotización", "bruto", "neto", "empresa"],
                "required_fields": ["salario_bruto", "salario_neto", "periodo"],
                "sections": ["datos_empresa", "datos_trabajador", "devengos", "deducciones"]
            },
            "multa": {
                "keywords": ["sanción", "multa", "infracción", "denuncia", "importe"],
                "required_fields": ["importe_multa", "fecha_infraccion", "normativa"],
                "sections": ["datos_sancionado", "hechos", "normativa", "sancion"]
            },
            "sentencia": {
                "keywords": ["sentencia", "juzgado", "fallo", "demandante", "demandado"],
                "required_fields": ["numero_procedimiento", "fecha_sentencia", "fallo"],
                "sections": ["encabezamiento", "antecedentes", "fundamentos", "fallo"]
            },
            "carta_presentacion": {
                "keywords": ["estimados", "candidatura", "puesto", "experiencia", "atentamente"],
                "required_fields": ["nombre", "puesto_solicitado"],
                "sections": ["encabezado", "presentacion", "experiencia", "cierre"]
            }
        }
    
    def _identify_document_structure(self, text: str) -> DocumentStructure:
        """Identifica el tipo y estructura del documento."""
        text_lower = text.lower()
        
        # Calcular puntuación para cada tipo de documento
        scores = {}
        for doc_type, config in self.document_types.items():
            score = 0
            keywords = config.get("keywords", [])
            
            for keyword in keywords:
                # Contar ocurrencias de palabras clave
                count = text_lower.count(keyword.lower())
                score += count * (2 if len(keyword) > 5 else 1)  # Palabras más largas tienen más peso
            
            # Normalizar por longitud del texto
            scores[doc_type] = score / (len(text) / 1000) if len(text) > 0 else 0
        
        # Identificar el tipo con mayor puntuación
        if scores:
            best_type = max(scores.items(), key=lambda x: x[1])
            if best_type[1] > 0.1:  # Umbral mínimo de confianza
                confidence = min(best_type[1] / 10, 1.0)  # Normalizar confianza
                return DocumentStructure(
                    document_type=best_type[0],
                    sections={},
                    confidence=confidence
                )
        
        return DocumentStructure("desconocido", {}, 0.0)
    
    def _extract_with_regex(self, text: str) -> List[LegalEntity]:
        """Extrae entidades usando patrones regex."""
        entities = []
        
        for category, patterns in self.patterns.items():
            for pattern_name, pattern in patterns.items():
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    # Obtener contexto (50 caracteres antes y después)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end].replace('\n', ' ').strip()
                    
                    # Calcular confianza basada en el patrón
                    confidence = self._calculate_regex_confidence(pattern_name, match.group())
                    
                    entities.append(LegalEntity(
                        type=f"{category}_{pattern_name}",
                        value=match.group().strip(),
                        confidence=confidence,
                        context=context,
                        position=(match.start(), match.end())
                    ))
        
        return entities
    
    def _extract_with_ai(self, text: str, document_type: str) -> List[LegalEntity]:
        """Extrae entidades usando IA."""
        try:
            prompt = f"""Analiza el siguiente documento legal y extrae entidades estructuradas.

TIPO DE DOCUMENTO: {document_type}

TEXTO DEL DOCUMENTO:
{text[:3000]}  # Limitar para evitar exceso de tokens

INSTRUCCIONES:
Extrae las siguientes entidades si están presentes:
- Fechas (formato: YYYY-MM-DD)
- Importes monetarios (formato: cantidad en euros)
- Identificadores (DNI, NIE, CIF, números de expediente)
- Nombres de personas y empresas
- Direcciones
- Teléfonos y emails
- Plazos y fechas límite
- Referencias legales (leyes, artículos)

FORMATO DE RESPUESTA (JSON):
{{
  "entities": [
    {{
      "type": "fecha",
      "value": "2024-03-15",
      "confidence": 0.9,
      "context": "fecha de emisión de la factura"
    }}
  ]
}}

Responde SOLO con el JSON, sin explicaciones adicionales."""

            llm = get_llm(temperature=0.1, max_output_tokens=2000)
            response = llm.invoke(prompt)
            
            # Extraer contenido de la respuesta
            content = response.content if hasattr(response, 'content') else str(response)
            
            # Parsear JSON
            import json
            try:
                # Limpiar la respuesta para extraer solo el JSON
                json_start = content.find('{')
                json_end = content.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_content = content[json_start:json_end]
                    data = json.loads(json_content)
                    
                    entities = []
                    for entity_data in data.get("entities", []):
                        entities.append(LegalEntity(
                            type=entity_data.get("type", "unknown"),
                            value=entity_data.get("value", ""),
                            confidence=entity_data.get("confidence", 0.5),
                            context=entity_data.get("context", "")
                        ))
                    
                    return entities
            except json.JSONDecodeError:
                print(f"Error parsing AI response JSON: {content[:200]}")
                return []
            
        except Exception as e:
            print(f"Error in AI entity extraction: {e}")
            return []
    
    def _combine_and_validate(self, regex_entities: List[LegalEntity], 
                            ai_entities: List[LegalEntity]) -> List[LegalEntity]:
        """Combina y valida entidades de diferentes métodos."""
        combined = []
        
        # Añadir entidades regex (generalmente más precisas)
        for entity in regex_entities:
            if self._validate_entity(entity):
                combined.append(entity)
        
        # Añadir entidades AI que no estén duplicadas
        for ai_entity in ai_entities:
            if self._validate_entity(ai_entity):
                # Verificar si ya existe una entidad similar
                is_duplicate = False
                for existing in combined:
                    if (existing.type.split('_')[0] == ai_entity.type and 
                        self._are_similar_values(existing.value, ai_entity.value)):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    combined.append(ai_entity)
        
        # Ordenar por confianza descendente
        combined.sort(key=lambda x: x.confidence, reverse=True)
        
        return combined
    
    def _extract_document_specific_data(self, text: str, document_type: str) -> Dict[str, Any]:
        """Extrae datos específicos según el tipo de documento."""
        specific_extractors = {
            "factura": self._extract_invoice_data,
            "contrato_alquiler": self._extract_rental_contract_data,
            "nomina": self._extract_payroll_data,
            "multa": self._extract_fine_data,
            "sentencia": self._extract_sentence_data
        }
        
        extractor = specific_extractors.get(document_type)
        if extractor:
            return extractor(text)
        
        return {}
    
    def _extract_invoice_data(self, text: str) -> Dict[str, Any]:
        """Extrae datos específicos de facturas."""
        data = {}
        
        # Buscar número de factura
        factura_match = re.search(r"(?:factura|fact\.?)\s*n[úº]?\.?\s*:?\s*([A-Z0-9\-/]+)", text, re.IGNORECASE)
        if factura_match:
            data["numero_factura"] = factura_match.group(1)
        
        # Buscar IVA
        iva_match = re.search(r"iva\s*(?:\d+%?)?\s*:?\s*(\d+(?:,\d{2})?)", text, re.IGNORECASE)
        if iva_match:
            data["iva"] = iva_match.group(1)
        
        # Buscar total
        total_match = re.search(r"total\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if total_match:
            data["total"] = total_match.group(1)
        
        return data
    
    def _extract_rental_contract_data(self, text: str) -> Dict[str, Any]:
        """Extrae datos específicos de contratos de alquiler."""
        data = {}
        
        # Buscar renta mensual
        renta_match = re.search(r"renta\s*(?:mensual)?\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if renta_match:
            data["renta_mensual"] = renta_match.group(1)
        
        # Buscar fianza
        fianza_match = re.search(r"fianza\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if fianza_match:
            data["fianza"] = fianza_match.group(1)
        
        # Buscar duración
        duracion_match = re.search(r"duración\s*:?\s*(\d+)\s*(años?|meses?)", text, re.IGNORECASE)
        if duracion_match:
            data["duracion"] = f"{duracion_match.group(1)} {duracion_match.group(2)}"
        
        return data
    
    def _extract_payroll_data(self, text: str) -> Dict[str, Any]:
        """Extrae datos específicos de nóminas."""
        data = {}
        
        # Buscar salario bruto
        bruto_match = re.search(r"(?:bruto|total\s+devengado)\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if bruto_match:
            data["salario_bruto"] = bruto_match.group(1)
        
        # Buscar salario neto
        neto_match = re.search(r"(?:neto|líquido\s+a\s+percibir)\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if neto_match:
            data["salario_neto"] = neto_match.group(1)
        
        return data
    
    def _extract_fine_data(self, text: str) -> Dict[str, Any]:
        """Extrae datos específicos de multas."""
        data = {}
        
        # Buscar importe de la multa
        multa_match = re.search(r"(?:multa|sanción|importe)\s*:?\s*(\d+(?:\.\d{3})*(?:,\d{2})?)", text, re.IGNORECASE)
        if multa_match:
            data["importe_multa"] = multa_match.group(1)
        
        # Buscar normativa aplicada
        normativa_match = re.search(r"(?:artículo|art\.?)\s*(\d+(?:\.\d+)?)", text, re.IGNORECASE)
        if normativa_match:
            data["articulo"] = normativa_match.group(1)
        
        return data
    
    def _extract_sentence_data(self, text: str) -> Dict[str, Any]:
        """Extrae datos específicos de sentencias."""
        data = {}
        
        # Buscar número de procedimiento
        proc_match = re.search(r"(?:procedimiento|proc\.?)\s*n[úº]?\.?\s*:?\s*([A-Z0-9\-/]+)", text, re.IGNORECASE)
        if proc_match:
            data["numero_procedimiento"] = proc_match.group(1)
        
        # Buscar juzgado
        juzgado_match = re.search(r"juzgado\s+([^,\n]+)", text, re.IGNORECASE)
        if juzgado_match:
            data["juzgado"] = juzgado_match.group(1).strip()
        
        return data
    
    def _calculate_regex_confidence(self, pattern_name: str, value: str) -> float:
        """Calcula la confianza de una extracción regex."""
        base_confidence = 0.8
        
        # Ajustar confianza según el patrón
        if "fecha" in pattern_name:
            # Validar formato de fecha
            if self._is_valid_date(value):
                return min(base_confidence + 0.1, 1.0)
            return base_confidence - 0.2
        
        elif "dni" in pattern_name or "nie" in pattern_name:
            # Validar DNI/NIE
            if self._is_valid_dni_nie(value):
                return min(base_confidence + 0.15, 1.0)
            return base_confidence - 0.3
        
        elif "euros" in pattern_name:
            # Validar formato de importe
            if self._is_valid_amount(value):
                return base_confidence
            return base_confidence - 0.1
        
        return base_confidence
    
    def _validate_entity(self, entity: LegalEntity) -> bool:
        """Valida si una entidad es correcta."""
        if not entity.value or len(entity.value.strip()) == 0:
            return False
        
        if entity.confidence < 0.3:  # Umbral mínimo de confianza
            return False
        
        # Validaciones específicas por tipo
        if "fecha" in entity.type:
            return self._is_valid_date(entity.value)
        elif "dni" in entity.type or "nie" in entity.type:
            return self._is_valid_dni_nie(entity.value)
        elif "email" in entity.type:
            return self._is_valid_email(entity.value)
        
        return True
    
    def _are_similar_values(self, value1: str, value2: str) -> bool:
        """Determina si dos valores son similares (para evitar duplicados)."""
        # Normalizar valores
        v1 = re.sub(r'\s+', '', value1.lower())
        v2 = re.sub(r'\s+', '', value2.lower())
        
        # Calcular similitud simple
        if v1 == v2:
            return True
        
        # Para fechas, comparar componentes
        if self._is_valid_date(value1) and self._is_valid_date(value2):
            return self._normalize_date(value1) == self._normalize_date(value2)
        
        # Para importes, comparar valores numéricos
        if self._is_valid_amount(value1) and self._is_valid_amount(value2):
            return self._normalize_amount(value1) == self._normalize_amount(value2)
        
        return False
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Valida si una cadena representa una fecha válida."""
        try:
            # Intentar varios formatos de fecha
            formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d", "%Y/%m/%d"]
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str.strip(), fmt)
                    # Verificar que la fecha esté en un rango razonable
                    if 1900 <= parsed_date.year <= 2030:
                        return True
                except ValueError:
                    continue
            
            return False
        except:
            return False
    
    def _is_valid_dni_nie(self, dni_nie: str) -> bool:
        """Valida DNI o NIE español."""
        dni_nie = dni_nie.upper().strip()
        
        # Validar formato
        if len(dni_nie) != 9:
            return False
        
        # Validar DNI
        if dni_nie[0].isdigit():
            letters = "TRWAGMYFPDXBNJZSQVHLCKE"
            try:
                number = int(dni_nie[:8])
                letter = dni_nie[8]
                return letters[number % 23] == letter
            except:
                return False
        
        # Validar NIE
        elif dni_nie[0] in 'XYZ':
            letters = "TRWAGMYFPDXBNJZSQVHLCKE"
            try:
                # Convertir primera letra a número
                first_digit = {'X': '0', 'Y': '1', 'Z': '2'}[dni_nie[0]]
                number = int(first_digit + dni_nie[1:8])
                letter = dni_nie[8]
                return letters[number % 23] == letter
            except:
                return False
        
        return False
    
    def _is_valid_email(self, email: str) -> bool:
        """Valida formato de email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    def _is_valid_amount(self, amount: str) -> bool:
        """Valida formato de importe monetario."""
        # Limpiar y normalizar
        clean_amount = re.sub(r'[€\s]', '', amount.strip())
        
        # Verificar formato español (punto para miles, coma para decimales)
        pattern = r'^\d{1,3}(?:\.\d{3})*(?:,\d{2})?$'
        return bool(re.match(pattern, clean_amount))
    
    def _normalize_date(self, date_str: str) -> str:
        """Normaliza una fecha al formato YYYY-MM-DD."""
        try:
            formats = ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y-%m-%d"]
            
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(date_str.strip(), fmt)
                    return parsed_date.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            
            return date_str
        except:
            return date_str
    
    def _normalize_amount(self, amount: str) -> float:
        """Normaliza un importe a float."""
        try:
            # Limpiar formato español
            clean = re.sub(r'[€\s]', '', amount.strip())
            clean = clean.replace('.', '').replace(',', '.')
            return float(clean)
        except:
            return 0.0


# Instancia global del extractor
legal_entity_extractor = LegalEntityExtractor()