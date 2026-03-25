"use client";

import { FileCheck, Plane, Receipt, Briefcase, Home } from "lucide-react";

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void;
}

const SUGGESTIONS = [
  {
    text: "Vuelo cancelado o retrasado",
    icon: Plane,
  },
  {
    text: "Factura de luz o gas incorrecta",
    icon: Receipt,
  },
  {
    text: "Despido o finiquito incorrecto",
    icon: Briefcase,
  },
  {
    text: "Fianza del piso no devuelta",
    icon: Home,
  },
];

const CARD_DELAYS = [0, 75, 150, 225];

export default function ChatEmptyState({ onSuggestionClick }: ChatEmptyStateProps) {
  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-white">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Icono principal */}
        <div className="flex justify-center">
          <div className="w-14 h-14 bg-slate-100 rounded-full flex items-center justify-center animate-bounce-soft">
            <FileCheck className="w-7 h-7 text-slate-600" strokeWidth={1.5} />
          </div>
        </div>

        {/* Título y descripción */}
        <div className="space-y-3">
          <h1 className="text-3xl font-semibold text-slate-900 tracking-tight">
            Hola, soy TramitUp
          </h1>
          <p className="text-base text-slate-500 max-w-lg mx-auto leading-relaxed">
            Cuéntame tu situación y te ayudo paso a paso.
          </p>
        </div>

        {/* Suggestion cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SUGGESTIONS.map((s, index) => {
            const Icon = s.icon;
            return (
              <button
                key={index}
                onClick={() => onSuggestionClick(s.text)}
                className="group flex items-center gap-4 p-5 bg-white border border-slate-200 rounded-xl text-left transition-all duration-200 ease-out hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/10 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:ring-offset-2 animate-fade-up"
                style={{ animationDelay: `${CARD_DELAYS[index]}ms` }}
              >
                <Icon
                  className="w-5 h-5 flex-shrink-0 text-slate-500 group-hover:text-blue-600 transition-colors duration-200"
                  strokeWidth={1.5}
                />
                <span className="text-sm font-medium text-slate-800">
                  {s.text}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
