"use client";

const SITUATIONS = [
  { id: "empleado", label: "Empleado/a por cuenta ajena", icon: "👔" },
  { id: "autonomo", label: "Autónomo/a", icon: "💻" },
  { id: "desempleado", label: "Desempleado/a", icon: "📋" },
  { id: "inquilino", label: "Inquilino/a", icon: "🏠" },
  { id: "propietario", label: "Propietario/a", icon: "🏡" },
  { id: "estudiante", label: "Estudiante", icon: "📚" },
  { id: "jubilado", label: "Jubilado/a", icon: "🌅" },
  { id: "otro", label: "Otro / Prefiero no decirlo", icon: "🔒" },
];

type OnboardingStep4Props = {
  onNext: (situation: string) => void;
  onBack: () => void;
};

export function OnboardingStep4({ onNext, onBack }: OnboardingStep4Props) {
  return (
    <div className="mx-auto max-w-lg space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">¿Cuál es tu situación?</h1>
        <p className="mt-2 text-sm text-slate-500">
          Esto nos ayuda a darte información más relevante. Es opcional.
        </p>
      </div>
      <div className="grid grid-cols-2 gap-2">
        {SITUATIONS.map((s) => (
          <button
            key={s.id}
            onClick={() => onNext(s.id)}
            className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 text-left transition-all hover:border-[var(--primary)] hover:shadow-sm"
          >
            <span className="text-lg">{s.icon}</span>
            <span className="text-xs font-medium text-slate-700">{s.label}</span>
          </button>
        ))}
      </div>
      <div className="flex gap-3">
        <button
          onClick={onBack}
          className="rounded-xl border border-slate-300 px-6 py-3 font-medium text-slate-700 hover:bg-slate-50"
        >
          Atrás
        </button>
        <button
          onClick={() => onNext("otro")}
          className="flex-1 rounded-xl border border-slate-200 py-3 font-medium text-slate-500 hover:bg-slate-50"
        >
          Saltar este paso
        </button>
      </div>
    </div>
  );
}
