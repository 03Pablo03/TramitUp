"use client";

import { useState } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const { resetPassword } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);
    setLoading(true);
    try {
      await resetPassword(email);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al enviar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#F9FAFB] px-4">
      <div className="w-full max-w-sm rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <h1 className="mb-2 text-xl font-semibold text-slate-800">
          Recuperar contraseña
        </h1>
        <p className="mb-6 text-sm text-slate-600">
          Introduce tu email y te enviaremos un enlace para restablecer tu contraseña.
        </p>
        {success ? (
          <div className="space-y-4">
            <p className="rounded-lg bg-emerald-50 p-4 text-sm text-emerald-800">
              Revisa tu email. Te hemos enviado un enlace para restablecer tu contraseña.
            </p>
            <Link
              href="/login"
              className="block text-center text-sm text-[#1A56DB] hover:underline"
            >
              Volver a iniciar sesión
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="mb-1 block text-sm font-medium text-slate-600">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full rounded-xl border border-slate-300 px-4 py-2.5 focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
              />
              {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8] disabled:opacity-50"
            >
              {loading ? "Enviando..." : "Enviar enlace"}
            </button>
          </form>
        )}
        <Link
          href="/login"
          className="mt-6 block text-center text-sm text-slate-500 hover:text-slate-700"
        >
          Volver al login
        </Link>
      </div>
    </div>
  );
}
