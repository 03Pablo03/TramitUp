-- Add category, subcategory, updated_at to conversations
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS category TEXT;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS subcategory TEXT;
ALTER TABLE conversations ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Daily usage for rate limiting (free users)
CREATE TABLE IF NOT EXISTS daily_usage (
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    message_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, date)
);

ALTER TABLE daily_usage ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own daily usage" ON daily_usage
    FOR ALL USING (auth.uid() = user_id);
