-- =============================================================================
-- MIGRACIÓN: conversation_attachments — Estructura completa + Seguridad
-- =============================================================================
-- Ejecutar en: Supabase Dashboard → SQL Editor
-- Idempotente: puede ejecutarse varias veces sin errores
-- =============================================================================


-- =============================================================================
-- 1. ESTRUCTURA DE LA TABLA
-- =============================================================================

CREATE TABLE IF NOT EXISTS conversation_attachments (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id           UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    conversation_id   UUID        REFERENCES conversations(id) ON DELETE SET NULL,
    filename          TEXT        NOT NULL,
    file_size         INTEGER,
    file_type         TEXT,
    storage_path      TEXT,
    analysis_summary  TEXT,
    extracted_text    TEXT,
    legal_entities    JSONB,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Añadir columnas faltantes si la tabla ya existía parcialmente
-- (ADD COLUMN IF NOT EXISTS es idempotente — no falla si ya existe)
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS extracted_text    TEXT;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS analysis_summary  TEXT;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS storage_path      TEXT;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS file_size         INTEGER;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS file_type         TEXT;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS legal_entities    JSONB;
ALTER TABLE conversation_attachments ADD COLUMN IF NOT EXISTS updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW();


-- =============================================================================
-- 2. CONSTRAINTS DE INTEGRIDAD
-- =============================================================================

-- Whitelist de tipos MIME permitidos (igual que validación backend)
ALTER TABLE conversation_attachments
    DROP CONSTRAINT IF EXISTS chk_file_type;
ALTER TABLE conversation_attachments
    ADD CONSTRAINT chk_file_type CHECK (
        file_type IS NULL OR file_type IN (
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'image/jpeg',
            'image/jpg',
            'image/png'
        )
    );

-- Tamaño máximo 10 MB (igual que validación backend) y debe ser positivo
ALTER TABLE conversation_attachments
    DROP CONSTRAINT IF EXISTS chk_file_size;
ALTER TABLE conversation_attachments
    ADD CONSTRAINT chk_file_size CHECK (
        file_size IS NULL OR (file_size > 0 AND file_size <= 10485760)
    );

-- Nombre de archivo no puede estar vacío
ALTER TABLE conversation_attachments
    DROP CONSTRAINT IF EXISTS chk_filename_not_empty;
ALTER TABLE conversation_attachments
    ADD CONSTRAINT chk_filename_not_empty CHECK (
        length(trim(filename)) > 0
    );


-- =============================================================================
-- 3. TRIGGER: actualización automática de updated_at
-- =============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_conversation_attachments_updated_at ON conversation_attachments;
CREATE TRIGGER trg_conversation_attachments_updated_at
    BEFORE UPDATE ON conversation_attachments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- =============================================================================
-- 4. ÍNDICES DE RENDIMIENTO
-- =============================================================================

-- Búsqueda de todos los archivos de un usuario (caso más frecuente)
CREATE INDEX IF NOT EXISTS idx_conv_attachments_user_id
    ON conversation_attachments(user_id);

-- Búsqueda de archivos de una conversación
CREATE INDEX IF NOT EXISTS idx_conv_attachments_conversation_id
    ON conversation_attachments(conversation_id);

-- Búsqueda combinada usuario + fecha (listado paginado)
CREATE INDEX IF NOT EXISTS idx_conv_attachments_user_created
    ON conversation_attachments(user_id, created_at DESC);

-- Búsqueda full-text en entidades legales extraídas (JSONB)
CREATE INDEX IF NOT EXISTS idx_conv_attachments_legal_entities
    ON conversation_attachments USING GIN (legal_entities);


-- =============================================================================
-- 5. ROW LEVEL SECURITY (RLS)
-- =============================================================================

ALTER TABLE conversation_attachments ENABLE ROW LEVEL SECURITY;

-- Eliminar políticas existentes para evitar duplicados
DROP POLICY IF EXISTS "Users can view own attachments"   ON conversation_attachments;
DROP POLICY IF EXISTS "Users can insert own attachments" ON conversation_attachments;
DROP POLICY IF EXISTS "Users can update own attachments" ON conversation_attachments;
DROP POLICY IF EXISTS "Users can delete own attachments" ON conversation_attachments;
DROP POLICY IF EXISTS "Service role full access"         ON conversation_attachments;

-- SELECT: solo los propios registros
CREATE POLICY "Users can view own attachments"
    ON conversation_attachments
    FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

-- INSERT: solo para el propio user_id (no puede falsificar user_id de otro)
CREATE POLICY "Users can insert own attachments"
    ON conversation_attachments
    FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- UPDATE: solo propios registros, y no puede cambiar el user_id
CREATE POLICY "Users can update own attachments"
    ON conversation_attachments
    FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- DELETE: solo propios registros
CREATE POLICY "Users can delete own attachments"
    ON conversation_attachments
    FOR DELETE
    TO authenticated
    USING (auth.uid() = user_id);

-- Service role: acceso total (el backend usa service_role_key → bypassa RLS)
-- Esta política actúa como capa de defensa adicional explícita
CREATE POLICY "Service role full access"
    ON conversation_attachments
    FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);


-- =============================================================================
-- 6. STORAGE POLICIES — bucket "documents"
-- =============================================================================
-- El bucket "documents" debe existir como privado (no público).
-- Crear en: Supabase Dashboard → Storage → New bucket → nombre: documents, privado
--
-- Estructura de rutas: attachments/{user_id}/{attachment_id}_{filename}
-- Las políticas se aplican sobre storage.objects.
-- =============================================================================

