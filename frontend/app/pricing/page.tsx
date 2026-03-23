"use client";

import { useRouter } from "next/navigation";
import { LandingNav } from "../landing/components/LandingNav";
import { Footer } from "../landing/components/Footer";
import { useAuth } from "@/context/AuthContext";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";

const plans = [
  {
    name: "Gratis",
    price: "0",
    period: "€",
    features: ["2 consultas al día", "Información basada en normativa real", "Acceso a todos los temas"],
    notIncluded: ["Generación de modelos de escritos", "Alertas de plazos"],
    cta: "Empezar gratis",
    primary: false,
    popular: false,
  },
  {
    name: "PRO",
    price: "9,99",
    period: "€/mes",
    trial: "3 días gratis",
    features: ["Consultas ilimitadas", "Modelos de escritos ilimitados", "Alertas de plazos legales", "Historial completo"],
    notIncluded: [],
    cta: "Probar 3 días gratis",
    primary: true,
    popular: true,
  },
];

export default function PricingPage() {
  const { user } = useAuth();
  const router = useRouter();
  const { startCheckout, loading } = useStripeCheckout();

  const handleProClick = () => {
    if (user) {
      startCheckout();
    } else {
      router.push("/login");
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <LandingNav />
      <main className="mx-auto max-w-6xl px-4 py-16">
        <h1 className="font-display text-center text-4xl font-bold text-[var(--text-dark)]">
          Precios
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
          Empieza gratis. Prueba PRO 3 días sin compromiso.
        </p>
        <div className="mt-16 mx-auto max-w-2xl grid gap-8 md:grid-cols-2">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border-2 p-8 ${
                plan.popular
                  ? "border-amber-400 bg-gradient-to-br from-amber-50/50 to-orange-50/50 shadow-lg"
                  : "border-[var(--border)] bg-white"
              }`}
            >
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 px-4 py-1 text-sm font-semibold text-white shadow-md">
                  Más popular
                </span>
              )}
              <h2 className="font-display text-xl font-semibold text-[var(--text-dark)]">
                {plan.name}
              </h2>
              <p className="mt-2">
                <span className="text-4xl font-bold text-[var(--text-dark)]">{plan.price}</span>
                <span className="text-[var(--text-muted)]">{plan.period}</span>
              </p>
              {plan.trial && (
                <p className="mt-1 text-sm font-medium text-amber-600">
                  {plan.trial} — luego se cobra automáticamente
                </p>
              )}
              <ul className="mt-6 space-y-3">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-[var(--text-body)]">
                    <span className="text-[var(--accent)]">✓</span> {f}
                  </li>
                ))}
                {plan.notIncluded.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-[var(--text-muted)]">
                    <span>✗</span> {f}
                  </li>
                ))}
              </ul>
              {plan.primary ? (
                <button
                  onClick={handleProClick}
                  disabled={loading}
                  className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-all bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-lg hover:from-amber-500 hover:to-orange-600 disabled:opacity-70"
                >
                  <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  {plan.cta}
                </button>
              ) : (
                <button
                  onClick={() => router.push("/login")}
                  className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-colors border border-[var(--border)] text-[var(--text-body)] hover:bg-[var(--surface)]"
                >
                  {plan.cta}
                </button>
              )}
              {plan.primary && (
                <p className="mt-3 text-center text-xs text-slate-400">
                  Se requiere tarjeta. Si no cancelas, se cobra automáticamente tras el periodo de prueba.
                </p>
              )}
            </div>
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}
