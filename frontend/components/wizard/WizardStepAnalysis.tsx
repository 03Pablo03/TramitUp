"use client";

import { useEffect, useState } from "react";
import { Search, AlertTriangle } from "@/lib/icons";

interface WizardStepAnalysisProps {
  analysis: string | null;
  loading: boolean;
  onContinue: () => void;
}

export function WizardStepAnalysis({ analysis, loading, onContinue }: WizardStepAnalysisProps) {
  const [dots, setDots] = useState("");

  useEffect(() => {
    if (!loading) return;
    const interval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "" : prev + "."));
    }, 500);
    return () => clearInterval(interval);
  }, [loading]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-500 shadow-lg shadow-blue-500/20">
          <svg className="h-8 w-8 animate-spin text-white" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-slate-800">Analizando tu caso{dots}</h3>
        <p className="mt-2 text-sm text-slate-500">
          Estamos revisando la normativa aplicable y calculando los importes correspondientes.
        </p>
        <div className="mt-6 flex gap-2">
          {["Recopilando datos", "Consultando normativa", "Calculando importes"].map((step, i) => (
            <span key={step} className="rounded-full bg-blue-50 px-3 py-1 text-xs font-medium text-blue-600 animate-pulse" style={{ animationDelay: `${i * 0.3}s` }}>
              {step}
            </span>
          ))}
        </div>
      </div>
    );
  }

  if (!analysis) return null;

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-blue-100 bg-blue-50/50 p-1">
        <div className="flex items-center gap-2 px-4 py-2">
          <Search className="h-5 w-5 text-blue-600" />
          <span className="text-sm font-semibold text-blue-800">Análisis de tu caso</span>
        </div>
      </div>

      <div className="prose prose-sm prose-slate max-w-none rounded-xl border border-slate-200 bg-white p-6">
        {analysis.split("\n").map((line, i) => {
          if (line.startsWith("**") && line.endsWith("**")) {
            return <h4 key={i} className="mt-4 first:mt-0 font-semibold text-slate-800">{line.replace(/\*\*/g, "")}</h4>;
          }
          if (line.startsWith("- ") || line.startsWith("• ")) {
            return <li key={i} className="ml-4 text-slate-600">{line.slice(2)}</li>;
          }
          if (line.trim()) {
            return <p key={i} className="text-slate-600">{line}</p>;
          }
          return null;
        })}
      </div>

      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
        <div className="flex gap-3">
          <AlertTriangle className="h-5 w-5 shrink-0 text-amber-500" />
          <p className="text-xs text-amber-700">
            Este análisis es orientativo y no sustituye el asesoramiento de un profesional del derecho.
            Los importes y plazos son estimaciones basadas en la normativa vigente.
          </p>
        </div>
      </div>

      <button
        onClick={onContinue}
        className="w-full rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
      >
        Continuar — Generar documento
      </button>
    </div>
  );
}
