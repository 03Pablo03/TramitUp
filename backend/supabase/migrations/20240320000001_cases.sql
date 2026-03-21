-- TramitUp — Fase 3: Expedientes de caso
-- Tabla principal para agrupar conversaciones, documentos y alertas por situación legal

CREATE TABLE IF NOT EXISTS cases (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id     UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title       TEXT        NOT NULL CHECK (char_length(title) BETWEEN 1 AND 120),
    category    TEXT        CHECK (category IN (
                                'laboral', 'vivienda', 'consumo', 'familia',
                                'trafico', 'administrativo', 'fiscal', 'penal', 'otro'
                            )),
    status      TEXT        NOT NULL DEFAULT 'open'
                            CHECK (status IN ('open', 'resolved', 'archived')),
    summary     TEXT        CHECK (char_length(summary) <= 1000),
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: each user can only access their own cases
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own cases" ON cases
    FOR ALL USING (auth.uid() = user_id);

-- Service role full access (backend uses service_role_key)
CREATE POLICY "Service role full access on cases" ON cases
    FOR ALL USING (true);

-- Index for fast user lookups
CREATE INDEX IF NOT EXISTS idx_cases_user_id ON cases(user_id);
CREATE INDEX IF NOT EXISTS idx_cases_user_status ON cases(user_id, status);

-- Link conversations to cases (nullable, set to NULL if case is deleted)
ALTER TABLE conversations
    ADD COLUMN IF NOT EXISTS case_id UUID REFERENCES cases(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_conversations_case_id ON conversations(case_id);

-- Link alerts to cases
ALTER TABLE alerts
    ADD COLUMN IF NOT EXISTS case_id UUID REFERENCES cases(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_alerts_case_id ON alerts(case_id);
