"use client";

import { FadeIn } from "@/components/ui/FadeIn";
import { Scale } from "@/lib/icons";

export function ProblemSection() {
  return (
    <FadeIn>
      <section className="bg-[var(--surface)] px-4 py-16">
        <div className="mx-auto flex max-w-4xl items-start gap-6">
          <div className="hidden sm:flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[var(--primary)]/10">
            <Scale className="h-6 w-6 text-[var(--primary)]" />
          </div>
          <div>
            <p className="text-lg font-semibold leading-relaxed text-[var(--text-dark)]">
              La normativa existe para protegerte, pero nadie te la explica.
            </p>
            <p className="mt-2 text-[var(--text-body)] leading-relaxed">
              Tramitup es un servicio especializado en la normativa española que te explica
              exactamente qué dice la ley en tu caso — sin tecnicismos, con referencias reales.
            </p>
          </div>
        </div>
      </section>
    </FadeIn>
  );
}
