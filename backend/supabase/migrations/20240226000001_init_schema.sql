-- TramitUp - Initial schema
-- Requires Supabase with pgvector extension enabled

-- Enable pgvector if not already
CREATE EXTENSION IF NOT EXISTS vector;

-- User profiles (extends auth.users)
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    plan TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'document', 'pro')),
    documents_used_today INTEGER NOT NULL DEFAULT 0,
    last_reset_date DATE DEFAULT CURRENT_DATE,
    stripe_customer_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Service role can do everything (backend uses service_role_key)
CREATE POLICY "Service role full access" ON profiles
    FOR ALL USING (true);

-- Conversations
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT DEFAULT 'Nueva conversación',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own conversations" ON conversations
    FOR ALL USING (auth.uid() = user_id);

-- Messages
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read messages of own conversations" ON messages
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM conversations c
            WHERE c.id = conversation_id AND c.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert messages in own conversations" ON messages
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM conversations c
            WHERE c.id = conversation_id AND c.user_id = auth.uid()
        )
    );

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own documents" ON documents
    FOR ALL USING (auth.uid() = user_id);

-- Embeddings for RAG (pgvector)
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for vector similarity search
CREATE INDEX IF NOT EXISTS embeddings_embedding_idx ON embeddings
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Alerts (stub for Phase 2)
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    deadline DATE NOT NULL,
    notified_at TIMESTAMPTZ[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own alerts" ON alerts
    FOR ALL USING (auth.uid() = user_id);
