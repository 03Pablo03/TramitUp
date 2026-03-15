"use client";

import React, { createContext, useContext, useEffect, useState, useCallback } from "react";
import { Session, User } from "@supabase/supabase-js";
import { createClient } from "@/lib/supabase/client";
import { setServerAccessToken } from "@/lib/api";

export type UserProfile = {
  id: string;
  name: string | null;
  email: string | null;
  plan: string;
  categories_interest: string[];
  onboarding_completed: boolean;
};

export type AuthContextType = {
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
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function profileFromRow(row: Record<string, unknown> | null): UserProfile | null {
  if (!row) return null;
  return {
    id: String(row.id),
    name: (row.name as string) ?? null,
    email: (row.email as string) ?? null,
    plan: (row.plan as string) ?? "free",
    categories_interest: Array.isArray(row.categories_interest) ? (row.categories_interest as string[]) : [],
    onboarding_completed: Boolean(row.onboarding_completed),
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [serverUser, setServerUser] = useState<User | null>(null);
  const supabase = createClient();

  const fetchProfile = useCallback(async (userId: string) => {
    const { data, error } = await supabase
      .from("profiles")
      .select("id, name, email, plan, categories_interest, onboarding_completed")
      .eq("id", userId)
      .single();
    if (!error && data) {
      setProfile(profileFromRow(data));
    } else {
      setProfile(null);
    }
  }, [supabase]);

  const refreshProfile = useCallback(async () => {
    if (session?.user?.id) {
      await fetchProfile(session.user.id);
    }
  }, [session?.user?.id, fetchProfile]);

  useEffect(() => {
    supabase.auth.getSession().then(async ({ data: { session: s } }) => {
      setSession(s);
      if (s?.user?.id) {
        await fetchProfile(s.user.id);
      } else {
        setProfile(null);
      }
      setLoading(false);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, s) => {
        setSession(s);
        if (s?.user?.id) {
          await fetchProfile(s.user.id);
        } else {
          setProfile(null);
        }
        setLoading(false);
      }
    );
    return () => subscription.unsubscribe();
  }, [fetchProfile]);

  // Si getSession() se bloquea (lock Supabase), usar sesión del servidor sin depender de setSession()
  useEffect(() => {
    const t = setTimeout(async () => {
      const res = await fetch("/api/auth/me", { credentials: "include" });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.user && data.access_token) {
        setServerAccessToken(data.access_token);
        setServerUser({ id: data.user.id, email: data.user.email ?? undefined } as User);
        setLoading(false);
        supabase.auth.setSession({
          access_token: data.access_token,
          refresh_token: data.refresh_token ?? "",
        }).then(() => {}).catch((error) => {
          // Fallback silencioso es intencional aquí
          if (process.env.NODE_ENV === "development") {
            console.warn("Failed to set session from server fallback:", error);
          }
        });
      } else if (res.status === 401) {
        setLoading(false);
      }
    }, 2000);
    return () => clearTimeout(t);
  }, [supabase]);

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
    if (error) throw error;
  };

  const signInWithEmail = async (email: string, password: string) => {
    try {
      const res = await fetch("/api/auth/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || "Error al iniciar sesión");

      const { error } = await supabase.auth.setSession({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
      });
      if (error) throw error;
    } catch (e) {
      if (e instanceof Error) throw e;
      throw new Error("Error al iniciar sesión");
    }
  };

  const signUpWithEmail = async (
    name: string,
    email: string,
    password: string,
    acceptTerms: boolean
  ) => {
    if (!acceptTerms) throw new Error("Debes aceptar los términos de uso y la política de privacidad");
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: { full_name: name },
        emailRedirectTo: `${window.location.origin}/auth/callback?next=/onboarding`,
      },
    });
    if (error) throw error;
  };

  const signInWithMagicLink = async (email: string) => {
    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: { emailRedirectTo: `${window.location.origin}/auth/callback?next=/onboarding` },
    });
    if (error) throw error;
  };

  const signOut = async () => {
    // Primero limpiar cookies en el servidor para que el middleware no redirija a /chat
    await fetch("/api/auth/signout", { method: "POST", credentials: "include" });
    setServerAccessToken(null);
    setServerUser(null);
    setSession(null);
    setProfile(null);
    await supabase.auth.signOut();
  };

  const resetPassword = async (email: string) => {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/callback`,
    });
    if (error) throw error;
  };

  const isPremium = profile?.plan === "pro";
  const onboardingCompleted = profile?.onboarding_completed ?? false;

  return (
    <AuthContext.Provider
      value={{
        user: session?.user ?? serverUser,
        profile,
        session,
        loading,
        isPremium,
        onboardingCompleted,
        signInWithGoogle,
        signInWithEmail,
        signUpWithEmail,
        signInWithMagicLink,
        signOut,
        resetPassword,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (ctx === undefined) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
