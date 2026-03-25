"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { createClient } from "@/lib/supabase/client";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";
import { ToolHeader } from "@/components/ToolHeader";

const CATEGORIES = [
  { id: "reclamaciones", label: "Reclamaciones", icon: "✈️" },
  { id: "laboral", label: "Laboral", icon: "💼" },
  { id: "vivienda", label: "Vivienda", icon: "🏠" },
  { id: "tramites", label: "Trámites", icon: "🏛️" },
];

type ApiProfile = {
  id: string;
  email: string | null;
  plan: string;
  documents_used_today: number;
  remaining_chats_today: number;
};

type SubscriptionInfo = {
  subscription_id: string;
  status: string; // active, trialing, canceled, past_due
  current_period_end: number; // unix timestamp
  cancel_at_period_end: boolean;
  trial_end: number | null; // unix timestamp
  canceled_at: number | null;
};

function formatDate(ts: number): string {
  return new Date(ts * 1000).toLocaleDateString("es-ES", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function daysUntil(ts: number): number {
  return Math.max(0, Math.ceil((ts * 1000 - Date.now()) / (1000 * 60 * 60 * 24)));
}

export default function AccountPage() {
  const { user, profile, signOut, refreshProfile } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [apiProfile, setApiProfile] = useState<ApiProfile | null>(null);
  const [subscription, setSubscription] = useState<SubscriptionInfo | null>(null);
  const [subLoading, setSubLoading] = useState(true);
  const [categories, setCategories] = useState<string[]>([]);
  const [savingPrefs, setSavingPrefs] = useState(false);
  const [showSignOutConfirm, setShowSignOutConfirm] = useState(false);
  const [showCancelConfirm, setShowCancelConfirm] = useState(false);
  const [isSigningOut, setIsSigningOut] = useState(false);
  const [cancelLoading, setCancelLoading] = useState(false);
  const [reactivateLoading, setReactivateLoading] = useState(false);
  const [subError, setSubError] = useState("");
  const { startCheckout, loading: checkoutLoading } = useStripeCheckout();

  useEffect(() => {
    if (!user && !isSigningOut) router.push("/login");
  }, [user, isSigningOut, router]);

  useEffect(() => {
    if (!user?.id) return;
    apiFetch("/me")
      .then((r) => r.json())
      .then(setApiProfile)
      .catch(() => {
        // Profile will be empty — user can still edit from form defaults
      });
  }, [user?.id]);

  // Load subscription info
  useEffect(() => {
    if (!user?.id) return;
    setSubLoading(true);
    apiFetch("/stripe/subscription")
      .then((r) => r.json())
      .then((data) => setSubscription(data.subscription || null))
      .catch(() => setSubscription(null))
      .finally(() => setSubLoading(false));
  }, [user?.id]);

  useEffect(() => {
    if (profile?.categories_interest) {
      setCategories(profile.categories_interest);
    }
  }, [profile?.categories_interest]);

  const toggleCategory = (id: string) => {
    const next = categories.includes(id)
      ? categories.filter((c) => c !== id)
      : [...categories, id];
    setCategories(next);
  };

  const savePreferences = async () => {
    if (!user) return;
    setSavingPrefs(true);
    try {
      const supabase = createClient();
      await supabase
        .from("profiles")
        .update({ categories_interest: categories })
        .eq("id", user.id);
      await refreshProfile();
    } finally {
      setSavingPrefs(false);
    }
  };

  const handleCancel = async () => {
    setCancelLoading(true);
    setSubError("");
    try {
      const res = await apiFetch("/stripe/subscription/cancel", { method: "POST" });
      const data = await res.json();
      if (!res.ok) {
        setSubError(data.detail || "Error al cancelar la suscripción.");
        return;
      }
      setSubscription(data.subscription);
      setShowCancelConfirm(false);
    } catch {
      setSubError("Error de conexión. Inténtalo de nuevo.");
    } finally {
      setCancelLoading(false);
    }
  };

  const handleReactivate = async () => {
    setReactivateLoading(true);
    setSubError("");
    try {
      const res = await apiFetch("/stripe/subscription/reactivate", { method: "POST" });
      const data = await res.json();
      if (!res.ok) {
        setSubError(data.detail || "Error al reactivar la suscripción.");
        return;
      }
      setSubscription(data.subscription);
    } catch {
      setSubError("Error de conexión. Inténtalo de nuevo.");
    } finally {
      setReactivateLoading(false);
    }
  };

  const success = searchParams.get("success");
  const canceled = searchParams.get("canceled");

  if (!user) return null;

  const isPro = apiProfile?.plan === "pro" || apiProfile?.plan === "document";
  const isTrialing = subscription?.status === "trialing";
  const isCancelScheduled = subscription?.cancel_at_period_end === true;

  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      <ToolHeader title="Mi cuenta" />
      <main className="mx-auto max-w-4xl p-6">
        {success && (
          <div className="mb-4 rounded-lg bg-emerald-50 p-4 text-emerald-800">
            Pago completado correctamente.
          </div>
        )}
        {canceled && (
          <div className="mb-4 rounded-lg bg-amber-50 p-4 text-amber-800">
            Pago cancelado.
          </div>
        )}

        <div className="space-y-6">
          {/* User info card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-[#1A56DB] text-2xl font-bold text-white">
                {(profile?.name || user.email || "U")[0].toUpperCase()}
              </div>
              <div>
                <h2 className="font-semibold text-slate-800">
                  {profile?.name || "Usuario"}
                </h2>
                <p className="text-sm text-slate-500">{user.email}</p>
                <span
                  className={`mt-1 inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    isPro
                      ? "bg-gradient-to-r from-amber-400 to-orange-500 text-white"
                      : "bg-slate-200 text-slate-700"
                  }`}
                >
                  {isPro && (
                    <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                  )}
                  {isPro ? "PRO" : "GRATIS"}
                </span>
              </div>
            </div>
          </div>

          {/* Subscription management card (PRO users) */}
          {isPro && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-4">
                <svg className="h-5 w-5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <h2 className="font-semibold text-slate-800">Tu suscripción PRO</h2>
              </div>

              {subLoading ? (
                <p className="text-sm text-slate-500">Cargando información de suscripción...</p>
              ) : subscription ? (
                <div className="space-y-4">
                  {/* Status badges */}
                  <div className="flex flex-wrap items-center gap-2">
                    {isTrialing && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-xs font-semibold text-blue-700">
                        Periodo de prueba
                      </span>
                    )}
                    {isCancelScheduled && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-3 py-1 text-xs font-semibold text-red-700">
                        Cancelación programada
                      </span>
                    )}
                    {!isCancelScheduled && !isTrialing && subscription.status === "active" && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-100 px-3 py-1 text-xs font-semibold text-emerald-700">
                        Activa
                      </span>
                    )}
                  </div>

                  {/* Subscription details */}
                  <div className="rounded-xl bg-slate-50 p-4 space-y-2">
                    {isTrialing && subscription.trial_end && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Prueba gratis termina el</span>
                        <span className="font-medium text-slate-800">{formatDate(subscription.trial_end)}</span>
                      </div>
                    )}
                    {isTrialing && subscription.trial_end && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-slate-600">Dias restantes de prueba</span>
                        <span className="font-medium text-blue-700">{daysUntil(subscription.trial_end)} dias</span>
                      </div>
                    )}
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">
                        {isCancelScheduled ? "Acceso hasta" : "Proxima renovacion"}
                      </span>
                      <span className="font-medium text-slate-800">{formatDate(subscription.current_period_end)}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-slate-600">Precio</span>
                      <span className="font-medium text-slate-800">9,99 €/mes</span>
                    </div>
                  </div>

                  {/* Cancel scheduled notice */}
                  {isCancelScheduled && (
                    <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                      <p className="text-sm text-amber-800">
                        Tu suscripcion se cancelara el{" "}
                        <strong>{formatDate(subscription.current_period_end)}</strong>.
                        Seguiras teniendo acceso PRO hasta esa fecha.
                      </p>
                      <button
                        onClick={handleReactivate}
                        disabled={reactivateLoading}
                        className="mt-3 inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all disabled:opacity-70"
                      >
                        <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        {reactivateLoading ? "Reactivando..." : "Mantener PRO"}
                      </button>
                    </div>
                  )}

                  {/* Trial notice */}
                  {isTrialing && !isCancelScheduled && subscription.trial_end && (
                    <div className="rounded-xl border border-blue-200 bg-blue-50 p-4">
                      <p className="text-sm text-blue-800">
                        Estas en periodo de prueba gratuito. Se cobrara automaticamente{" "}
                        <strong>9,99 €</strong> el{" "}
                        <strong>{formatDate(subscription.trial_end)}</strong> si no cancelas antes.
                      </p>
                    </div>
                  )}

                  {subError && (
                    <div className="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">
                      {subError}
                    </div>
                  )}

                  {/* Cancel button */}
                  {!isCancelScheduled && (
                    <button
                      onClick={() => setShowCancelConfirm(true)}
                      className="text-sm text-slate-400 hover:text-red-500 transition-colors underline"
                    >
                      Cancelar suscripcion
                    </button>
                  )}
                </div>
              ) : (
                <p className="text-sm text-slate-500">
                  No se encontro informacion de suscripcion. Si acabas de suscribirte, espera unos segundos y recarga la pagina.
                </p>
              )}
            </div>
          )}

          {/* Upgrade card (free users) */}
          {!isPro && (
            <div className="rounded-2xl border-2 border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50 p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-2">
                <svg className="h-5 w-5 text-amber-500" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <h2 className="font-semibold text-slate-800">Hazte PRO</h2>
              </div>
              <p className="mb-1 text-sm text-slate-600">
                Consultas ilimitadas, documentos y alertas.
              </p>
              <p className="mb-4 text-sm font-medium text-amber-700">
                3 dias gratis, luego 9,99 €/mes. Cancela cuando quieras.
              </p>
              <button
                onClick={startCheckout}
                disabled={checkoutLoading}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 px-6 py-3 font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all disabled:opacity-70"
              >
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {checkoutLoading ? "Redirigiendo..." : "Probar 3 dias gratis"}
              </button>
            </div>
          )}

          {/* Preferences card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 font-semibold text-slate-800">Mis preferencias</h2>
            <p className="mb-4 text-sm text-slate-600">
              Categorias que te interesan (para personalizar tu experiencia)
            </p>
            <div className="flex flex-wrap gap-2">
              {CATEGORIES.map((c) => (
                <label
                  key={c.id}
                  className="flex cursor-pointer items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm"
                >
                  <input
                    type="checkbox"
                    checked={categories.includes(c.id)}
                    onChange={() => toggleCategory(c.id)}
                    className="rounded border-slate-300"
                  />
                  <span>{c.icon}</span>
                  <span>{c.label}</span>
                </label>
              ))}
            </div>
            <button
              onClick={savePreferences}
              disabled={savingPrefs}
              className="mt-4 rounded-xl border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
            >
              {savingPrefs ? "Guardando..." : "Guardar preferencias"}
            </button>
          </div>

          {/* Sign out button */}
          <button
            onClick={() => setShowSignOutConfirm(true)}
            className="w-full rounded-xl border border-red-200 bg-red-50 py-3 font-medium text-red-700 hover:bg-red-100"
          >
            Cerrar sesion
          </button>
        </div>

        <p className="mt-8 text-sm text-slate-500">
          Tramitup ofrece informacion basada en normativa publica. No prestamos
          asesoramiento juridico.
        </p>
      </main>

      {/* Cancel subscription confirmation modal */}
      {showCancelConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-red-100 text-xl">
              ⚠️
            </div>
            <h3 className="text-lg font-semibold text-slate-800">¿Cancelar suscripcion?</h3>
            <p className="mt-2 text-sm text-slate-600">
              {isTrialing
                ? "Perderas el acceso a las funciones PRO cuando termine tu periodo de prueba. No se te cobrara nada."
                : "Seguiras teniendo acceso PRO hasta el final de tu periodo de facturacion actual. Despues pasaras al plan gratuito."
              }
            </p>
            <div className="mt-2 rounded-lg bg-slate-50 p-3">
              <p className="text-xs text-slate-500">
                Acceso PRO hasta:{" "}
                <strong className="text-slate-700">
                  {subscription?.current_period_end
                    ? formatDate(subscription.current_period_end)
                    : "—"}
                </strong>
              </p>
            </div>
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setShowCancelConfirm(false)}
                className="flex-1 rounded-xl border border-slate-200 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Mantener PRO
              </button>
              <button
                onClick={handleCancel}
                disabled={cancelLoading}
                className="flex-1 rounded-xl bg-red-600 py-2.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-70"
              >
                {cancelLoading ? "Cancelando..." : "Confirmar cancelacion"}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Sign out confirmation modal */}
      {showSignOutConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
            <h3 className="text-lg font-semibold text-slate-800">¿Estas seguro?</h3>
            <p className="mt-2 text-sm text-slate-600">
              Se cerrara tu sesion y volveras a la pagina principal.
            </p>
            <div className="mt-6 flex gap-3">
              <button
                onClick={() => setShowSignOutConfirm(false)}
                className="flex-1 rounded-xl border border-slate-200 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
              >
                Cancelar
              </button>
              <button
                onClick={async () => {
                  setIsSigningOut(true);
                  try {
                    await signOut();
                    window.location.replace("/");
                  } catch {
                    window.location.replace("/");
                  }
                }}
                className="flex-1 rounded-xl bg-red-600 py-2.5 text-sm font-medium text-white hover:bg-red-700"
              >
                Cerrar sesion
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
