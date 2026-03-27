"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useAlerts } from "@/hooks/useAlerts";
import { apiFetch } from "@/lib/api";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";
import { ToolHeader } from "@/components/ToolHeader";
import { ProButton } from "@/components/ProBadge";
import { AlertCard } from "@/components/alerts/AlertCard";
import { AlertCalendar } from "@/components/alerts/AlertCalendar";
import { ManualCreateAlertModal } from "@/components/alerts/ManualCreateAlertModal";
import { Calendar, ClipboardList, Bell, MessageSquare, AlertTriangle } from "@/lib/icons";

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
  const { startCheckout, loading: checkoutLoading } = useStripeCheckout();

  useEffect(() => {
    if (user?.id && !authLoading) {
      apiFetch("/me")
        .then((r) => r.json())
        .then((data) => setUserPlan(data?.plan || "free"))
        .catch(() => setUserPlan("free"));
    }
  }, [user?.id, authLoading]);

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
      <ToolHeader
        title="Mis alertas de plazos"
        actions={
          <div className="flex items-center gap-2">
            {userPlan !== "pro" && userPlan !== "document" && (
              <ProButton onClick={startCheckout} disabled={checkoutLoading} size="sm" />
            )}
            <div className="flex items-center overflow-hidden rounded-lg border border-slate-200 bg-slate-50">
              <button
                onClick={() => setView("calendar")}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium transition-colors ${
                  view === "calendar"
                    ? "bg-[#1A56DB] text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                <Calendar className="h-4 w-4" /> Calendario
              </button>
              <button
                onClick={() => setView("list")}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium transition-colors ${
                  view === "list"
                    ? "bg-[#1A56DB] text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                <ClipboardList className="h-4 w-4" /> Lista
              </button>
            </div>
            <button
              onClick={() => {
                if (userPlan !== "pro" && userPlan !== "document") {
                  startCheckout();
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white hover:bg-[#1542a8]"
            >
              + Nueva Alerta
            </button>
          </div>
        }
      />

      <main className="mx-auto max-w-5xl p-6">
        {userPlan !== "pro" && userPlan !== "document" && (
          <div className="mb-6 rounded-xl border-2 border-amber-500 bg-amber-50 p-6">
            <h3 className="flex items-center gap-2 text-lg font-semibold text-amber-800"><AlertTriangle className="h-5 w-5 text-amber-600" /> Las alertas son exclusivas de PRO</h3>
            <p className="mt-2 text-sm text-amber-700">
              Hazte PRO para crear alertas de plazos legales y recibir avisos por email antes de que venzan.
            </p>
            <ProButton
              onClick={startCheckout}
              disabled={checkoutLoading}
              label="Probar 3 días gratis"
            />
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
              <div className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
                <div className="text-center">
                  <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 shadow-lg shadow-amber-500/20">
                    <Bell className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="mt-5 text-lg font-bold text-slate-800">
                    {tab === "active"
                      ? "Nunca más pierdas un plazo legal"
                      : tab === "expired"
                      ? "Sin plazos vencidos"
                      : "Sin alertas descartadas"}
                  </h3>
                  {tab === "active" && (
                    <>
                      <p className="mt-2 mx-auto max-w-md text-sm text-slate-500">
                        TramitUp detecta plazos automáticamente en tus consultas y te avisa por email antes de que venzan. También puedes crear alertas manualmente.
                      </p>
                      <div className="mt-5 flex flex-col sm:flex-row items-center justify-center gap-3">
                        <Link
                          href="/chat"
                          className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-5 py-2.5 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
                        >
                          <MessageSquare className="h-4 w-4" /> Consultar al asistente
                        </Link>
                        <button
                          onClick={() => {
                            if (userPlan === "pro" || userPlan === "document") {
                              setShowCreateModal(true);
                            } else {
                              startCheckout();
                            }
                          }}
                          className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-all"
                        >
                          + Crear alerta manual
                        </button>
                      </div>
                      <div className="mt-6 grid grid-cols-3 gap-3 text-center max-w-sm mx-auto">
                        <div>
                          <p className="text-lg">7 días</p>
                          <p className="text-[11px] text-slate-400">Primer aviso</p>
                        </div>
                        <div>
                          <p className="text-lg">3 días</p>
                          <p className="text-[11px] text-slate-400">Recordatorio</p>
                        </div>
                        <div>
                          <p className="text-lg">1 día</p>
                          <p className="text-[11px] text-slate-400">Aviso urgente</p>
                        </div>
                      </div>
                    </>
                  )}
                  {tab !== "active" && (
                    <p className="mt-2 text-sm text-slate-500">
                      {tab === "expired"
                        ? "Los plazos vencidos aparecerán aquí para tu referencia."
                        : "Las alertas que descartes aparecerán aquí."}
                    </p>
                  )}
                </div>
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
          const res = await apiFetch("/alerts/create", {
            method: "POST",
            body: JSON.stringify(alertData),
          });
          if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            throw new Error(data?.detail || "Error creando la alerta");
          }
          refresh();
          setShowCreateModal(false);
        }}
      />
    </div>
  );
}
