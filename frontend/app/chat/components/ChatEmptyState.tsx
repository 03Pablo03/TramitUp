"use client";

import { Scale, Plane, Receipt, Briefcase, Home, CheckCircle, Lock, FileText } from "lucide-react";

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void;
}

const SUGGESTIONS = [
  {
    text: "Vuelo cancelado o retrasado",
    icon: Plane,
    law: "Reglamento CE 261/2004",
  },
  {
    text: "Factura de luz o gas incorrecta",
    icon: Receipt,
    law: "Ley General de Consumidores",
  },
  {
    text: "Despido o finiquito incorrecto",
    icon: Briefcase,
    law: "Estatuto de los Trabajadores",
  },
  {
    text: "Fianza del piso no devuelta",
    icon: Home,
    law: "Ley de Arrendamientos Urbanos",
  },
];

const CARD_DELAYS = [0, 75, 150, 225];

export default function ChatEmptyState({ onSuggestionClick }: ChatEmptyStateProps) {
  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-white">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Main icon */}
        <div className="flex justify-center">
          <div className="w-14 h-14 bg-blue-50 rounded-full flex items-center justify-center animate-bounce-soft">
            <Scale className="w-7 h-7 text-blue-600" strokeWidth={1.5} />
          </div>
        </div>

        {/* Title and description */}
        <div className="space-y-2">
          <h1 className="text-3xl font-semibold text-slate-900 tracking-tight">
            Hola, soy TramitUp
          </h1>
          <p className="text-base text-slate-500 max-w-lg mx-auto leading-relaxed">
            Cuéntame tu situación y te ayudo paso a paso.
          </p>
          <div className="flex items-center justify-center gap-1.5 pt-0.5">
            <CheckCircle className="text-slate-400 flex-shrink-0" size={12} strokeWidth={1.5} />
            <span className="text-xs text-slate-400">
              Información basada en legislación española vigente · Actualizado 2026
            </span>
          </div>
        </div>

        {/* Suggestion cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SUGGESTIONS.map((s, index) => {
            const Icon = s.icon;
            return (
              <button
                key={index}
                onClick={() => onSuggestionClick(s.text)}
                className="group flex items-start gap-4 p-5 bg-white border border-slate-200 rounded-xl text-left transition-all duration-200 ease-out hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/10 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:ring-offset-2 animate-fade-up"
                style={{ animationDelay: `${CARD_DELAYS[index]}ms` }}
              >
                <Icon
                  className="w-5 h-5 flex-shrink-0 text-slate-400 group-hover:text-blue-600 transition-colors duration-200 mt-0.5"
                  strokeWidth={1.5}
                />
                <div className="min-w-0">
                  <span className="block text-sm font-medium text-slate-800">
                    {s.text}
                  </span>
                  <span className="block text-xs text-slate-400 mt-0.5">
                    {s.law}
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Trust bar */}
        <div className="flex items-center justify-center gap-6 pt-1">
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Lock size={12} strokeWidth={1.5} />
            <span>Datos protegidos</span>
          </div>
          <span className="text-slate-200">·</span>
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <FileText size={12} strokeWidth={1.5} />
            <span>Legislación vigente</span>
          </div>
          <span className="text-slate-200">·</span>
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Scale size={12} strokeWidth={1.5} />
            <span>+10.000 consultas resueltas</span>
          </div>
        </div>
      </div>
    </div>
  );
}
