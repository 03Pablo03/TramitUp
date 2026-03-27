"use client";

import Link from "next/link";
import { ClipboardList, Circle, CheckCircle } from "@/lib/icons";

interface Clausula {
  id: string;
  titulo: string;
  fragmento: string;
  riesgo: "alto" | "medio" | "bajo";
  problema: string;
  base_legal: string;
  accion: string;
}

interface ContractAnalysisData {
  tipo_contrato: string;
  resumen: string;
  clausulas: Clausula[];
  recomendacion_general: string;
}

const RISK_CONFIG = {
  alto: {
    label: "RIESGO ALTO",
    bg: "bg-red-50",
    border: "border-red-300",
    badge: "bg-red-100 text-red-700 border border-red-300",
    iconColor: "text-red-500",
    dot: "bg-red-500",
  },
  medio: {
    label: "REVISAR",
    bg: "bg-amber-50",
    border: "border-amber-300",
    badge: "bg-amber-100 text-amber-700 border border-amber-300",
    iconColor: "text-amber-500",
    dot: "bg-amber-500",
  },
  bajo: {
    label: "ATENCIÓN",
    bg: "bg-blue-50",
    border: "border-blue-200",
    badge: "bg-blue-100 text-blue-700 border border-blue-200",
    iconColor: "text-blue-500",
    dot: "bg-blue-400",
  },
};

const CONTRACT_LABELS: Record<string, string> = {
  alquiler: "Contrato de alquiler",
  laboral: "Contrato laboral",
  otro: "Contrato general",
  desconocido: "Contrato",
};

export function ContractAnalysisResult({ data }: { data: ContractAnalysisData }) {
  const tipoLabel = CONTRACT_LABELS[data.tipo_contrato] ?? "Contrato";
  const clausulasAlto = data.clausulas.filter((c) => c.riesgo === "alto");
  const clausulasMedio = data.clausulas.filter((c) => c.riesgo === "medio");
  const clausulasBajo = data.clausulas.filter((c) => c.riesgo === "bajo");

  const allClauses = [...clausulasAlto, ...clausulasMedio, ...clausulasBajo];

  return (
    <div className="space-y-6">
      {/* Cabecera */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-white">
            <ClipboardList className="h-6 w-6" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h2 className="text-lg font-semibold text-slate-900">{tipoLabel}</h2>
              <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600 capitalize">
                {data.tipo_contrato}
              </span>
            </div>
            <p className="mt-1 text-sm text-slate-600">{data.resumen}</p>
          </div>
        </div>

        {/* Resumen visual */}
        {data.clausulas.length > 0 && (
          <div className="mt-4 flex flex-wrap gap-3">
            {clausulasAlto.length > 0 && (
              <div className="flex items-center gap-1.5 rounded-lg bg-red-50 px-3 py-1.5 text-sm font-medium text-red-700">
                <span className="h-2 w-2 rounded-full bg-red-500" />
                {clausulasAlto.length} riesgo{clausulasAlto.length !== 1 ? "s" : ""} alto{clausulasAlto.length !== 1 ? "s" : ""}
              </div>
            )}
            {clausulasMedio.length > 0 && (
              <div className="flex items-center gap-1.5 rounded-lg bg-amber-50 px-3 py-1.5 text-sm font-medium text-amber-700">
                <span className="h-2 w-2 rounded-full bg-amber-500" />
                {clausulasMedio.length} a revisar
              </div>
            )}
            {clausulasBajo.length > 0 && (
              <div className="flex items-center gap-1.5 rounded-lg bg-blue-50 px-3 py-1.5 text-sm font-medium text-blue-700">
                <span className="h-2 w-2 rounded-full bg-blue-400" />
                {clausulasBajo.length} de atención
              </div>
            )}
            {data.clausulas.length === 0 && (
              <div className="flex items-center gap-1.5 rounded-lg bg-green-50 px-3 py-1.5 text-sm font-medium text-green-700">
                <span className="h-2 w-2 rounded-full bg-green-500" />
                Sin cláusulas problemáticas detectadas
              </div>
            )}
          </div>
        )}
      </div>

      {/* Sin problemas */}
      {data.clausulas.length === 0 && (
        <div className="rounded-2xl border border-green-200 bg-green-50 p-6 text-center">
          <CheckCircle className="h-10 w-10 text-green-500" />
          <p className="mt-2 font-semibold text-green-800">El contrato parece correcto</p>
          <p className="mt-1 text-sm text-green-700">{data.recomendacion_general}</p>
        </div>
      )}

      {/* Cláusulas */}
      {allClauses.map((clausula) => {
        const cfg = RISK_CONFIG[clausula.riesgo] ?? RISK_CONFIG.bajo;
        return (
          <div
            key={clausula.id}
            className={`rounded-2xl border ${cfg.border} ${cfg.bg} p-5 shadow-sm`}
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-start gap-2">
                <Circle className={`mt-0.5 h-4 w-4 fill-current ${cfg.iconColor}`} />
                <h3 className="font-semibold text-slate-900">{clausula.titulo}</h3>
              </div>
              <span className={`shrink-0 rounded-full px-2.5 py-0.5 text-xs font-bold ${cfg.badge}`}>
                {cfg.label}
              </span>
            </div>

            {/* Fragmento literal */}
            {clausula.fragmento && (
              <blockquote className="mt-3 rounded-lg border-l-4 border-slate-300 bg-white/60 px-4 py-2 text-sm italic text-slate-600">
                «{clausula.fragmento}»
              </blockquote>
            )}

            <div className="mt-3 space-y-2 text-sm">
              <div>
                <span className="font-medium text-slate-700">Problema: </span>
                <span className="text-slate-600">{clausula.problema}</span>
              </div>
              <div>
                <span className="font-medium text-slate-700">Base legal: </span>
                <span className="text-slate-600">{clausula.base_legal}</span>
              </div>
              <div className="rounded-lg bg-white/80 p-3">
                <span className="font-medium text-slate-700">Qué puedes hacer: </span>
                <span className="text-slate-700">{clausula.accion}</span>
              </div>
            </div>
          </div>
        );
      })}

      {/* Recomendación general */}
      {data.recomendacion_general && data.clausulas.length > 0 && (
        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-5">
          <p className="text-sm font-medium text-slate-700">Recomendación general</p>
          <p className="mt-1 text-sm text-slate-600">{data.recomendacion_general}</p>
        </div>
      )}

      {/* CTA */}
      <div className="rounded-2xl border border-blue-100 bg-blue-50 p-5 text-center">
        <p className="text-sm font-medium text-slate-700">
          ¿Quieres consultar sobre alguna cláusula específica?
        </p>
        <Link
          href="/chat"
          className="mt-3 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-5 py-2.5 text-sm font-bold text-white hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
        >
          Consultar con el asistente →
        </Link>
      </div>
    </div>
  );
}
