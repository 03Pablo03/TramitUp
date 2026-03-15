"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { LoginForm } from "@/components/auth/LoginForm";
import { RegisterForm } from "@/components/auth/RegisterForm";
import { Logo } from "@/components/Logo";

type Tab = "login" | "register";

function LoginContent() {
  const [tab, setTab] = useState<Tab>("login");
  const [urlError, setUrlError] = useState<string | null>(null);
  const searchParams = useSearchParams();

  useEffect(() => {
    const err = searchParams.get("error");
    if (err) setUrlError(decodeURIComponent(err));
  }, [searchParams]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#F9FAFB] px-4 py-12">
      <div className="mb-8">
        <Logo height={44} />
      </div>
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          <div className="mb-6 flex rounded-xl border border-slate-200 p-1">
            <button
              type="button"
              onClick={() => setTab("login")}
              className={`flex-1 rounded-lg py-2 text-sm font-medium transition ${
                tab === "login"
                  ? "bg-[#1A56DB] text-white"
                  : "text-slate-600 hover:text-slate-800"
              }`}
            >
              Entrar
            </button>
            <button
              type="button"
              onClick={() => setTab("register")}
              className={`flex-1 rounded-lg py-2 text-sm font-medium transition ${
                tab === "register"
                  ? "bg-[#1A56DB] text-white"
                  : "text-slate-600 hover:text-slate-800"
              }`}
            >
              Crear cuenta
            </button>
          </div>

          <h1 className="mb-6 text-xl font-semibold text-slate-800">
            {tab === "login" ? "Iniciar sesión" : "Crear cuenta"}
          </h1>

          {urlError && (
            <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
              {urlError}
            </div>
          )}

          {tab === "login" ? (
            <LoginForm onSwitchToRegister={() => setTab("register")} />
          ) : (
            <RegisterForm onSwitchToLogin={() => setTab("login")} />
          )}
        </div>
        <Link
          href="/"
          className="mt-6 block text-center text-sm text-slate-500 hover:text-slate-700"
        >
          Volver al inicio
        </Link>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div>Cargando...</div>}>
      <LoginContent />
    </Suspense>
  );
}
