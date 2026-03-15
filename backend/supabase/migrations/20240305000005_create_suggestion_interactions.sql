-- Crear tabla para interacciones con sugerencias proactivas
CREATE TABLE IF NOT EXISTS user_suggestion_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    suggestion_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('seen', 'acted', 'dismissed')),
    action_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE user_suggestion_interactions ENABLE ROW LEVEL SECURITY;

-- Política de seguridad: usuarios solo ven sus propias interacciones
CREATE POLICY "Users can manage own suggestion interactions" 
ON user_suggestion_interactions 
FOR ALL 
USING (auth.uid() = user_id);

-- Índices para rendimiento
CREATE INDEX IF NOT EXISTS idx_suggestion_interactions_user_id 
ON user_suggestion_interactions (user_id);

CREATE INDEX IF NOT EXISTS idx_suggestion_interactions_suggestion_id 
ON user_suggestion_interactions (suggestion_id);

CREATE INDEX IF NOT EXISTS idx_suggestion_interactions_action 
ON user_suggestion_interactions (action);

CREATE INDEX IF NOT EXISTS idx_suggestion_interactions_created_at 
ON user_suggestion_interactions (created_at DESC);

-- Índice compuesto para consultas frecuentes
CREATE INDEX IF NOT EXISTS idx_suggestion_interactions_user_suggestion 
ON user_suggestion_interactions (user_id, suggestion_id);

-- Función para obtener estadísticas de interacción del usuario
CREATE OR REPLACE FUNCTION get_user_suggestion_stats(p_user_id UUID)
RETURNS TABLE (
    total_suggestions_seen BIGINT,
    total_suggestions_acted BIGINT,
    total_suggestions_dismissed BIGINT,
    engagement_rate FLOAT
)
LANGUAGE SQL
AS $$
    WITH stats AS (
        SELECT 
            COUNT(*) FILTER (WHERE action = 'seen') as seen_count,
            COUNT(*) FILTER (WHERE action = 'acted') as acted_count,
            COUNT(*) FILTER (WHERE action = 'dismissed') as dismissed_count,
            COUNT(*) as total_count
        FROM user_suggestion_interactions 
        WHERE user_id = p_user_id
    )
    SELECT 
        seen_count,
        acted_count,
        dismissed_count,
        CASE 
            WHEN seen_count > 0 THEN (acted_count::FLOAT / seen_count::FLOAT)
            ELSE 0.0
        END as engagement_rate
    FROM stats;
$$;

-- Función para limpiar interacciones antiguas (más de 90 días)
CREATE OR REPLACE FUNCTION cleanup_old_suggestion_interactions()
RETURNS INTEGER
LANGUAGE SQL
AS $$
    DELETE FROM user_suggestion_interactions 
    WHERE created_at < NOW() - INTERVAL '90 days';
    
    SELECT ROW_COUNT();
$$;

-- Comentarios para documentación
COMMENT ON TABLE user_suggestion_interactions IS 'Registra las interacciones del usuario con sugerencias proactivas';
COMMENT ON COLUMN user_suggestion_interactions.suggestion_id IS 'ID único de la sugerencia (generado por el servicio)';
COMMENT ON COLUMN user_suggestion_interactions.action IS 'Tipo de acción: seen (vista), acted (ejecutada), dismissed (descartada)';
COMMENT ON COLUMN user_suggestion_interactions.action_data IS 'Datos adicionales sobre la acción realizada';

COMMENT ON FUNCTION get_user_suggestion_stats IS 'Obtiene estadísticas de interacción con sugerencias para un usuario';
COMMENT ON FUNCTION cleanup_old_suggestion_interactions IS 'Limpia interacciones con sugerencias más antiguas de 90 días';