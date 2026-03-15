"use client";

import { useState } from "react";
import { Logo } from "@/components/Logo";
import { OnboardingProgress } from "@/components/auth/OnboardingProgress";
import { OnboardingStep1 } from "@/components/auth/OnboardingStep1";
import { OnboardingStep2 } from "@/components/auth/OnboardingStep2";
import { OnboardingStep3 } from "@/components/auth/OnboardingStep3";

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [categories, setCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const handleComplete = async () => {
    setError(null);
    
    // Validar que se hayan seleccionado al menos 2 categorías
    if (categories.length < 2) {
      setError("Por favor, selecciona al menos 2 áreas de interés para personalizar mejor tu experiencia.");
      return;
    }
    
    setLoading(true);

    try {
      const res = await fetch("/api/auth/complete-onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ categories_interest: categories }),
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
        <OnboardingProgress step={step} total={3} />
        <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
          {step === 1 && (
            <OnboardingStep1 onNext={() => setStep(2)} />
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
            <OnboardingStep3
              onBack={() => setStep(2)}
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
