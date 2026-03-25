"use client";

import { FileCheck, Plane, Zap, Briefcase, Home, AlertTriangle, Building2 } from "lucide-react";

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void;
}

const SUGGESTIONS = [
  {
    text: "Vuelo cancelado o retrasado",
    icon: Plane,
    bg: "bg-blue-50",
    border: "border-blue-100",
    iconColor: "text-blue-500",
  },
  {
    text: "Factura de luz o gas incorrecta",
    icon: Zap,
    bg: "bg-orange-50",
    border: "border-orange-100",
    iconColor: "text-orange-500",
  },
  {
    text: "Despido o finiquito incorrecto",
    icon: Briefcase,
    bg: "bg-red-50",
    border: "border-red-100",
    iconColor: "text-red-500",
  },
  {
    text: "Fianza del piso no devuelta",
    icon: Home,
    bg: "bg-green-50",
    border: "border-green-100",
    iconColor: "text-green-500",
  },
];

const FEATURES = [
  {
    icon: "📋",
    title: "Información normativa",
    desc: "Qué dice la ley en tu caso concreto",
  },
  {
    icon: "📄",
    title: "Modelo de escrito",
    desc: "PDF y Word listos para presentar",
  },
  {
    icon: "⏰",
    title: "Alerta de plazo",
    desc: "Te avisamos antes de que venza",
  },
];

const POPULAR_CHIPS = [
  "Baja médica y trabajo",
  "Reclamar vuelo cancelado",
  "Contrato de alquiler",
  "Accidente de tráfico",
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
        <div className="space-y-4">
          <h1 className="text-3xl font-fraunces font-semibold text-gray-900">
            Hola, soy TramitUp
          </h1>
          <p className="text-base text-gray-500 max-w-lg mx-auto leading-relaxed">
            Cuéntamelo y te explico qué dice la normativa, qué opciones tienes y genero
            el modelo de escrito si lo necesitas.
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

        {/* Lo que otros consultan */}
        <div className="space-y-3">
          <div className="flex items-center justify-center">
            <div className="flex-1 h-px bg-gray-200"></div>
            <span className="px-4 text-sm font-medium text-gray-400">Lo que otros consultan</span>
            <div className="flex-1 h-px bg-gray-200"></div>
          </div>
          <div className="flex flex-wrap justify-center gap-2">
            {POPULAR_CHIPS.map((chip) => (
              <button
                key={chip}
                onClick={() => onSuggestionClick(chip)}
                className="rounded-full border border-slate-200 bg-white px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 transition-colors duration-200 ease-out"
              >
                {chip}
              </button>
            ))}
          </div>
        </div>

        {/* Lo que puedes obtener */}
        <div className="space-y-6">
          <div className="flex items-center justify-center">
            <div className="flex-1 h-px bg-gray-200"></div>
            <span className="px-4 text-sm font-medium text-gray-400">Lo que puedes obtener</span>
            <div className="flex-1 h-px bg-gray-200"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {FEATURES.map((feature, index) => (
              <div
                key={index}
                className="bg-white border border-gray-200 rounded-2xl p-4 text-center space-y-2 shadow-sm animate-fade-up"
                style={{ animationDelay: `${(index + 4) * 75}ms` }}
              >
                <div className="text-2xl">{feature.icon}</div>
                <h3 className="font-medium text-gray-900 text-sm">{feature.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
