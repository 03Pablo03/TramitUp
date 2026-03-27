"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useStripeCheckout } from "@/hooks/useStripeCheckout";
import { Check, X, Star } from "@/lib/icons";
import { FadeIn } from "@/components/ui/FadeIn";

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
    trial: "3 días gratis",
    features: [
      "Consultas ilimitadas",
      "Modelos de escritos ilimitados",
      "Alertas de plazos legales",
      "Historial completo",
    ],
    notIncluded: [],
    cta: "Probar 3 días gratis",
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
      router.push("/login?redirect=" + encodeURIComponent("/pricing?checkout=pro"));
    }
  };

  return (
    <FadeIn>
      <section className="bg-white px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            Precios
          </h2>
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
                <h3 className="font-display text-xl font-semibold text-[var(--text-dark)]">
                  {plan.name}
                </h3>
                <p className="mt-2">
                  <span className="text-4xl font-bold text-[var(--text-dark)]">
                    {plan.price}
                  </span>
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
                      <Check className="h-4 w-4 text-[var(--accent)]" /> {f}
                    </li>
                  ))}
                  {plan.notIncluded.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-[var(--text-muted)]">
                      <X className="h-4 w-4 text-slate-300" /> {f}
                    </li>
                  ))}
                </ul>
                {plan.ctaPrimary ? (
                  <button
                    onClick={handleProClick}
                    disabled={loading}
                    className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-all active:scale-[0.98] bg-gradient-to-r from-amber-400 to-orange-500 text-white shadow-lg hover:from-amber-500 hover:to-orange-600 disabled:opacity-70"
                  >
                    <Star className="h-5 w-5 fill-current" />
                    {plan.cta}
                  </button>
                ) : (
                  <button
                    onClick={() => router.push("/login")}
                    className="mt-8 flex w-full items-center justify-center gap-2 rounded-xl py-3.5 font-bold transition-all active:scale-[0.98] border border-[var(--border)] text-[var(--text-body)] hover:bg-[var(--surface)]"
                  >
                    {plan.cta}
                  </button>
                )}
                {plan.ctaPrimary && (
                  <p className="mt-3 text-center text-xs text-slate-400">
                    Se requiere tarjeta. Si no cancelas, se cobra automáticamente tras el periodo de prueba.
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>
    </FadeIn>
  );
}
