-- Add workflow tracking columns to cases
ALTER TABLE cases ADD COLUMN IF NOT EXISTS workflow_steps JSONB DEFAULT '[]';
ALTER TABLE cases ADD COLUMN IF NOT EXISTS required_documents JSONB DEFAULT '[]';
ALTER TABLE cases ADD COLUMN IF NOT EXISTS progress_pct INTEGER DEFAULT 0;
ALTER TABLE cases ADD COLUMN IF NOT EXISTS next_action TEXT;
ALTER TABLE cases ADD COLUMN IF NOT EXISTS next_action_deadline DATE;
ALTER TABLE cases ADD COLUMN IF NOT EXISTS subcategory TEXT;

-- Add user profile fields for enhanced onboarding
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS situation_type TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS first_scenario TEXT;

-- Create tramite wizards table
CREATE TABLE IF NOT EXISTS tramite_wizards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    case_id UUID REFERENCES cases(id),
    template_id TEXT NOT NULL,
    current_step TEXT NOT NULL,
    step_data JSONB DEFAULT '{}',
    status TEXT DEFAULT 'in_progress',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_wizards_user ON tramite_wizards(user_id);
CREATE INDEX IF NOT EXISTS idx_wizards_status ON tramite_wizards(user_id, status);

-- RLS for tramite_wizards
ALTER TABLE tramite_wizards ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own wizards"
    ON tramite_wizards
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- Message feedback table
CREATE TABLE IF NOT EXISTS message_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    message_index INTEGER NOT NULL,
    user_id UUID NOT NULL,
    rating TEXT NOT NULL CHECK (rating IN ('positive', 'negative')),
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_feedback_conv ON message_feedback(conversation_id);

ALTER TABLE message_feedback ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own feedback"
    ON message_feedback
    FOR ALL
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());
