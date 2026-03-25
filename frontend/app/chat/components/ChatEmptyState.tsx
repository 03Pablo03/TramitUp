"use client";

import { FileCheck, Plane, Zap, Briefcase, Home } from "lucide-react";

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void;
}

const SUGGESTIONS = [
  {
    text: "Vuelo cancelado o retrasado",
    icon: Plane,
    bg: "bg-blue-100",
    border: "border-blue-200",
    iconColor: "text-blue-500",
  },
  {
    text: "Factura de luz o gas incorrecta",
    icon: Zap,
    bg: "bg-orange-100",
    border: "border-orange-200",
    iconColor: "text-orange-500",
  },
  {
    text: "Despido o finiquito incorrecto",
    icon: Briefcase,
    bg: "bg-red-100",
    border: "border-red-200",
    iconColor: "text-red-500",
  },
  {
    text: "Fianza del piso no devuelta",
    icon: Home,
    bg: "bg-green-100",
    border: "border-green-200",
    iconColor: "text-green-500",
  },
];

const CARD_DELAYS = [0, 75, 150, 225];

export default function ChatEmptyState({ onSuggestionClick }: ChatEmptyStateProps) {
  return (
    <div className="flex-1 flex items-center justify-center p-8 bg-[#FAFAF9]">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Icono principal con bounce-soft */}
        <div className="flex justify-center">
          <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center animate-bounce-soft">
            <FileCheck className="w-7 h-7 text-blue-600" strokeWidth={1.5} />
          </div>
        </div>

        {/* Título y descripción */}
        <div className="space-y-3">
          <h1 className="text-3xl font-fraunces font-semibold text-gray-900">
            Hola, soy TramitUp
          </h1>
          <p className="text-base text-gray-500 max-w-lg mx-auto leading-relaxed">
            Cuéntame tu situación y te ayudo paso a paso.
          </p>
        </div>

        {/* Suggestion cards — staggered fade-up */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SUGGESTIONS.map((s, index) => {
            const Icon = s.icon;
            return (
              <button
                key={index}
                onClick={() => onSuggestionClick(s.text)}
                className={`group flex items-center gap-3 p-4 ${s.bg} border ${s.border} rounded-2xl text-left transition-all duration-200 ease-out hover:scale-[1.02] hover:shadow-md focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 animate-fade-up`}
                style={{ animationDelay: `${CARD_DELAYS[index]}ms` }}
              >
                <Icon
                  className={`w-5 h-5 flex-shrink-0 ${s.iconColor}`}
                  strokeWidth={1.5}
                />
                <span className="text-sm font-medium text-gray-700">
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
