-- Añadir columna para entidades legales extraídas
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS legal_entities JSONB;

-- Añadir índice para búsquedas en entidades legales
CREATE INDEX IF NOT EXISTS idx_conversation_attachments_legal_entities 
ON conversation_attachments USING GIN (legal_entities);

-- Comentario para la nueva columna
COMMENT ON COLUMN conversation_attachments.legal_entities IS 'Entidades legales extraídas del documento (fechas, importes, DNI, etc.)';

-- Función para buscar documentos por tipo de entidad
CREATE OR REPLACE FUNCTION search_documents_by_entity_type(
    p_user_id UUID,
    p_entity_type TEXT
)
RETURNS TABLE (
    attachment_id UUID,
    filename TEXT,
    entity_value TEXT,
    confidence FLOAT,
    created_at TIMESTAMPTZ
)
LANGUAGE SQL
AS $$
    SELECT 
        ca.id as attachment_id,
        ca.filename,
        entity->>'value' as entity_value,
        (entity->>'confidence')::FLOAT as confidence,
        ca.created_at
    FROM conversation_attachments ca,
         jsonb_array_elements(ca.legal_entities->'entities') as entity
    WHERE ca.user_id = p_user_id
      AND entity->>'type' LIKE '%' || p_entity_type || '%'
      AND (entity->>'confidence')::FLOAT > 0.5
    ORDER BY (entity->>'confidence')::FLOAT DESC, ca.created_at DESC;
$$;

-- Función para obtener estadísticas de entidades por usuario
CREATE OR REPLACE FUNCTION get_user_entity_stats(p_user_id UUID)
RETURNS TABLE (
    entity_type TEXT,
    total_count BIGINT,
    avg_confidence FLOAT
)
LANGUAGE SQL
AS $$
    SELECT 
        entity->>'type' as entity_type,
        COUNT(*) as total_count,
        AVG((entity->>'confidence')::FLOAT) as avg_confidence
    FROM conversation_attachments ca,
         jsonb_array_elements(ca.legal_entities->'entities') as entity
    WHERE ca.user_id = p_user_id
      AND ca.legal_entities IS NOT NULL
    GROUP BY entity->>'type'
    ORDER BY total_count DESC;
$$;

-- Comentarios para las funciones
COMMENT ON FUNCTION search_documents_by_entity_type IS 'Busca documentos que contengan un tipo específico de entidad legal';
COMMENT ON FUNCTION get_user_entity_stats IS 'Obtiene estadísticas de entidades legales extraídas para un usuario';