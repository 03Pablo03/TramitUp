"use client";

import { FileCheck } from "lucide-react";

interface ChatEmptyStateProps {
  onSuggestionClick: (suggestion: string) => void;
}

const SUGGESTIONS = [
  { emoji: "✈️", text: "Vuelo cancelado o retrasado" },
  { emoji: "💡", text: "Factura de luz o gas incorrecta" },
  { emoji: "💼", text: "Despido o finiquito incorrecto" },
  { emoji: "🏠", text: "Fianza del piso no devuelta" },
  { emoji: "🚗", text: "Multa de tráfico injusta" },
  { emoji: "🏛️", text: "Problema con Hacienda o AEAT" },
];

const FEATURES = [
  {
    icon: "📋",
    title: "Información normativa",
    desc: "Qué dice la ley en tu caso concreto"
  },
  {
    icon: "📄",
    title: "Modelo de escrito",
    desc: "PDF y Word listos para presentar"
  },
  {
    icon: "⏰",
    title: "Alerta de plazo",
    desc: "Te avisamos antes de que venza"
  }
];

export default function ChatEmptyState({ onSuggestionClick }: ChatEmptyStateProps) {
  return (
    <div className="flex-1 flex items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center space-y-8">
        {/* Icono principal */}
        <div className="flex justify-center">
          <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
            <FileCheck className="w-6 h-6 text-blue-600" />
          </div>
        </div>

        {/* Título y descripción */}
        <div className="space-y-4">
          <h1 className="text-3xl font-fraunces font-semibold text-gray-900">
            ¿Cuál es tu situación?
          </h1>
          <p className="text-base text-gray-500 max-w-lg mx-auto leading-relaxed">
            Cuéntamelo y te explico qué dice la normativa, qué opciones tienes y genero 
            el modelo de escrito si lo necesitas.
          </p>
        </div>

        {/* Casos frecuentes */}
        <div className="space-y-6">
          <div className="flex items-center justify-center">
            <div className="flex-1 h-px bg-gray-200"></div>
            <span className="px-4 text-sm font-medium text-gray-400">Casos frecuentes</span>
            <div className="flex-1 h-px bg-gray-200"></div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {SUGGESTIONS.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => onSuggestionClick(suggestion.text)}
                className="group flex items-center gap-3 p-4 bg-white border border-gray-200 rounded-2xl text-left transition-all duration-150 hover:border-blue-500 hover:bg-blue-50 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                style={{
                  animationDelay: `${index * 50}ms`,
                  animation: 'fadeInUp 0.3s ease-out forwards',
                  opacity: 0,
                  transform: 'translateY(8px)'
                }}
              >
                <span className="text-lg flex-shrink-0">{suggestion.emoji}</span>
                <span className="text-sm font-medium text-gray-700 group-hover:text-blue-600">
                  {suggestion.text}
                </span>
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
                className="bg-white border border-gray-200 rounded-xl p-4 text-center space-y-2 shadow-sm"
                style={{
                  animationDelay: `${(index + 6) * 50}ms`,
                  animation: 'fadeInUp 0.3s ease-out forwards',
                  opacity: 0,
                  transform: 'translateY(8px)'
                }}
              >
                <div className="text-2xl">{feature.icon}</div>
                <h3 className="font-medium text-gray-900 text-sm">{feature.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
}