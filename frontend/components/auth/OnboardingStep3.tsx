"use client";

import Link from "next/link";

type OnboardingStep3Props = {
  onBack: () => void;
  onComplete: () => void;
  loading?: boolean;
  error?: string | null;
  onClearError?: () => void;
};

export function OnboardingStep3({ onBack, onComplete, loading, error, onClearError }: OnboardingStep3Props) {
  return (
    <div className="mx-auto max-w-lg space-y-6">
      <h1 className="text-2xl font-bold text-slate-800">Tu plan gratuito incluye</h1>
      <ul className="space-y-3">
        {[
          { text: "2 consultas al día", included: true },
          { text: "Información basada en normativa real", included: true },
          { text: "Acceso a todos los temas", included: true },
          { text: "Generación de modelos de escritos", included: false },
          { text: "Alertas de plazos", included: false },
          { text: "Consultas ilimitadas", included: false },
        ].map((item) => (
          <li
            key={item.text}
            className={`flex items-center gap-2 ${
              item.included ? "text-slate-700" : "text-slate-400"
            }`}
          >
            <span className="text-xl">{item.included ? "✓" : "✗"}</span>
            <span>{item.text}</span>
          </li>
        ))}
      </ul>
      <p className="text-slate-600">
        Con PRO (€9,99/mes) tienes todo sin límites.
      </p>
      {error && (
        <div
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
        >
          {error}
          {onClearError && (
            <button
              type="button"
              onClick={onClearError}
              className="ml-2 underline"
              aria-label="Cerrar error"
            >
              Cerrar
            </button>
          )}
        </div>
      )}
      <div className="flex gap-3">
        <button
          type="button"
          onClick={onBack}
          disabled={loading}
          className="rounded-xl border border-slate-300 px-6 py-3 font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
        >
          Atrás
        </button>
        <button
          type="button"
          onClick={() => onComplete()}
          disabled={loading}
          className="flex-1 rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8] disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {loading ? "Guardando..." : "Empezar gratis →"}
        </button>
      </div>
      <Link
        href="/pricing"
        className="block text-center text-sm text-[#1A56DB] hover:underline"
      >
        Ver plan PRO
      </Link>
    </div>
  );
}
