"use client";

import { useState } from "react";
import { Logo } from "@/components/Logo";
import { OnboardingProgress } from "@/components/auth/OnboardingProgress";
import { OnboardingStep1 } from "@/components/auth/OnboardingStep1";
import { OnboardingStep2 } from "@/components/auth/OnboardingStep2";
import { OnboardingStep3 } from "@/components/auth/OnboardingStep3";
import { OnboardingStep4 } from "@/components/auth/OnboardingStep4";

const SCENARIO_TO_VALUE: Record<string, string> = {
  despido: "Me han despedido",
  vuelo: "Vuelo cancelado/retrasado",
  alquiler: "Problema con alquiler/fianza",
  factura: "Factura incorrecta",
  multa: "Multa de tráfico",
  general: "Exploración general",
};

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [scenario, setScenario] = useState("");
  const [categories, setCategories] = useState<string[]>([]);
  const [situation, setSituation] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleScenario = (s: string) => {
    setScenario(s);
    // Auto-select relevant category based on scenario
    const scenarioCategories: Record<string, string[]> = {
      despido: ["laboral"],
      vuelo: ["reclamaciones"],
      alquiler: ["vivienda"],
      factura: ["reclamaciones"],
      multa: ["tramites"],
      general: [],
    };
    const suggested = scenarioCategories[s] || [];
    setCategories((prev) => Array.from(new Set([...prev, ...suggested])));
    setStep(2);
  };

  const handleSituation = (s: string) => {
    setSituation(s);
    setStep(4);
  };

  const handleComplete = async () => {
    setError(null);

    if (categories.length < 1) {
      setError("Por favor, selecciona al menos una área de interés.");
      return;
    }

    setLoading(true);

    try {
      const res = await fetch("/api/auth/complete-onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          categories_interest: categories,
          situation_type: situation || null,
          first_scenario: SCENARIO_TO_VALUE[scenario] || null,
        }),
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        setError(data.error || "No se pudo completar el registro. Inténtalo de nuevo.");
        setLoading(false);
        return;
      }

      window.location.href = "/chat";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error inesperado. Inténtalo de nuevo.");
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB] px-4 py-12">
      <div className="mx-auto max-w-2xl">
        <div className="mb-8 flex justify-center">
          <Logo height={40} />
        </div>
        <OnboardingProgress step={step} total={4} />
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          {step === 1 && (
            <OnboardingStep1 onNext={handleScenario} />
          )}
          {step === 2 && (
            <OnboardingStep2
              selected={categories}
              onSelect={setCategories}
              onNext={() => setStep(3)}
              onBack={() => setStep(1)}
            />
          )}
          {step === 3 && (
            <OnboardingStep4
              onNext={handleSituation}
              onBack={() => setStep(2)}
            />
          )}
          {step === 4 && (
            <OnboardingStep3
              onBack={() => setStep(3)}
              onComplete={handleComplete}
              loading={loading}
              error={error}
              onClearError={() => setError(null)}
            />
          )}
        </div>
        <p className="mt-8 text-center text-sm text-slate-500">
          Tramitup — Entiende tus derechos. Actúa con información.
        </p>
      </div>
    </div>
  );
}
