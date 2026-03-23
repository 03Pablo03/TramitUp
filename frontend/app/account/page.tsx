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

export default function AccountPage() {
  const { user, profile, signOut, refreshProfile } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [apiProfile, setApiProfile] = useState<ApiProfile | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [savingPrefs, setSavingPrefs] = useState(false);
  const [showSignOutConfirm, setShowSignOutConfirm] = useState(false);
  const [isSigningOut, setIsSigningOut] = useState(false);
  const { startCheckout, loading: checkoutLoading } = useStripeCheckout();

  useEffect(() => {
    if (!user && !isSigningOut) router.push("/login");
  }, [user, isSigningOut, router]);

  useEffect(() => {
    if (!user?.id) return;
    apiFetch("/me")
      .then((r) => r.json())
      .then(setApiProfile)
      .catch((error) => {
        console.warn("Error loading user profile:", error);
      });
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

  const success = searchParams.get("success");
  const canceled = searchParams.get("canceled");

  if (!user) return null;

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
                  className={`mt-1 inline-block rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    apiProfile?.plan === "pro"
                      ? "bg-[#1A56DB] text-white"
                      : "bg-slate-200 text-slate-700"
                  }`}
                >
                  {apiProfile?.plan === "pro" ? "PRO" : "GRATIS"}
                </span>
              </div>
            </div>
          </div>

          {apiProfile?.plan !== "pro" && (
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
                3 días gratis, luego 9,99 €/mes. Cancela cuando quieras.
              </p>
              <button
                onClick={startCheckout}
                disabled={checkoutLoading}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 px-6 py-3 font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all disabled:opacity-70"
              >
                <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                {checkoutLoading ? "Redirigiendo..." : "Probar 3 días gratis"}
              </button>
            </div>
          )}

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 font-semibold text-slate-800">Mis preferencias</h2>
            <p className="mb-4 text-sm text-slate-600">
              Categorías que te interesan (para personalizar tu experiencia)
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

          <button
            onClick={() => setShowSignOutConfirm(true)}
            className="w-full rounded-xl border border-red-200 bg-red-50 py-3 font-medium text-red-700 hover:bg-red-100"
          >
            Cerrar sesión
          </button>
        </div>

        <p className="mt-8 text-sm text-slate-500">
          Tramitup ofrece información basada en normativa pública. No prestamos
          asesoramiento jurídico.
        </p>
      </main>

      {showSignOutConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-sm rounded-2xl bg-white p-6 shadow-xl">
            <h3 className="text-lg font-semibold text-slate-800">¿Estás seguro?</h3>
            <p className="mt-2 text-sm text-slate-600">
              Se cerrará tu sesión y volverás a la página principal.
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
                Cerrar sesión
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
