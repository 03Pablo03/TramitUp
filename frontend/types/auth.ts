import { User, Session } from '@supabase/supabase-js';

export interface UserProfile {
  id: string;
  name: string | null;
  email: string | null;
  plan: UserPlan;
  categories_interest: string[];
  onboarding_completed: boolean;
  documents_used_today?: number;
  remaining_chats_today?: number;
}

export type UserPlan = 'free' | 'document' | 'pro';

export interface AuthContextType {
  user: User | null;
  profile: UserProfile | null;
  session: Session | null;
  loading: boolean;
  isPremium: boolean;
  onboardingCompleted: boolean;
  signInWithGoogle: () => Promise<void>;
  signInWithEmail: (email: string, password: string) => Promise<void>;
  signUpWithEmail: (name: string, email: string, password: string, acceptTerms: boolean) => Promise<void>;
  signInWithMagicLink: (email: string) => Promise<void>;
  signOut: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  refreshProfile: () => Promise<void>;
}

export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  name: string;
  email: string;
  password: string;
  acceptTerms: boolean;
}