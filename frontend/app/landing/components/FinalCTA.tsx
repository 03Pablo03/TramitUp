"use client";

import Link from "next/link";
import { FadeIn } from "@/components/ui/FadeIn";

export function FinalCTA() {
  return (
    <FadeIn>
      <section className="bg-white px-4 py-24">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-display text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            Empieza gratis. Sin tarjeta.
          </h2>
          <p className="mt-4 text-xl text-[var(--text-body)]">
            2 consultas gratuitas al día para siempre. Actualiza a PRO cuando lo
            necesites.
          </p>
          <Link
            href="/login"
            className="mt-8 inline-flex rounded-xl bg-[var(--primary)] px-10 py-4 text-lg font-semibold text-white transition-transform hover:bg-[var(--primary-dark)] active:scale-[0.98]"
          >
            Crear cuenta gratis →
          </Link>
          <p className="mt-6 text-sm text-[var(--text-muted)]">
            Ya somos más de 2.400 ciudadanos informados
          </p>
        </div>
      </section>
    </FadeIn>
  );
}
