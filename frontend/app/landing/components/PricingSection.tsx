"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";

const plans = [
  {
    name: "Gratis",
    price: "0",
    period: "€",
    features: [
      "2 consultas al día",
      "Información basada en normativa real",
      "Acceso a todos los temas",
    ],
    notIncluded: ["Generación de modelos de escritos", "Alertas de plazos"],
    cta: "Empezar gratis",
    ctaPrimary: false,
    popular: false,
  },
  {
    name: "PRO",
    price: "9,99",
    period: "€/mes",
    features: [
      "Consultas ilimitadas",
      "Modelos de escritos ilimitados",
      "Alertas de plazos legales",
      "Historial completo",
    ],
    notIncluded: [],
    cta: "Probar PRO",
    ctaPrimary: true,
    popular: true,
  },
];

export function PricingSection() {
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
    <section className="bg-white px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
          Precios
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
          Empieza gratis. Actualiza cuando lo necesites.
        </p>
        <div className="mt-16 mx-auto max-w-2xl grid gap-8 md:grid-cols-2">
          {plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border-2 p-8 ${
                plan.popular
                  ? "border-[var(--primary)] bg-[var(--primary-light)]/20 shadow-lg"
                  : "border-[var(--border)] bg-white"
              }`}
            >
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-[var(--primary)] px-4 py-1 text-sm font-semibold text-white">
                  Más popular
                </span>
              )}
              <h3 className="font-display text-xl font-semibold text-[var(--text-dark)]">
                {plan.name}
              </h3>
              <p className="mt-2">
                <span className="text-4xl font-bold text-[var(--text-dark)]">
                  {plan.price}
                </span>
                <span className="text-[var(--text-muted)]">{plan.period}</span>
              </p>
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
              {plan.ctaPrimary ? (
                <button
                  onClick={handleProClick}
                  disabled={loading}
                  className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-colors bg-gradient-to-r from-[var(--primary)] to-blue-600 text-white shadow-lg hover:from-[var(--primary-dark)] hover:to-blue-700 disabled:opacity-70"
                >
                  <span className="text-amber-300">★</span>
                  Hazte PRO
                </button>
              ) : (
                <button
                  onClick={() => router.push("/login")}
                  className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-colors border border-[var(--border)] text-[var(--text-body)] hover:bg-[var(--surface)]"
                >
                  {plan.cta}
                </button>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
