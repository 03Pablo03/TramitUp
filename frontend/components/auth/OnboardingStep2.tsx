"use client";

import { useState } from "react";

const CATEGORIES = [
  { id: "reclamaciones", label: "Reclamaciones (vuelos, bancos, facturas...)", icon: "✈️" },
  { id: "laboral", label: "Laboral (despido, paro, nómina...)", icon: "💼" },
  { id: "vivienda", label: "Vivienda (alquiler, hipoteca, comunidad...)", icon: "🏠" },
  { id: "tramites", label: "Trámites (Hacienda, Seguridad Social, multas...)", icon: "🏛️" },
];

type OnboardingStep2Props = {
  selected: string[];
  onSelect: (ids: string[]) => void;
  onNext: () => void;
  onBack: () => void;
};

export function OnboardingStep2({
  selected,
  onSelect,
  onNext,
  onBack,
}: OnboardingStep2Props) {
  const toggle = (id: string) => {
    if (selected.includes(id)) {
      onSelect(selected.filter((s) => s !== id));
    } else {
      onSelect([...selected, id]);
    }
  };

  return (
    <div className="mx-auto max-w-lg space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">¿Para qué lo usarás?</h1>
        <p className="mt-2 text-slate-600">
          Selecciona al menos una categoría para personalizar tu experiencia
        </p>
      </div>
      <div className="space-y-3">
        {CATEGORIES.map((c) => (
          <label
            key={c.id}
            className="flex cursor-pointer items-center gap-3 rounded-xl border border-slate-200 p-4 transition hover:border-[#1A56DB]/50"
          >
            <input
              type="checkbox"
              checked={selected.includes(c.id)}
              onChange={() => toggle(c.id)}
              className="h-4 w-4 rounded border-slate-300"
            />
            <span className="text-xl">{c.icon}</span>
            <span className="text-slate-700">{c.label}</span>
          </label>
        ))}
      </div>
      {selected.length < 1 && (
        <p className="text-sm text-amber-600">Selecciona al menos una categoría</p>
      )}
      <div className="flex gap-3">
        <button
          onClick={onBack}
          className="rounded-xl border border-slate-300 px-6 py-3 font-medium text-slate-700 hover:bg-slate-50"
        >
          Atrás
        </button>
        <button
          onClick={onNext}
          disabled={selected.length < 1}
          className="flex-1 rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8] disabled:opacity-50"
        >
          Continuar
        </button>
      </div>
    </div>
  );
}
