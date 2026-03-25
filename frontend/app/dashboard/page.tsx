"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { ToolHeader } from "@/components/ToolHeader";

// ── Types ────────────────────────────────────────────────────────────────────
type Alert = {
  id: string;
  description: string;
  deadline_date: string;
  law_reference?: string;
  days_remaining: number;
  urgency: string;
};

type CaseItem = {
  id: string;
  title: string;
  category?: string;
  status: string;
  conversation_count: number;
  alert_count: number;
  updated_at: string;
};

type Conversation = {
  id: string;
  title: string;
  category?: string;
  subcategory?: string;
  updated_at: string;
};

type LegalEvent = {
  title: string;
  category: string;
  description: string;
  icon: string;
  start_date: string;
  end_date: string;
  active: boolean;
  days_until_start: number;
};

type Reminder = {
  type: string;
  priority: string;
  title: string;
  description: string;
  action_url: string;
  action_label: string;
};

type Recommendation = {
  type: string;
  priority: string;
  title: string;
  reason: string;
  template_id?: string;
  template_title?: string;
  template_icon?: string;
  template_description?: string;
  action_url: string;
  action_label: string;
};

type DashboardData = {
  urgent_alerts: Alert[];
  upcoming_deadlines: Alert[];
  active_cases: CaseItem[];
  recent_conversations: Conversation[];
  stats: { total_cases: number; total_alerts_active: number; total_conversations: number };
  legal_calendar: LegalEvent[];
  reminders?: Reminder[];
  recommendations?: Recommendation[];
};

// ── Helpers ──────────────────────────────────────────────────────────────────
const CATEGORY_ICONS: Record<string, string> = {
  laboral: "💼",
  vivienda: "🏠",
  consumo: "🛒",
  familia: "👨‍👩‍👧",
  trafico: "🚗",
  administrativo: "🏛️",
  fiscal: "💰",
  penal: "⚖️",
  otro: "📋",
};

function formatDeadline(dateStr: string): string {
  try {
    const d = new Date(dateStr + "T00:00:00");
    return d.toLocaleDateString("es-ES", { day: "numeric", month: "short" });
  } catch {
    return dateStr;
  }
}

function timeAgo(dateStr: string): string {
  try {
    const d = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - d.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    if (diffMins < 60) return `hace ${diffMins}m`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `hace ${diffHours}h`;
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `hace ${diffDays}d`;
    return formatDeadline(dateStr.slice(0, 10));
  } catch {
    return "";
  }
}

