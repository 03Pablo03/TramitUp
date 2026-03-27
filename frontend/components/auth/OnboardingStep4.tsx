"use client";

import { Briefcase, Monitor, ClipboardList, Home, GraduationCap, Sunset, Lock } from "@/lib/icons";

const SITUATIONS = [
  { id: "empleado", label: "Empleado/a por cuenta ajena", icon: Briefcase, iconColor: "text-blue-600", iconBg: "bg-blue-50" },
  { id: "autonomo", label: "Autónomo/a", icon: Monitor, iconColor: "text-indigo-600", iconBg: "bg-indigo-50" },
  { id: "desempleado", label: "Desempleado/a", icon: ClipboardList, iconColor: "text-amber-600", iconBg: "bg-amber-50" },
  { id: "inquilino", label: "Inquilino/a", icon: Home, iconColor: "text-emerald-600", iconBg: "bg-emerald-50" },
  { id: "propietario", label: "Propietario/a", icon: Home, iconColor: "text-teal-600", iconBg: "bg-teal-50" },
  { id: "estudiante", label: "Estudiante", icon: GraduationCap, iconColor: "text-purple-600", iconBg: "bg-purple-50" },
  { id: "jubilado", label: "Jubilado/a", icon: Sunset, iconColor: "text-orange-600", iconBg: "bg-orange-50" },
  { id: "otro", label: "Otro / Prefiero no decirlo", icon: Lock, iconColor: "text-slate-500", iconBg: "bg-slate-100" },
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
        {SITUATIONS.map((s) => {
          const Icon = s.icon;
          return (
            <button
              key={s.id}
              onClick={() => onNext(s.id)}
              className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 text-left transition-all hover:border-[var(--primary)] hover:shadow-sm"
            >
              <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${s.iconBg} shrink-0`}>
                <Icon className={`h-5 w-5 ${s.iconColor}`} />
              </div>
              <span className="text-xs font-medium text-slate-700">{s.label}</span>
            </button>
          );
        })}
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
