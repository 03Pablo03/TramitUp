-- Tabla de alertas de plazos legales (solo PRO)
-- Reemplaza el stub de init_schema (document_id, title, deadline) por el esquema completo

DROP TABLE IF EXISTS alert_notifications;
DROP TABLE IF EXISTS alerts;

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    description TEXT NOT NULL,
    deadline_date DATE NOT NULL,
    law_reference TEXT,
    notify_days_before INTEGER[] DEFAULT '{7,3,1}',
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'expired', 'dismissed')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alert_notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id UUID NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    days_before INTEGER,
    email_id TEXT
);

ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE alert_notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_see_own_alerts"
    ON alerts FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "users_see_own_notifications"
    ON alert_notifications FOR ALL
    USING (alert_id IN (SELECT id FROM alerts WHERE user_id = auth.uid()));

CREATE INDEX IF NOT EXISTS idx_alerts_deadline_active
    ON alerts(deadline_date) WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_alerts_user_status
    ON alerts(user_id, status, deadline_date);