// ── Component ────────────────────────────────────────────────────────────────
export default function DashboardPage() {
  const { user, profile, loading: authLoading } = useAuth();
  const router = useRouter();

  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || authLoading) return;
    apiFetch("/dashboard")
      .then((r) => r.json())
      .then((res) => setData(res.data))
      .catch(() => setError("No se pudo cargar el panel."))
      .finally(() => setLoading(false));
  }, [user?.id, authLoading]);

  if (authLoading || loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-center">
          <div className="mx-auto h-8 w-8 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
          <p className="mt-3 text-sm text-slate-500">Preparando tu panel...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">
        <div className="text-center">
          <p className="text-red-500 text-sm">{error}</p>
          <button onClick={() => window.location.reload()} className="mt-3 text-sm text-[var(--primary)] underline">
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  const userName = profile?.name || user?.email?.split("@")[0] || "usuario";
  const hasUrgent = (data?.urgent_alerts?.length ?? 0) > 0;
  const hasActiveCases = (data?.active_cases?.length ?? 0) > 0;
  const hasRecent = (data?.recent_conversations?.length ?? 0) > 0;
  const hasCalendar = (data?.legal_calendar?.length ?? 0) > 0;

  return (
    <>
      <ToolHeader title="Mi panel" backHref="/chat" backLabel="Chat" />

      <div className="min-h-screen bg-[#F9FAFB]">
        <div className="mx-auto max-w-5xl px-4 py-6 sm:px-6">
          {/* ── Saludo + Stats ───────────────────────────────────────────── */}
          <div className="mb-6">
            <h1 className="font-display text-2xl font-bold text-slate-900">
              Hola, {userName}
            </h1>
            <p className="mt-1 text-sm text-slate-500">
              Tu resumen legal de hoy
            </p>
          </div>

          {/* ── Stats cards ──────────────────────────────────────────────── */}
          <div className="mb-6 grid grid-cols-3 gap-3">
            <Link href="/casos" className="rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-slate-300 hover:shadow-sm">
              <p className="text-2xl font-bold text-[var(--primary)]">{data?.stats.total_cases ?? 0}</p>
              <p className="text-xs text-slate-500">Expedientes</p>
            </Link>
            <Link href="/alerts" className="rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-slate-300 hover:shadow-sm">
              <p className="text-2xl font-bold text-amber-600">{data?.stats.total_alerts_active ?? 0}</p>
              <p className="text-xs text-slate-500">Alertas activas</p>
            </Link>
            <Link href="/chat" className="rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-slate-300 hover:shadow-sm">
              <p className="text-2xl font-bold text-emerald-600">{data?.stats.total_conversations ?? 0}</p>
              <p className="text-xs text-slate-500">Consultas</p>
            </Link>
          </div>

          {/* ── Alertas urgentes ─────────────────────────────────────────── */}
          {hasUrgent && (
            <section className="mb-6">
              <div className="rounded-xl border border-red-200 bg-red-50 p-4">
                <div className="mb-3 flex items-center gap-2">
                  <span className="flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-xs text-white">!</span>
                  <h2 className="text-sm font-bold text-red-800">
                    Plazos urgentes ({data!.urgent_alerts.length})
                  </h2>
                </div>
                <div className="space-y-2">
                  {data!.urgent_alerts.map((alert) => (
                    <Link
                      key={alert.id}
                      href="/alerts"
                      className="flex items-center justify-between rounded-lg bg-white p-3 border border-red-100 transition-all hover:border-red-200 hover:shadow-sm"
                    >
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-slate-800 truncate">{alert.description}</p>
                        {alert.law_reference && (
                          <p className="text-xs text-slate-500 truncate">{alert.law_reference}</p>
                        )}
                      </div>
                      <div className="ml-3 shrink-0 text-right">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-bold ${
                          alert.days_remaining <= 1
                            ? "bg-red-100 text-red-700"
                            : "bg-amber-100 text-amber-700"
                        }`}>
                          {alert.days_remaining === 0
                            ? "HOY"
                            : alert.days_remaining === 1
                            ? "MAÑANA"
                            : `${alert.days_remaining} días`}
                        </span>
                        <p className="mt-0.5 text-xs text-slate-400">{formatDeadline(alert.deadline_date)}</p>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            </section>
          )}

          {/* ── Recordatorios inteligentes ──────────────────────────────── */}
          {data?.reminders && data.reminders.length > 0 && !hasUrgent && (
            <section className="mb-6">
              <div className="space-y-2">
                {data.reminders.slice(0, 3).map((reminder, i) => (
                  <Link
                    key={i}
                    href={reminder.action_url}
                    className={`flex items-center gap-3 rounded-xl border p-3 transition-all hover:shadow-sm ${
                      reminder.priority === "critical"
                        ? "border-red-200 bg-red-50 hover:border-red-300"
                        : reminder.priority === "high"
                        ? "border-amber-200 bg-amber-50 hover:border-amber-300"
                        : "border-blue-200 bg-blue-50 hover:border-blue-300"
                    }`}
                  >
                    <div className="min-w-0 flex-1">
                      <p className={`text-sm font-medium ${
                        reminder.priority === "critical" ? "text-red-800" : reminder.priority === "high" ? "text-amber-800" : "text-blue-800"
                      }`}>{reminder.title}</p>
                      <p className={`text-xs ${
                        reminder.priority === "critical" ? "text-red-600" : reminder.priority === "high" ? "text-amber-600" : "text-blue-600"
                      }`}>{reminder.description}</p>
                    </div>
                    <span className={`shrink-0 rounded-lg px-2.5 py-1 text-xs font-medium ${
                      reminder.priority === "critical" ? "bg-red-100 text-red-700" : reminder.priority === "high" ? "bg-amber-100 text-amber-700" : "bg-blue-100 text-blue-700"
                    }`}>
                      {reminder.action_label}
                    </span>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* ── Acciones rápidas ─────────────────────────────────────────── */}
          <section className="mb-6">
            <h2 className="mb-3 text-sm font-semibold text-slate-700">Acciones rápidas</h2>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <Link
                href="/chat"
                className="flex flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-[var(--primary)] hover:shadow-md"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-xl">💬</span>
                <span className="text-xs font-semibold text-slate-700">Nueva consulta</span>
              </Link>
              <Link
                href="/calculadora"
                className="flex flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-emerald-400 hover:shadow-md"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-xl">🧮</span>
                <span className="text-xs font-semibold text-slate-700">Calculadora</span>
              </Link>
              <Link
                href="/contrato"
                className="flex flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-violet-400 hover:shadow-md"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-violet-50 text-xl">📄</span>
                <span className="text-xs font-semibold text-slate-700">Analizar contrato</span>
              </Link>
              <Link
                href="/wizard"
                className="flex flex-col items-center gap-2 rounded-xl border border-slate-200 bg-white p-4 text-center transition-all hover:border-amber-400 hover:shadow-md"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 text-xl">📋</span>
                <span className="text-xs font-semibold text-slate-700">Trámite guiado</span>
              </Link>
            </div>
          </section>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* ── Expedientes activos ──────────────────────────────────── */}
            <section>
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-700">Expedientes activos</h2>
                <Link href="/casos" className="text-xs font-medium text-[var(--primary)] hover:underline">
                  Ver todos
                </Link>
              </div>
              {hasActiveCases ? (
                <div className="space-y-2">
                  {data!.active_cases.map((c) => (
                    <Link
                      key={c.id}
                      href={`/casos/${c.id}`}
                      className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 transition-all hover:border-slate-300 hover:shadow-sm"
                    >
                      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-50 text-lg shrink-0">
                        {CATEGORY_ICONS[c.category || "otro"] || "📋"}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-slate-800 truncate">{c.title}</p>
                        <div className="flex items-center gap-2 text-xs text-slate-400">
                          <span>{c.conversation_count} consultas</span>
                          {c.alert_count > 0 && (
                            <span className="text-amber-500">{c.alert_count} alertas</span>
                          )}
                        </div>
                      </div>
                      <svg className="h-4 w-4 text-slate-300 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                      </svg>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center">
                  <p className="text-2xl mb-2">📁</p>
                  <p className="text-sm font-medium text-slate-600">Sin expedientes abiertos</p>
                  <p className="mt-1 text-xs text-slate-400">
                    Crea un expediente para organizar tu trámite paso a paso
                  </p>
                  <Link
                    href="/casos"
                    className="mt-3 inline-block rounded-lg bg-[var(--primary)] px-4 py-1.5 text-xs font-semibold text-white hover:bg-[var(--primary-dark)] transition-colors"
                  >
                    Crear expediente
                  </Link>
                </div>
              )}
            </section>

            {/* ── Conversaciones recientes ─────────────────────────────── */}
            <section>
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-700">Consultas recientes</h2>
                <Link href="/chat" className="text-xs font-medium text-[var(--primary)] hover:underline">
                  Ver todas
                </Link>
              </div>
              {hasRecent ? (
                <div className="space-y-2">
                  {data!.recent_conversations.map((conv) => (
                    <Link
                      key={conv.id}
                      href={`/chat/${conv.id}`}
                      className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 transition-all hover:border-slate-300 hover:shadow-sm"
                    >
                      <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-50 text-lg shrink-0">
                        {CATEGORY_ICONS[conv.category || "otro"] || "💬"}
                      </span>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-slate-800 truncate">
                          {conv.title || "Consulta sin título"}
                        </p>
                        {conv.subcategory && (
                          <p className="text-xs text-slate-400 capitalize">{conv.subcategory}</p>
                        )}
                      </div>
                      <span className="text-xs text-slate-400 shrink-0">{timeAgo(conv.updated_at)}</span>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-center">
                  <p className="text-2xl mb-2">💬</p>
                  <p className="text-sm font-medium text-slate-600">Sin consultas todavía</p>
                  <p className="mt-1 text-xs text-slate-400">
                    Pregunta lo que necesites sobre tus trámites legales
                  </p>
                  <Link
                    href="/chat"
                    className="mt-3 inline-block rounded-lg bg-[var(--primary)] px-4 py-1.5 text-xs font-semibold text-white hover:bg-[var(--primary-dark)] transition-colors"
                  >
                    Empezar consulta
                  </Link>
                </div>
              )}
            </section>
          </div>

          {/* ── Próximos plazos (timeline) ────────────────────────────────── */}
          {(data?.upcoming_deadlines?.length ?? 0) > 0 && (
            <section className="mt-6">
              <div className="mb-3 flex items-center justify-between">
                <h2 className="text-sm font-semibold text-slate-700">Próximos plazos (7 días)</h2>
                <Link href="/alerts" className="text-xs font-medium text-[var(--primary)] hover:underline">
                  Ver alertas
                </Link>
              </div>
              <div className="rounded-xl border border-slate-200 bg-white p-4">
                <div className="space-y-3">
                  {data!.upcoming_deadlines.map((dl) => (
                    <div key={dl.id} className="flex items-center gap-3">
                      <div className="flex flex-col items-center">
                        <span className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold text-white ${
                          dl.days_remaining <= 1
                            ? "bg-red-500"
                            : dl.days_remaining <= 3
                            ? "bg-amber-500"
                            : "bg-blue-500"
                        }`}>
                          {dl.days_remaining}
                        </span>
                        <span className="text-[10px] text-slate-400 mt-0.5">días</span>
                      </div>
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-slate-800 truncate">{dl.description}</p>
                        <p className="text-xs text-slate-400">{formatDeadline(dl.deadline_date)}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          )}

          {/* ── Recomendaciones personalizadas ─────────────────────────── */}
          {data?.recommendations && data.recommendations.length > 0 && (
            <section className="mt-6">
              <h2 className="mb-3 text-sm font-semibold text-slate-700">Recomendado para ti</h2>
              <div className="grid gap-3 sm:grid-cols-2">
                {data.recommendations.slice(0, 4).map((rec, i) => (
                  <Link
                    key={i}
                    href={rec.action_url}
                    className="group flex items-start gap-3 rounded-xl border border-slate-200 bg-white p-4 transition-all hover:border-[var(--primary)] hover:shadow-md"
                  >
                    <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-xl shrink-0 group-hover:bg-blue-100 transition-colors">
                      {rec.template_icon || "💡"}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="text-sm font-semibold text-slate-800 group-hover:text-[var(--primary)] transition-colors">
                        {rec.template_title || rec.title}
                      </p>
                      <p className="text-xs text-slate-500 mt-0.5 line-clamp-2">
                        {rec.reason}
                      </p>
                      <span className="mt-2 inline-flex items-center gap-1 text-xs font-medium text-[var(--primary)]">
                        {rec.action_label}
                        <svg className="h-3 w-3" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                        </svg>
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          )}

          {/* ── Calendario legal ──────────────────────────────────────────── */}
          {hasCalendar && (
            <section className="mt-6 mb-8">
              <h2 className="mb-3 text-sm font-semibold text-slate-700">Calendario legal</h2>
              <div className="space-y-2">
                {data!.legal_calendar.map((event, i) => (
                  <div
                    key={i}
                    className={`flex items-start gap-3 rounded-xl border p-3 ${
                      event.active
                        ? "border-emerald-200 bg-emerald-50"
                        : "border-slate-200 bg-white"
                    }`}
                  >
                    <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-white text-lg shrink-0 shadow-sm">
                      {event.icon}
                    </span>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-medium text-slate-800">{event.title}</p>
                        {event.active && (
                          <span className="rounded-full bg-emerald-500 px-2 py-0.5 text-[10px] font-bold text-white">
                            EN CURSO
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 mt-0.5">{event.description}</p>
                      {!event.active && event.days_until_start > 0 && (
                        <p className="text-xs text-slate-400 mt-0.5">
                          Comienza en {event.days_until_start} días ({formatDeadline(event.start_date)})
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}
        </div>
      </div>
    </>
  );
}
