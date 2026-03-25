"use client";

const SCENARIOS = [
  { id: "despido", label: "Me han despedido o voy a dejar mi trabajo", icon: "💼", accent: "border-slate-200 hover:border-blue-400" },
  { id: "vuelo", label: "Me han cancelado o retrasado un vuelo", icon: "✈️", accent: "border-slate-200 hover:border-cyan-400" },
  { id: "alquiler", label: "Tengo un problema con mi alquiler o fianza", icon: "🏠", accent: "border-slate-200 hover:border-emerald-400" },
  { id: "factura", label: "Quiero reclamar una factura o cobro incorrecto", icon: "💡", accent: "border-slate-200 hover:border-amber-400" },
  { id: "multa", label: "Quiero recurrir una multa de tráfico", icon: "🚗", accent: "border-slate-200 hover:border-red-400" },
  { id: "general", label: "Otra cosa / Solo quiero explorar", icon: "🔍", accent: "border-slate-200 hover:border-violet-400" },
];

type OnboardingStep1Props = {
  onNext: (scenario: string) => void;
};

export function OnboardingStep1({ onNext }: OnboardingStep1Props) {
  return (
    <div className="mx-auto max-w-lg space-y-6">
      <div className="text-center">
        <div className="inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-2xl shadow-lg shadow-blue-500/20 mb-4">
          👋
        </div>
        <h1 className="text-2xl font-bold text-slate-800">¿Qué te trae por aquí?</h1>
        <p className="mt-2 text-sm text-slate-500">
          Así personalizamos tu experiencia desde el primer momento
        </p>
      </div>
      <div className="space-y-2">
        {SCENARIOS.map((s) => (
          <button
            key={s.id}
            onClick={() => onNext(s.id)}
            className={`flex w-full items-center gap-4 rounded-xl border bg-white p-4 text-left transition-all hover:shadow-md ${s.accent}`}
          >
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-50 text-xl shrink-0">
              {s.icon}
            </span>
            <span className="text-sm font-medium text-slate-700">{s.label}</span>
            <svg className="ml-auto h-4 w-4 text-slate-300 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
            </svg>
          </button>
        ))}
      </div>
    </div>
  );
}
