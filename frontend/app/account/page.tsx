"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { createClient } from "@/lib/supabase/client";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";

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
      <header className="border-b border-slate-200 bg-white px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <div className="flex items-center gap-6">
            <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
              TramitUp
            </span>
            <span className="text-sm text-slate-500">Mi cuenta</span>
          </div>
          <Link href="/chat" className="text-slate-600 hover:text-slate-800">
            Chat
          </Link>
        </div>
      </header>
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
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="mb-4 font-semibold text-slate-800">Hazte PRO</h2>
              <p className="mb-4 text-sm text-slate-600">
                Consultas ilimitadas, documentos y alertas por 9,99 €/mes.
              </p>
              <button
                onClick={startCheckout}
                disabled={checkoutLoading}
                className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-6 py-3 font-bold text-white shadow-lg hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all disabled:opacity-70"
              >
                <span className="text-amber-300">★</span>
                {checkoutLoading ? "Redirigiendo..." : "Hazte PRO — 9,99 €/mes"}
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
