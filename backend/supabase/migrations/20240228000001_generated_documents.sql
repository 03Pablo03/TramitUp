-- Tabla de documentos generados (modelos de escritos)
CREATE TABLE IF NOT EXISTS generated_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    document_type TEXT NOT NULL,
    pdf_path TEXT,
    docx_path TEXT,
    data_json JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE generated_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_see_own_generated_documents"
    ON generated_documents FOR ALL USING (auth.uid() = user_id);

-- Índice para listado por usuario
CREATE INDEX IF NOT EXISTS idx_generated_documents_user_created
    ON generated_documents (user_id, created_at DESC);

-- NOTA: Crear bucket "documents" en Supabase Storage (Dashboard > Storage > New bucket)
-- Configuración: Private, no public
