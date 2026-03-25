"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { ToolHeader } from "@/components/ToolHeader";

const STATUS_LABELS: Record<string, string> = {
  open: "Abierto",
  resolved: "Resuelto",
  archived: "Archivado",
};

const STATUS_NEXT: Record<string, { label: string; value: string }[]> = {
  open: [
    { label: "Marcar resuelto", value: "resolved" },
    { label: "Archivar", value: "archived" },
  ],
  resolved: [
    { label: "Reabrir", value: "open" },
    { label: "Archivar", value: "archived" },
  ],
  archived: [
    { label: "Reabrir", value: "open" },
  ],
};

const CATEGORY_ICONS: Record<string, string> = {
  laboral: "💼", vivienda: "🏠", consumo: "🛒", familia: "👨‍👩‍👧",
  trafico: "🚗", administrativo: "🏛️", fiscal: "💰", penal: "⚖️", otro: "📋",
};

const STEP_STATUS_STYLES: Record<string, { bg: string; text: string; icon: string }> = {
  completed: { bg: "bg-emerald-500", text: "text-emerald-700", icon: "✓" },
  in_progress: { bg: "bg-blue-500", text: "text-blue-700", icon: "→" },
  pending: { bg: "bg-slate-300", text: "text-slate-500", icon: "" },
  skipped: { bg: "bg-slate-200", text: "text-slate-400", icon: "—" },
};

interface WorkflowStep {
  step: number;
  title: string;
  description: string;
  status: string;
}

interface RequiredDoc {
  name: string;
  required: boolean;
  how_to_get?: string;
  portal?: string;
  checked?: boolean;
}

interface Conversation { id: string; title: string; created_at: string; }
interface Alert { id: string; description: string; deadline_date: string; status: string; urgency_level?: string; }

interface CaseDetail {
  id: string;
  title: string;
  category?: string | null;
  subcategory?: string | null;
  status: "open" | "resolved" | "archived";
  summary?: string | null;
  created_at: string;
  conversations: Conversation[];
  alerts: Alert[];
  workflow_steps?: WorkflowStep[];
  required_documents?: RequiredDoc[];
  progress_pct?: number;
  next_action?: string | null;
  next_action_deadline?: string | null;
}

