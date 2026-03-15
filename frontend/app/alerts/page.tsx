"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useAlerts } from "@/hooks/useAlerts";
import { apiFetch } from "@/lib/api";
import { AlertCard } from "@/components/alerts/AlertCard";
import { AlertCalendar } from "@/components/alerts/AlertCalendar";
import { ManualCreateAlertModal } from "@/components/alerts/ManualCreateAlertModal";

type Tab = "active" | "expired" | "dismissed";
type View = "list" | "calendar";

export default function AlertsPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("active");
  const [view, setView] = useState<View>("calendar");
  const [searchQuery, setSearchQuery] = useState("");
  const [urgencyFilter, setUrgencyFilter] = useState<string>("all");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [userPlan, setUserPlan] = useState<string>("free");
  const { alerts, isLoading, dismissAlert, deleteAlert, refresh } = useAlerts(!!user && !authLoading && (userPlan === "pro" || userPlan === "document"));

  useEffect(() => {
    if (user && !authLoading) {
      apiFetch("/me")
        .then((r) => r.json())
        .then((data) => setUserPlan(data?.plan || "free"))
        .catch(() => setUserPlan("free"));
    }
  }, [user, authLoading]);

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  const filtered = alerts
    .filter((a) => {
      if (tab === "active") return a.status === "active";
      if (tab === "expired") return a.status === "expired";
      return a.status === "dismissed";
    })
    .filter((a) => {
      if (!searchQuery) return true;
      return (
        a.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (a.law_reference && a.law_reference.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    })
    .filter((a) => {
      if (urgencyFilter === "all") return true;
      return a.urgency === urgencyFilter;
    });

  const activeCount = alerts.filter((a) => a.status === "active").length;
  const expiredCount = alerts.filter((a) => a.status === "expired").length;
  const dismissedCount = alerts.filter((a) => a.status === "dismissed").length;

  if (authLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-slate-500">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="mx-auto flex max-w-5xl items-center justify-between">
          <div className="flex items-center gap-6">
            <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
              TramitUp
            </span>
            <span className="text-sm text-slate-500">Mis alertas de plazos</span>
          </div>
          <div className="flex items-center gap-4">
            {userPlan !== "pro" && userPlan !== "document" && (
              <Link
                href="/account"
                className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700"
              >
                ★ Hazte PRO
              </Link>
            )}
            {/* View toggle */}
            <div className="flex items-center overflow-hidden rounded-lg border border-slate-200 bg-slate-50">
              <button
                onClick={() => setView("calendar")}
                className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                  view === "calendar"
                    ? "bg-[#1A56DB] text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                📅 Calendario
              </button>
              <button
                onClick={() => setView("list")}
                className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                  view === "list"
                    ? "bg-[#1A56DB] text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                📋 Lista
              </button>
            </div>
            <button
              onClick={() => {
                if (userPlan !== "pro" && userPlan !== "document") {
                  router.push("/account");
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white hover:bg-[#1542a8]"
            >
              + Nueva Alerta
            </button>
            <Link href="/chat" className="text-sm text-slate-600 hover:text-slate-800">
              ← Chat
            </Link>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl p-6">
        {userPlan !== "pro" && userPlan !== "document" && (
          <div className="mb-6 rounded-xl border-2 border-amber-500 bg-amber-50 p-6">
            <h3 className="text-lg font-semibold text-amber-800">⭐ Las alertas son exclusivas de PRO</h3>
            <p className="mt-2 text-sm text-amber-700">
              Hazte PRO para crear alertas de plazos legales y recibir avisos por email antes de que venzan.
            </p>
            <Link
              href="/account"
              className="mt-4 inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-6 py-2.5 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700"
            >
              ★ Hazte PRO — 9,99 €/mes
            </Link>
          </div>
        )}
        {/* Stats strip */}
        <div className="mb-6 grid grid-cols-3 gap-4">
          <div className="rounded-xl border border-slate-200 bg-white p-4 text-center shadow-sm">
            <p className="text-2xl font-bold text-slate-800">{activeCount}</p>
            <p className="text-xs text-slate-500">Activas</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-4 text-center shadow-sm">
            <p className="text-2xl font-bold text-red-600">
              {alerts.filter((a) => a.status === "active" && a.days_remaining <= 3).length}
            </p>
            <p className="text-xs text-slate-500">Urgentes (≤3 días)</p>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-4 text-center shadow-sm">
            <p className="text-2xl font-bold text-slate-400">{expiredCount}</p>
            <p className="text-xs text-slate-500">Vencidas</p>
          </div>
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <p className="text-slate-500">Cargando alertas...</p>
          </div>
        ) : view === "calendar" ? (
          <AlertCalendar
            alerts={alerts.filter((a) => a.status !== "dismissed")}
            onDismiss={dismissAlert}
            onDelete={deleteAlert}
          />
        ) : (
          <>
            {/* Tabs */}
            <div className="mb-6 flex gap-2 border-b border-slate-200">
              {(["active", "expired", "dismissed"] as Tab[]).map((t) => {
                const counts = { active: activeCount, expired: expiredCount, dismissed: dismissedCount };
                const labels = { active: "Activas", expired: "Vencidas", dismissed: "Descartadas" };
                return (
                  <button
                    key={t}
                    onClick={() => setTab(t)}
                    className={`border-b-2 px-4 py-2 text-sm font-medium ${
                      tab === t
                        ? "border-[#1A56DB] text-[#1A56DB]"
                        : "border-transparent text-slate-500"
                    }`}
                  >
                    {labels[t]} ({counts[t]})
                  </button>
                );
              })}
            </div>

            {/* Filters */}
            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex flex-1 gap-3">
                <input
                  type="text"
                  placeholder="Buscar alertas..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
                />
                <select
                  value={urgencyFilter}
                  onChange={(e) => setUrgencyFilter(e.target.value)}
                  className="rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-[#1A56DB] focus:outline-none focus:ring-1 focus:ring-[#1A56DB]"
                >
                  <option value="all">Todas las urgencias</option>
                  <option value="high">Alta urgencia</option>
                  <option value="medium">Media urgencia</option>
                  <option value="low">Baja urgencia</option>
                </select>
              </div>
              {(searchQuery || urgencyFilter !== "all") && (
                <button
                  onClick={() => { setSearchQuery(""); setUrgencyFilter("all"); }}
                  className="text-sm text-slate-500 hover:text-slate-700"
                >
                  Limpiar filtros
                </button>
              )}
            </div>

            {filtered.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center">
                <p className="mb-2 text-4xl">⏰</p>
                <p className="mb-4 text-slate-600">No tienes alertas {tab === "active" ? "activas" : tab === "expired" ? "vencidas" : "descartadas"}.</p>
                <p className="mb-6 text-sm text-slate-500">
                  Cuando el asistente detecte plazos en tu conversación, se añadirán aquí automáticamente.
                </p>
                <Link
                  href="/chat"
                  className="inline-flex items-center gap-2 rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white hover:bg-[#1545a8]"
                >
                  Ir al chat →
                </Link>
              </div>
            ) : (
              <ul className="space-y-4">
                {filtered.map((alert) => (
                  <li key={alert.alert_id}>
                    <AlertCard
                      alert={alert}
                      onDismiss={() => dismissAlert(alert.alert_id)}
                      onDelete={() => deleteAlert(alert.alert_id)}
                    />
                  </li>
                ))}
              </ul>
            )}
          </>
        )}
      </main>

      <ManualCreateAlertModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreateAlert={async (alertData) => {
          try {
            await fetch('/api/backend/alerts/create', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              credentials: 'include',
              body: JSON.stringify(alertData)
            });
            refresh();
            setShowCreateModal(false);
          } catch (error) {
            console.error('Error creating alert:', error);
            throw error;
          }
        }}
      />
    </div>
  );
}
