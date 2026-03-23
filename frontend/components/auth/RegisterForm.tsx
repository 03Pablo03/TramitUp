"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

type RegisterFormProps = {
  onSwitchToLogin: () => void;
};

export function RegisterForm({ onSwitchToLogin }: RegisterFormProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [error, setError] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const { signUpWithEmail } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirect") || "/chat";

  const handleGoogleSignUp = async () => {
    setError({});
    setLoading(true);
    try {
      const callbackUrl = `${window.location.origin}/auth/callback?next=${encodeURIComponent(redirectTo)}`;
      const { createClient } = await import("@/lib/supabase/client");
      const supabase = createClient();
      const { error: oauthError } = await supabase.auth.signInWithOAuth({
        provider: "google",
        options: { redirectTo: callbackUrl },
      });
      if (oauthError) throw oauthError;
    } catch (err) {
      setError({ form: err instanceof Error ? err.message : "Error al registrarse" });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError({});
    if (!acceptTerms) {
      setError({ terms: "Debes aceptar los términos y la política de privacidad" });
      return;
    }
    if (password.length < 8) {
      setError({ password: "La contraseña debe tener al menos 8 caracteres" });
      return;
    }
    setLoading(true);
    try {
      await signUpWithEmail(name, email, password, acceptTerms);
      setError({
        form: "Revisa tu email para confirmar la cuenta. Luego podrás iniciar sesión.",
      });
    } catch (err) {
      setError({
        form: err instanceof Error ? err.message : "Error al crear la cuenta",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <button
        type="button"
        onClick={handleGoogleSignUp}
        disabled={loading}
        className="flex w-full items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white py-3 font-medium text-slate-700 shadow-sm hover:bg-slate-50 disabled:opacity-50"
      >
        <svg className="h-5 w-5" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
        </svg>
        Registrarse con Google
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
          <label className="mb-1 block text-sm font-medium text-slate-600">Nombre</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
            placeholder="Tu nombre"
          />
        </div>
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
        </div>
        <div>
          <label className="mb-1 block text-sm font-medium text-slate-600">Contraseña (mín. 8 caracteres)</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
          />
          {error.password && <p className="mt-1 text-sm text-red-600">{error.password}</p>}
        </div>
        <label className="flex items-start gap-2">
          <input
            type="checkbox"
            checked={acceptTerms}
            onChange={(e) => setAcceptTerms(e.target.checked)}
            className="mt-1 rounded border-slate-300"
          />
          <span className="text-sm text-slate-600">
            Acepto los{" "}
            <a href="/terms" className="text-[#1A56DB] hover:underline">
              términos de uso
            </a>{" "}
            y la{" "}
            <a href="/privacy" className="text-[#1A56DB] hover:underline">
              política de privacidad
            </a>
          </span>
        </label>
        {error.terms && <p className="text-sm text-red-600">{error.terms}</p>}
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8] disabled:opacity-50"
        >
          {loading ? "Creando cuenta..." : "Crear cuenta gratis"}
        </button>
        {error.form && <p className="text-center text-sm text-red-600">{error.form}</p>}
      </form>

      <p className="text-center text-sm text-slate-600">
        ¿Ya tienes cuenta?{" "}
        <button
          type="button"
          onClick={onSwitchToLogin}
          className="font-medium text-[#1A56DB] hover:underline"
        >
          Entra aquí
        </button>
      </p>
    </div>
  );
}
