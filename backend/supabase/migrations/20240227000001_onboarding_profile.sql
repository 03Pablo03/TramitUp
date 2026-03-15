-- Add onboarding columns to profiles (user_profiles in spec = profiles in our schema)
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS categories_interest TEXT[] DEFAULT '{}';
ALTER TABLE profiles ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT false;

-- Update trigger to set name from OAuth metadata
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(COALESCE(NEW.email, ''), '@', 1))
    )
    ON CONFLICT (id) DO UPDATE SET
        email = EXCLUDED.email,
        name = COALESCE(EXCLUDED.name, profiles.name);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