-- Eliminar políticas existentes del bucket para evitar duplicados
DROP POLICY IF EXISTS "Users can upload to own folder"      ON storage.objects;
DROP POLICY IF EXISTS "Users can read own files"            ON storage.objects;
DROP POLICY IF EXISTS "Users can update own files"          ON storage.objects;
DROP POLICY IF EXISTS "Users can delete own files"          ON storage.objects;
DROP POLICY IF EXISTS "Service role full storage access"    ON storage.objects;

-- UPLOAD: solo en la carpeta attachments/{propio_user_id}/
CREATE POLICY "Users can upload to own folder"
    ON storage.objects
    FOR INSERT
    TO authenticated
    WITH CHECK (
        bucket_id = 'documents'
        AND name LIKE 'attachments/' || auth.uid()::text || '/%'
    );

-- READ: solo los propios archivos
CREATE POLICY "Users can read own files"
    ON storage.objects
    FOR SELECT
    TO authenticated
    USING (
        bucket_id = 'documents'
        AND name LIKE 'attachments/' || auth.uid()::text || '/%'
    );

-- UPDATE: solo los propios archivos (metadatos)
CREATE POLICY "Users can update own files"
    ON storage.objects
    FOR UPDATE
    TO authenticated
    USING (
        bucket_id = 'documents'
        AND name LIKE 'attachments/' || auth.uid()::text || '/%'
    )
    WITH CHECK (
        bucket_id = 'documents'
        AND name LIKE 'attachments/' || auth.uid()::text || '/%'
    );

-- DELETE: solo los propios archivos
CREATE POLICY "Users can delete own files"
    ON storage.objects
    FOR DELETE
    TO authenticated
    USING (
        bucket_id = 'documents'
        AND name LIKE 'attachments/' || auth.uid()::text || '/%'
    );

-- Service role: acceso completo al bucket (el backend usa service_role_key)
CREATE POLICY "Service role full storage access"
    ON storage.objects
    FOR ALL
    TO service_role
    USING (bucket_id = 'documents')
    WITH CHECK (bucket_id = 'documents');


-- =============================================================================
-- 7. FUNCIONES DE BÚSQUEDA (ya existentes — con seguridad añadida)
-- =============================================================================

-- Función para buscar documentos por tipo de entidad legal
CREATE OR REPLACE FUNCTION search_documents_by_entity_type(
    p_user_id    UUID,
    p_entity_type TEXT
)
RETURNS TABLE (
    attachment_id UUID,
    filename      TEXT,
    entity_value  TEXT,
    confidence    FLOAT,
    created_at    TIMESTAMPTZ
)
LANGUAGE SQL
SECURITY INVOKER   -- Ejecuta con los permisos del llamante (respeta RLS)
STABLE             -- No modifica la BD, permite optimizaciones
AS $$
    SELECT
        ca.id           AS attachment_id,
        ca.filename,
        entity->>'value'                   AS entity_value,
        (entity->>'confidence')::FLOAT     AS confidence,
        ca.created_at
    FROM conversation_attachments ca,
         jsonb_array_elements(ca.legal_entities->'entities') AS entity
    WHERE ca.user_id = p_user_id
      AND entity->>'type' LIKE '%' || p_entity_type || '%'
      AND (entity->>'confidence')::FLOAT > 0.5
    ORDER BY (entity->>'confidence')::FLOAT DESC, ca.created_at DESC;
$$;

-- Función para obtener estadísticas de entidades por usuario
CREATE OR REPLACE FUNCTION get_user_entity_stats(p_user_id UUID)
RETURNS TABLE (
    entity_type  TEXT,
    total_count  BIGINT,
    avg_confidence FLOAT
)
LANGUAGE SQL
SECURITY INVOKER
STABLE
AS $$
    SELECT
        entity->>'type'                    AS entity_type,
        COUNT(*)                           AS total_count,
        AVG((entity->>'confidence')::FLOAT) AS avg_confidence
    FROM conversation_attachments ca,
         jsonb_array_elements(ca.legal_entities->'entities') AS entity
    WHERE ca.user_id = p_user_id
      AND ca.legal_entities IS NOT NULL
    GROUP BY entity->>'type'
    ORDER BY total_count DESC;
$$;


-- =============================================================================
-- 8. COMENTARIOS DE DOCUMENTACIÓN
-- =============================================================================

COMMENT ON TABLE conversation_attachments IS
    'Archivos adjuntos subidos por usuarios en conversaciones. RLS activo: cada usuario solo accede a sus propios archivos.';

COMMENT ON COLUMN conversation_attachments.user_id IS
    'Propietario del archivo. FK a auth.users con CASCADE DELETE.';

COMMENT ON COLUMN conversation_attachments.extracted_text IS
    'Primeros 8000 caracteres del texto extraído del documento (PDF/DOCX/imagen).';

COMMENT ON COLUMN conversation_attachments.legal_entities IS
    'Entidades legales extraídas estructuradas (fechas, importes, DNI, etc.) en formato JSONB.';

COMMENT ON COLUMN conversation_attachments.storage_path IS
    'Ruta en Supabase Storage: attachments/{user_id}/{attachment_id}_{filename}';
