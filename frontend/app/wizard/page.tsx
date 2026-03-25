"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ToolHeader } from "@/components/ToolHeader";
import { apiFetch } from "@/lib/api";

type Template = {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: string;
  estimated_time: string;
};

const CATEGORY_COLORS: Record<string, string> = {
  consumo: "bg-amber-50 text-amber-700 border-amber-200",
  laboral: "bg-blue-50 text-blue-700 border-blue-200",
  vivienda: "bg-emerald-50 text-emerald-700 border-emerald-200",
  trafico: "bg-red-50 text-red-700 border-red-200",
  fiscal: "bg-purple-50 text-purple-700 border-purple-200",
};

const CATEGORY_LABELS: Record<string, string> = {
  consumo: "Consumo",
  laboral: "Laboral",
  vivienda: "Vivienda",
  trafico: "Tráfico",
  fiscal: "Fiscal",
};

export default function WizardGalleryPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string | null>(null);

  useEffect(() => {
    apiFetch("/wizard/templates")
      .then((r) => r.json())
      .then((d) => setTemplates(d.data || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const categories = [...new Set(templates.map((t) => t.category))];
  const filtered = filter ? templates.filter((t) => t.category === filter) : templates;

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <ToolHeader title="Trámites guiados" />
      <div className="mx-auto max-w-3xl px-4 py-8">
        {/* Hero */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-3xl shadow-lg shadow-blue-500/20">
            📋
          </div>
          <h1 className="text-2xl font-bold text-slate-800">
            ¿Qué trámite necesitas gestionar?
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Te guiamos paso a paso. Recopilamos datos, analizamos tu caso, generamos documentos y te decimos exactamente qué hacer.
          </p>
        </div>

        {/* Category filters */}
        {categories.length > 1 && (
          <div className="mb-6 flex flex-wrap justify-center gap-2">
            <button
              onClick={() => setFilter(null)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-all ${
                !filter
                  ? "bg-slate-800 text-white shadow-sm"
                  : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
              }`}
            >
              Todos
            </button>
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setFilter(cat === filter ? null : cat)}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-all ${
                  filter === cat
                    ? "bg-slate-800 text-white shadow-sm"
                    : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
                }`}
              >
                {CATEGORY_LABELS[cat] || cat}
              </button>
            ))}
          </div>
        )}

        {/* Templates grid */}
        {loading ? (
          <div className="grid gap-4 sm:grid-cols-2">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="animate-pulse rounded-2xl border border-slate-200 bg-white p-6">
                <div className="mb-3 h-10 w-10 rounded-xl bg-slate-100" />
                <div className="mb-2 h-5 w-3/4 rounded bg-slate-100" />
                <div className="h-4 w-full rounded bg-slate-50" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {filtered.map((t) => (
              <Link
                key={t.id}
                href={`/wizard/${t.id}`}
                className="group rounded-2xl border border-slate-200 bg-white p-6 transition-all hover:border-[var(--primary)] hover:shadow-lg hover:shadow-blue-500/5"
              >
                <div className="mb-3 flex items-start justify-between">
                  <span className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-50 text-2xl group-hover:bg-blue-50 transition-colors">
                    {t.icon}
                  </span>
                  <span
                    className={`rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                      CATEGORY_COLORS[t.category] || "bg-slate-50 text-slate-600 border-slate-200"
                    }`}
                  >
                    {CATEGORY_LABELS[t.category] || t.category}
                  </span>
                </div>
                <h3 className="mb-1 font-semibold text-slate-800 group-hover:text-[var(--primary)] transition-colors">
                  {t.title}
                </h3>
                <p className="mb-3 text-sm text-slate-500 line-clamp-2">{t.description}</p>
                <div className="flex items-center gap-1.5 text-xs text-slate-400">
                  <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {t.estimated_time}
                </div>
              </Link>
            ))}
          </div>
        )}

        {!loading && filtered.length === 0 && (
          <div className="rounded-2xl border border-dashed border-slate-300 p-12 text-center">
            <p className="text-slate-500">No hay trámites disponibles en esta categoría.</p>
          </div>
        )}

        {/* CTA */}
        <div className="mt-8 rounded-2xl border border-slate-200 bg-gradient-to-r from-slate-50 to-blue-50/30 p-6 text-center">
          <p className="text-sm text-slate-600">
            ¿No encuentras tu trámite?{" "}
            <Link href="/chat" className="font-semibold text-[var(--primary)] hover:underline">
              Consulta al asistente
            </Link>{" "}
            y te ayudará con cualquier gestión legal.
          </p>
        </div>
      </div>
    </div>
  );
}
