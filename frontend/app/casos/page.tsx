"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { CaseCard, CaseData } from "@/components/CaseCard";

const CATEGORIES = [
  { value: "laboral", label: "💼 Laboral" },
  { value: "vivienda", label: "🏠 Vivienda" },
  { value: "consumo", label: "🛒 Consumo" },
  { value: "familia", label: "👨‍👩‍👧 Familia" },
  { value: "trafico", label: "🚗 Tráfico" },
  { value: "administrativo", label: "🏛️ Administrativo" },
  { value: "fiscal", label: "💰 Fiscal" },
  { value: "penal", label: "⚖️ Penal" },
  { value: "otro", label: "📋 Otro" },
];

export default function CasosPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [cases, setCases] = useState<CaseData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // New case form
  const [showForm, setShowForm] = useState(false);
  const [formTitle, setFormTitle] = useState("");
  const [formCategory, setFormCategory] = useState("");
  const [formSummary, setFormSummary] = useState("");
  const [creating, setCreating] = useState(false);
  const [createError, setCreateError] = useState("");

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || authLoading) return;
    apiFetch("/cases")
      .then((r) => r.json())
      .then((data) => setCases(data.cases || []))
      .catch(() => setError("No se pudieron cargar los expedientes."))
      .finally(() => setLoading(false));
  }, [user?.id, authLoading]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formTitle.trim()) return;
    setCreating(true);
    setCreateError("");

    try {
      const res = await apiFetch("/cases", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: formTitle.trim(),
          category: formCategory || null,
          summary: formSummary.trim() || null,
        }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const msg = body.detail || `Error ${res.status}`;
        if (res.status === 403) {
          setCreateError(msg);
        } else {
          setCreateError(msg);
        }
        return;
      }

      const newCase: CaseData = await res.json();
      setCases((prev) => [newCase, ...prev]);
      setShowForm(false);
      setFormTitle("");
      setFormCategory("");
      setFormSummary("");
    } catch {
      setCreateError("Error de conexión. Inténtalo de nuevo.");
    } finally {
      setCreating(false);
    }
  };

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-slate-500">Cargando...</div>
      </div>
    );
  }

  const openCases = cases.filter((c) => c.status === "open");
  const otherCases = cases.filter((c) => c.status !== "open");

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-3xl items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push("/chat")}
              className="text-sm text-slate-500 hover:text-slate-800"
            >
              ← Chat
            </button>
            <span className="text-slate-300">|</span>
            <h1 className="text-lg font-bold text-slate-900">Mis expedientes</h1>
          </div>
          <button
            onClick={() => { setShowForm(true); setCreateError(""); }}
            className="rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
          >
            + Nuevo expediente
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8">

        {/* Create form */}
        {showForm && (
          <div className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-md">
            <h2 className="mb-4 font-semibold text-slate-900">Nuevo expediente</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">
                  Título <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={formTitle}
                  onChange={(e) => setFormTitle(e.target.value)}
                  placeholder="Ej: Despido empresa Acme S.L."
                  maxLength={120}
                  className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-[var(--primary)] focus:outline-none focus:ring-1 focus:ring-[var(--primary)]"
                  required
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Categoría</label>
                <select
                  value={formCategory}
                  onChange={(e) => setFormCategory(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-[var(--primary)] focus:outline-none focus:ring-1 focus:ring-[var(--primary)]"
                >
                  <option value="">— Seleccionar —</option>
                  {CATEGORIES.map((c) => (
                    <option key={c.value} value={c.value}>{c.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Descripción breve</label>
                <textarea
                  value={formSummary}
                  onChange={(e) => setFormSummary(e.target.value)}
                  placeholder="Describe brevemente la situación..."
                  rows={2}
                  maxLength={1000}
                  className="w-full rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-[var(--primary)] focus:outline-none focus:ring-1 focus:ring-[var(--primary)]"
                />
              </div>

              {createError && (
                <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
                  {createError}
                  {createError.includes("PRO") && (
                    <button
                      type="button"
                      onClick={() => router.push("/pricing")}
                      className="ml-2 font-bold underline"
                    >
                      Ver planes
                    </button>
                  )}
                </div>
              )}

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={creating || !formTitle.trim()}
                  className="flex-1 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-2 text-sm font-bold text-white disabled:opacity-50 transition-all"
                >
                  {creating ? "Creando..." : "Crear expediente"}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="rounded-xl border border-slate-200 px-4 py-2 text-sm text-slate-600 hover:bg-slate-50"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        {error && (
          <div className="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        )}

        {cases.length === 0 && !showForm && (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-12 text-center">
            <div className="text-5xl">📁</div>
            <h2 className="mt-4 text-lg font-semibold text-slate-800">Sin expedientes aún</h2>
            <p className="mt-2 text-sm text-slate-500">
              Crea un expediente para agrupar conversaciones, documentos y alertas de un mismo problema legal.
            </p>
            <button
              onClick={() => setShowForm(true)}
              className="mt-6 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-6 py-2.5 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
            >
              + Crear primer expediente
            </button>
          </div>
        )}

        {openCases.length > 0 && (
          <section className="mb-6">
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
              Abiertos ({openCases.length})
            </h2>
            <div className="space-y-3">
              {openCases.map((c) => <CaseCard key={c.id} data={c} />)}
            </div>
          </section>
        )}

        {otherCases.length > 0 && (
          <section>
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
              Resueltos / Archivados ({otherCases.length})
            </h2>
            <div className="space-y-3">
              {otherCases.map((c) => <CaseCard key={c.id} data={c} />)}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
