"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

type LoginFormProps = {
  onSwitchToRegister: () => void;
};

export function LoginForm({ onSwitchToRegister }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [connectionOk, setConnectionOk] = useState<boolean | null>(null);
  const { signInWithGoogle, signInWithEmail, signInWithMagicLink } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirect") || "/chat";

  // Verificar conectividad con Supabase al montar
  useEffect(() => {
    const check = async () => {
      const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
      const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
      if (!url || !key) {
        setConnectionOk(false);
        return;
      }
      try {
        const res = await fetch(`${url.replace(/\/$/, "")}/auth/v1/health`, {
          method: "GET",
          headers: { apikey: key },
        });
        setConnectionOk(res.ok);
      } catch {
        setConnectionOk(false);
      }
    };
    check();
  }, []);

  const handleGoogleSignIn = async () => {
    setError({});
    setLoading(true);
    try {
      // Pass redirect as `next` param to the OAuth callback
      const callbackUrl = `${window.location.origin}/auth/callback?next=${encodeURIComponent(redirectTo)}`;
      const { createClient } = await import("@/lib/supabase/client");
      const supabase = createClient();
      const { error: oauthError } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo: callbackUrl },
      });
      if (oauthError) throw oauthError;
    } catch (err) {
      setError({ form: err instanceof Error ? err.message : "Error al iniciar sesión" });
      if (process.env.NODE_ENV === "development") console.error("[Login Google]", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError({});
    if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
      setError({ form: "Configura NEXT_PUBLIC_SUPABASE_URL y NEXT_PUBLIC_SUPABASE_ANON_KEY en .env.local" });
      return;
    }
    setLoading(true);
    try {
      const timeoutMs = 15000;
      await Promise.race([
        signInWithEmail(email, password),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("La conexión tardó demasiado. Comprueba tu internet o que el proyecto Supabase esté activo.")), timeoutMs)
        ),
      ]);
      router.push(redirectTo);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Error al iniciar sesión";
      setError({ password: msg });
      if (process.env.NODE_ENV === "development") console.error("[Login]", err);
    } finally {
      setLoading(false);
    }
  };

  const handleMagicLink = async (e: React.MouseEvent) => {
    e.preventDefault();
    if (!email.trim()) {
      setError({ email: "Introduce tu email" });
      return;
    }
    setError({});
    setLoading(true);
    try {
      await signInWithMagicLink(email);
      setError({ form: "Revisa tu email. Te hemos enviado un enlace para entrar." });
    } catch (err) {
      setError({ email: err instanceof Error ? err.message : "Error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={handleGoogleSignIn}
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white py-3 font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:opacity-50"
      >
        <svg className="h-5 w-5" viewBox="0 0 24 24">
          <path
            fill="#4285F4"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="#34A853"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="#FBBC05"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          />
          <path
            fill="#EA4335"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          />
        </svg>
        Continuar con Google
      </button>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-slate-200" />
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="bg-white px-2 text-slate-500">o</span>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-600">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
            placeholder="tu@email.com"
          />
          {error.email && <p className="mt-1 text-sm text-red-600">{error.email}</p>}
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-600">Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
          />
          {error.password && <p className="mt-1 text-sm text-red-600">{error.password}</p>}
        </div>
        <div className="flex items-center justify-between">
          <Link
            href="/login/forgot"
            className="text-sm text-[#1A56DB] hover:underline"
          >
            ¿Olvidaste tu contraseña?
          </Link>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8] disabled:opacity-50"
        >
          {loading ? "Entrando..." : "Entrar"}
        </button>
        {connectionOk === false && (
          <p className="rounded-lg bg-amber-50 p-3 text-center text-sm text-amber-800">
            No se pudo conectar con Supabase. Verifica .env.local y reinicia el servidor (npm run dev).
          </p>
        )}
        {error.form && (
          <p className="text-center text-sm text-red-600">{error.form}</p>
        )}
      </form>

      <p className="text-center text-sm text-slate-600">
        <button
          type="button"
          onClick={handleMagicLink}
          disabled={loading}
          className="text-[#1A56DB] hover:underline disabled:opacity-50"
        >
          Enviar enlace mágico al email
        </button>
      </p>

      <p className="text-center text-sm text-slate-600">
        ¿No tienes cuenta?{" "}
        <button
          type="button"
          onClick={onSwitchToRegister}
          className="font-medium text-[#1A56DB] hover:underline"
        >
          Créala gratis
        </button>
      </p>
    </div>
  );
}