export default function CaseDetailPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const caseId = params.id as string;

  const [data, setData] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [allConvs, setAllConvs] = useState<{ id: string; title: string }[]>([]);
  const [showLinkModal, setShowLinkModal] = useState(false);
  const [linking, setLinking] = useState(false);

  const [editingTitle, setEditingTitle] = useState(false);
  const [titleInput, setTitleInput] = useState("");
  const [deleting, setDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || authLoading) return;
    apiFetch(`/cases/${caseId}`)
      .then((r) => {
        if (!r.ok) throw new Error("not found");
        return r.json();
      })
      .then((d) => {
        setData(d);
        setTitleInput(d.title);
      })
      .catch(() => setError("Expediente no encontrado."))
      .finally(() => setLoading(false));
  }, [user?.id, authLoading, caseId]);

  // ── Handlers ──────────────────────────────────────────────────────────────
  const handleStatusChange = async (newStatus: string) => {
    if (!data) return;
    const res = await apiFetch(`/cases/${caseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    if (res.ok) setData((d) => d ? { ...d, status: newStatus as CaseDetail["status"] } : d);
  };

  const handleTitleSave = async () => {
    if (!titleInput.trim() || !data) return;
    const res = await apiFetch(`/cases/${caseId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: titleInput.trim() }),
    });
    if (res.ok) {
      setData((d) => d ? { ...d, title: titleInput.trim() } : d);
      setEditingTitle(false);
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    const res = await apiFetch(`/cases/${caseId}`, { method: "DELETE" });
    if (res.ok) router.push("/casos");
    else {
      setDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const handleStepUpdate = async (stepIndex: number, newStatus: string) => {
    const res = await apiFetch(`/cases/${caseId}/steps/${stepIndex}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    if (res.ok) {
      const updated = await res.json();
      setData((d) => d ? {
        ...d,
        workflow_steps: updated.workflow_steps,
        progress_pct: updated.progress_pct,
        next_action: updated.next_action,
        status: updated.status || d.status,
      } : d);
    }
  };

  const handleDocCheck = async (docIndex: number, checked: boolean) => {
    const res = await apiFetch(`/cases/${caseId}/documents/${docIndex}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ checked }),
    });
    if (res.ok && data) {
      const docs = [...(data.required_documents || [])];
      docs[docIndex] = { ...docs[docIndex], checked };
      setData((d) => d ? { ...d, required_documents: docs } : d);
    }
  };

  const handleOpenLinkModal = async () => {
    setShowLinkModal(true);
    if (allConvs.length > 0) return;
    const res = await apiFetch("/history");
    const d = await res.json();
    setAllConvs(d.conversations || []);
  };

  const handleLink = async (convId: string) => {
    setLinking(true);
    const res = await apiFetch(`/cases/${caseId}/conversations/${convId}`, { method: "POST" });
    if (res.ok) {
      const conv = allConvs.find((c) => c.id === convId);
      if (conv) {
        setData((d) =>
          d ? { ...d, conversations: [{ ...conv, created_at: new Date().toISOString() }, ...d.conversations] } : d
        );
      }
      setShowLinkModal(false);
    }
    setLinking(false);
  };

  const handleUnlink = async (convId: string) => {
    const res = await apiFetch(`/cases/${caseId}/conversations/${convId}`, { method: "DELETE" });
    if (res.ok) {
      setData((d) => d ? { ...d, conversations: d.conversations.filter((c) => c.id !== convId) } : d);
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────
  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
          <p className="mt-3 text-sm text-slate-500">Cargando expediente...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-[#F9FAFB] gap-4">
        <p className="text-slate-600">{error || "Expediente no encontrado."}</p>
        <button onClick={() => router.push("/casos")} className="text-sm text-[var(--primary)] underline">
          Volver a expedientes
        </button>
      </div>
    );
  }

  const icon = data.category ? (CATEGORY_ICONS[data.category] ?? "📋") : "📋";
  const linkedConvIds = new Set(data.conversations.map((c) => c.id));
  const unlinkedConvs = allConvs.filter((c) => !linkedConvIds.has(c.id));
  const steps = data.workflow_steps || [];
  const docs = data.required_documents || [];
  const progress = data.progress_pct ?? 0;
  const docsChecked = docs.filter((d) => d.checked).length;

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <ToolHeader
        title={`${icon} ${data.title}`}
        backHref="/casos"
        backLabel="Expedientes"
        actions={
          <div className="flex items-center gap-2">
            {editingTitle ? (
              <div className="flex items-center gap-2">
                <input
                  value={titleInput}
                  onChange={(e) => setTitleInput(e.target.value)}
                  maxLength={120}
                  className="rounded-lg border border-[var(--primary)] px-2 py-1 text-sm focus:outline-none"
                  autoFocus
                  onKeyDown={(e) => { if (e.key === "Enter") handleTitleSave(); if (e.key === "Escape") setEditingTitle(false); }}
                />
                <button onClick={handleTitleSave} className="text-xs text-[var(--primary)] font-semibold">Guardar</button>
                <button onClick={() => setEditingTitle(false)} className="text-xs text-slate-400">✕</button>
              </div>
            ) : (
              <button
                onClick={() => setEditingTitle(true)}
                className="text-xs text-slate-500 hover:text-[var(--primary)] transition-colors"
              >
                Editar
              </button>
            )}
            <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
              data.status === "open" ? "bg-green-100 text-green-700" :
              data.status === "resolved" ? "bg-blue-100 text-blue-700" :
              "bg-slate-100 text-slate-500"
            }`}>
              {STATUS_LABELS[data.status]}
            </span>
          </div>
        }
      />

      <main className="mx-auto max-w-3xl px-4 py-6 space-y-6">

        {/* ── Progress bar ─────────────────────────────────────────────── */}
        {steps.length > 0 && (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h2 className="text-sm font-semibold text-slate-800">Progreso del expediente</h2>
                {data.next_action && (
                  <p className="text-xs text-slate-500 mt-0.5">
                    Siguiente: <span className="font-medium text-[var(--primary)]">{data.next_action}</span>
                  </p>
                )}
              </div>
              <span className="text-lg font-bold text-[var(--primary)]">{progress}%</span>
            </div>
            <div className="h-3 w-full rounded-full bg-slate-100 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-[var(--primary)] to-blue-500 transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* ── Next action card ─────────────────────────────────────────── */}
        {data.next_action && data.status === "open" && (
          <div className="rounded-2xl border border-blue-200 bg-blue-50 p-5">
            <div className="flex items-start gap-3">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[var(--primary)] text-sm text-white font-bold shrink-0">
                {steps.findIndex((s) => s.status === "pending" || s.status === "in_progress") + 1}
              </span>
              <div>
                <p className="text-sm font-semibold text-blue-900">{data.next_action}</p>
                {steps.find((s) => s.title === data.next_action)?.description && (
                  <p className="text-xs text-blue-700 mt-1">
                    {steps.find((s) => s.title === data.next_action)?.description}
                  </p>
                )}
                <button
                  onClick={() => {
                    const idx = steps.findIndex((s) => s.title === data.next_action);
                    if (idx >= 0) handleStepUpdate(idx, "completed");
                  }}
                  className="mt-3 rounded-lg bg-[var(--primary)] px-4 py-1.5 text-xs font-semibold text-white hover:bg-[var(--primary-dark)] transition-colors"
                >
                  Marcar como completado
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ── Workflow timeline ─────────────────────────────────────────── */}
        {steps.length > 0 && (
          <section>
            <h2 className="mb-3 text-sm font-semibold text-slate-700">Pasos del trámite</h2>
            <div className="space-y-0">
              {steps.map((step, i) => {
                const style = STEP_STATUS_STYLES[step.status] || STEP_STATUS_STYLES.pending;
                const isLast = i === steps.length - 1;
                return (
                  <div key={i} className="flex gap-3">
                    {/* Timeline line + dot */}
                    <div className="flex flex-col items-center">
                      <div className={`flex h-7 w-7 items-center justify-center rounded-full ${style.bg} text-xs font-bold text-white shrink-0`}>
                        {style.icon || step.step}
                      </div>
                      {!isLast && (
                        <div className={`w-0.5 flex-1 min-h-[24px] ${step.status === "completed" || step.status === "skipped" ? "bg-emerald-300" : "bg-slate-200"}`} />
                      )}
                    </div>
                    {/* Content */}
                    <div className={`pb-4 flex-1 ${isLast ? "" : ""}`}>
                      <div className="flex items-center justify-between">
                        <p className={`text-sm font-medium ${step.status === "completed" ? "text-emerald-700 line-through" : step.status === "skipped" ? "text-slate-400 line-through" : "text-slate-800"}`}>
                          {step.title}
                        </p>
                        {/* Step actions */}
                        {data.status === "open" && (
                          <div className="flex gap-1">
                            {step.status === "pending" && (
                              <>
                                <button
                                  onClick={() => handleStepUpdate(i, "completed")}
                                  className="rounded px-2 py-0.5 text-[10px] font-medium text-emerald-600 hover:bg-emerald-50 transition-colors"
                                >
                                  Completar
                                </button>
                                <button
                                  onClick={() => handleStepUpdate(i, "skipped")}
                                  className="rounded px-2 py-0.5 text-[10px] font-medium text-slate-400 hover:bg-slate-50 transition-colors"
                                >
                                  Saltar
                                </button>
                              </>
                            )}
                            {(step.status === "completed" || step.status === "skipped") && (
                              <button
                                onClick={() => handleStepUpdate(i, "pending")}
                                className="rounded px-2 py-0.5 text-[10px] font-medium text-slate-400 hover:bg-slate-50 transition-colors"
                              >
                                Deshacer
                              </button>
                            )}
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">{step.description}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* ── Document checklist ────────────────────────────────────────── */}
        {docs.length > 0 && (
          <section>
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-sm font-semibold text-slate-700">Documentos necesarios</h2>
              <span className="text-xs text-slate-400">{docsChecked} de {docs.length} listos</span>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-sm">
              {docs.map((doc, i) => (
                <div
                  key={i}
                  className={`flex items-start gap-3 px-4 py-3 ${i < docs.length - 1 ? "border-b border-slate-100" : ""} ${doc.checked ? "bg-emerald-50/50" : ""}`}
                >
                  <button
                    onClick={() => handleDocCheck(i, !doc.checked)}
                    className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded border-2 transition-all ${
                      doc.checked
                        ? "border-emerald-500 bg-emerald-500 text-white"
                        : "border-slate-300 hover:border-[var(--primary)]"
                    }`}
                  >
                    {doc.checked && (
                      <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    )}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <p className={`text-sm font-medium ${doc.checked ? "text-emerald-700 line-through" : "text-slate-800"}`}>
                        {doc.name}
                      </p>
                      {doc.required && !doc.checked && (
                        <span className="rounded bg-red-100 px-1.5 py-0.5 text-[10px] font-semibold text-red-600">
                          Obligatorio
                        </span>
                      )}
                    </div>
                    {doc.how_to_get && !doc.checked && (
                      <p className="text-xs text-slate-500 mt-0.5">{doc.how_to_get}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* ── Info card + actions ───────────────────────────────────────── */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              {data.summary && <p className="text-sm text-slate-600">{data.summary}</p>}
              <p className="text-xs text-slate-400">
                Creado el {new Date(data.created_at).toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" })}
                {data.category && <span className="ml-2 capitalize">{icon} {data.category}{data.subcategory ? ` > ${data.subcategory}` : ""}</span>}
              </p>
            </div>
            <div className="flex flex-wrap gap-2">
              {(STATUS_NEXT[data.status] ?? []).map((action) => (
                <button
                  key={action.value}
                  onClick={() => handleStatusChange(action.value)}
                  className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:border-slate-300 hover:bg-slate-50 transition-colors"
                >
                  {action.label}
                </button>
              ))}
              <button
                onClick={() => setShowDeleteConfirm(true)}
                disabled={deleting}
                className="rounded-lg border border-red-200 px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
              >
                {deleting ? "Eliminando..." : "Eliminar"}
              </button>
            </div>
          </div>
        </div>

        {/* ── Conversations ────────────────────────────────────────────── */}
        <section>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-700">
              Conversaciones vinculadas ({data.conversations.length})
            </h2>
            <button
              onClick={handleOpenLinkModal}
              className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:border-[var(--primary)] hover:text-[var(--primary)] transition-colors"
            >
              + Vincular conversación
            </button>
          </div>

          {data.conversations.length === 0 ? (
            <div className="rounded-xl border border-dashed border-slate-200 bg-white p-6 text-center text-sm text-slate-400">
              No hay conversaciones vinculadas.{" "}
              <button onClick={handleOpenLinkModal} className="text-[var(--primary)] underline">Vincular una</button>
              {" "}o{" "}
              <Link href="/chat" className="text-[var(--primary)] underline">iniciar consulta</Link>
            </div>
          ) : (
            <div className="space-y-2">
              {data.conversations.map((conv) => (
                <div
                  key={conv.id}
                  className="flex items-center justify-between rounded-xl border border-slate-200 bg-white px-4 py-3"
                >
                  <div className="min-w-0">
                    <a
                      href={`/chat?conv=${conv.id}`}
                      className="truncate text-sm font-medium text-slate-800 hover:text-[var(--primary)] transition-colors"
                    >
                      {conv.title || "Conversación sin título"}
                    </a>
                    <p className="text-xs text-slate-400">
                      {new Date(conv.created_at).toLocaleDateString("es-ES")}
                    </p>
                  </div>
                  <button
                    onClick={() => handleUnlink(conv.id)}
                    className="ml-3 shrink-0 text-xs text-slate-400 hover:text-red-500 transition-colors"
                  >
                    Desvincular
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* ── Alerts ──────────────────────────────────────────────────── */}
        {data.alerts.length > 0 && (
          <section>
            <h2 className="mb-3 text-sm font-semibold text-slate-700">
              Alertas vinculadas ({data.alerts.length})
            </h2>
            <div className="space-y-2">
              {data.alerts.map((alert) => {
                const deadlineDate = new Date(alert.deadline_date);
                const daysLeft = Math.ceil((deadlineDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
                const isUrgent = daysLeft <= 3;
                return (
                  <div
                    key={alert.id}
                    className={`rounded-xl border px-4 py-3 ${isUrgent ? "border-red-200 bg-red-50" : "border-amber-200 bg-amber-50"}`}
                  >
                    <p className={`text-sm font-medium ${isUrgent ? "text-red-800" : "text-amber-800"}`}>
                      {alert.description}
                    </p>
                    <p className={`mt-0.5 text-xs ${isUrgent ? "text-red-600" : "text-amber-600"}`}>
                      Vence {deadlineDate.toLocaleDateString("es-ES")}
                      {daysLeft >= 0 ? ` · ${daysLeft} días restantes` : " · VENCIDO"}
                    </p>
                  </div>
                );
              })}
            </div>
          </section>
        )}
      </main>

      {/* Delete confirmation modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
            <h3 className="mb-2 font-semibold text-slate-900">Eliminar expediente</h3>
            <p className="mb-5 text-sm text-slate-600">
              ¿Seguro que quieres eliminar este expediente? Esta acción no se puede deshacer.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors"
              >
                Cancelar
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting}
                className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {deleting ? "Eliminando..." : "Sí, eliminar"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Link conversation modal */}
      {showLinkModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="font-semibold text-slate-900">Vincular conversación</h3>
              <button onClick={() => setShowLinkModal(false)} className="text-slate-400 hover:text-slate-600">✕</button>
            </div>

            {unlinkedConvs.length === 0 ? (
              <p className="text-sm text-slate-500">
                {allConvs.length === 0
                  ? "No tienes conversaciones en el historial."
                  : "Todas tus conversaciones ya están vinculadas a este expediente."}
              </p>
            ) : (
              <div className="max-h-72 space-y-2 overflow-y-auto">
                {unlinkedConvs.map((conv) => (
                  <button
                    key={conv.id}
                    disabled={linking}
                    onClick={() => handleLink(conv.id)}
                    className="w-full rounded-xl border border-slate-200 px-4 py-3 text-left text-sm hover:border-[var(--primary)] hover:bg-blue-50 transition-colors disabled:opacity-50"
                  >
                    {conv.title || "Conversación sin título"}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
