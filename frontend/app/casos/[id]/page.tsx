"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";

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

interface Conversation { id: string; title: string; created_at: string; }
interface Alert { id: string; description: string; deadline_date: string; status: string; urgency_level?: string; }

interface CaseDetail {
  id: string;
  title: string;
  category?: string | null;
  status: "open" | "resolved" | "archived";
  summary?: string | null;
  created_at: string;
  conversations: Conversation[];
  alerts: Alert[];
}

export default function CaseDetailPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const params = useParams();
  const caseId = params.id as string;

  const [data, setData] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Conversations available to link
  const [allConvs, setAllConvs] = useState<{ id: string; title: string }[]>([]);
  const [showLinkModal, setShowLinkModal] = useState(false);
  const [linking, setLinking] = useState(false);

  // Edit title
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleInput, setTitleInput] = useState("");

  // Delete
  const [deleting, setDeleting] = useState(false);

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
    if (!confirm("¿Seguro que quieres eliminar este expediente? Las conversaciones y alertas vinculadas no se borrarán.")) return;
    setDeleting(true);
    const res = await apiFetch(`/cases/${caseId}`, { method: "DELETE" });
    if (res.ok) router.push("/casos");
    else setDeleting(false);
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

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-slate-500">Cargando...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-[#F9FAFB] gap-4">
        <p className="text-slate-600">{error || "Expediente no encontrado."}</p>
        <button onClick={() => router.push("/casos")} className="text-sm text-[var(--primary)] underline">
          ← Volver a expedientes
        </button>
      </div>
    );
  }

  const icon = data.category ? (CATEGORY_ICONS[data.category] ?? "📋") : "📋";
  const linkedConvIds = new Set(data.conversations.map((c) => c.id));
  const unlinkedConvs = allConvs.filter((c) => !linkedConvIds.has(c.id));

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white px-6 py-4 shadow-sm">
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-4">
          <button onClick={() => router.push("/casos")} className="shrink-0 text-sm text-slate-500 hover:text-slate-800">
            ← Expedientes
          </button>
          <div className="flex flex-1 items-center gap-2 min-w-0">
            <span className="text-xl">{icon}</span>
            {editingTitle ? (
              <div className="flex flex-1 items-center gap-2">
                <input
                  value={titleInput}
                  onChange={(e) => setTitleInput(e.target.value)}
                  maxLength={120}
                  className="flex-1 rounded-lg border border-[var(--primary)] px-2 py-1 text-sm focus:outline-none"
                  autoFocus
                  onKeyDown={(e) => { if (e.key === "Enter") handleTitleSave(); if (e.key === "Escape") setEditingTitle(false); }}
                />
                <button onClick={handleTitleSave} className="text-xs text-[var(--primary)] font-semibold">Guardar</button>
                <button onClick={() => setEditingTitle(false)} className="text-xs text-slate-400">✕</button>
              </div>
            ) : (
              <button
                onClick={() => setEditingTitle(true)}
                className="min-w-0 truncate text-left text-base font-semibold text-slate-900 hover:text-[var(--primary)] transition-colors"
                title="Haz clic para editar el título"
              >
                {data.title}
              </button>
            )}
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <span className={`rounded-full px-2.5 py-0.5 text-xs font-medium ${
              data.status === "open" ? "bg-green-100 text-green-700" :
              data.status === "resolved" ? "bg-blue-100 text-blue-700" :
              "bg-slate-100 text-slate-500"
            }`}>
              {STATUS_LABELS[data.status]}
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8 space-y-6">

        {/* Info card */}
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="space-y-1">
              {data.summary && <p className="text-sm text-slate-600">{data.summary}</p>}
              <p className="text-xs text-slate-400">
                Creado el {new Date(data.created_at).toLocaleDateString("es-ES", { day: "numeric", month: "long", year: "numeric" })}
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
                onClick={handleDelete}
                disabled={deleting}
                className="rounded-lg border border-red-200 px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50 transition-colors disabled:opacity-50"
              >
                {deleting ? "Eliminando..." : "Eliminar"}
              </button>
            </div>
          </div>
        </div>

        {/* Conversations */}
        <section>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="font-semibold text-slate-900">
              💬 Conversaciones vinculadas ({data.conversations.length})
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
              <button onClick={handleOpenLinkModal} className="text-[var(--primary)] underline">
                Vincular una
              </button>
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
                    title="Desvincular"
                  >
                    Desvincular
                  </button>
                </div>
              ))}
            </div>
          )}
        </section>

        {/* Alerts */}
        {data.alerts.length > 0 && (
          <section>
            <h2 className="mb-3 font-semibold text-slate-900">
              🔔 Alertas vinculadas ({data.alerts.length})
            </h2>
            <div className="space-y-2">
              {data.alerts.map((alert) => {
                const isUrgent = alert.urgency_level === "urgent" || alert.urgency_level === "critical";
                const deadlineDate = new Date(alert.deadline_date);
                const daysLeft = Math.ceil((deadlineDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24));
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
