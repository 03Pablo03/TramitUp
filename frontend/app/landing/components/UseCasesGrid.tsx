"use client";

import Link from "next/link";
import { Plane, Lightbulb, Briefcase, Home, Landmark, ClipboardList } from "@/lib/icons";
import { FadeIn } from "@/components/ui/FadeIn";
import type { ComponentType } from "react";
import type { LucideProps } from "lucide-react";

const cases: {
  icon: ComponentType<LucideProps>;
  title: string;
  desc: string;
  law: string;
}[] = [
  {
    icon: Plane,
    title: "Vuelo cancelado",
    desc: "Iberia me canceló el vuelo. ¿Qué me corresponde?",
    law: "EU 261/2004 · Hasta 600€",
  },
  {
    icon: Lightbulb,
    title: "Factura incorrecta",
    desc: "Endesa me cobró el doble este mes.",
    law: "Ley 24/2013 · CNMC",
  },
  {
    icon: Briefcase,
    title: "Despido",
    desc: "¿Está bien calculado el finiquito?",
    law: "Estatuto Trabajadores",
  },
  {
    icon: Home,
    title: "Fianza no devuelta",
    desc: "El casero no devuelve la fianza.",
    law: "LAU 29/1994 · 1 mes",
  },
  {
    icon: Landmark,
    title: "Multa de tráfico",
    desc: "Creo que es injusta. ¿Puedo recurrirla?",
    law: "RDL 6/2015 · 20 días",
  },
  {
    icon: ClipboardList,
    title: "Hacienda",
    desc: "La renta me sale a pagar pero hay un error.",
    law: "Ley 58/2003 LGT",
  },
];

export function UseCasesGrid() {
  return (
    <FadeIn>
      <section className="bg-[var(--surface)] px-4 py-20">
        <div className="mx-auto max-w-4xl">
          <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            Casos de uso
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
            Situaciones reales que Tramitup puede ayudarte a resolver
          </p>

          {/* Compact list, 2 columns on desktop */}
          <div className="mt-12 grid gap-3 sm:grid-cols-2">
            {cases.map((c) => {
              const Icon = c.icon;
              return (
                <Link
                  key={c.title}
                  href="/login"
                  className="group flex items-center gap-4 rounded-xl border border-[var(--border)] bg-white px-5 py-4 transition-all duration-200 hover:border-[var(--primary)]/30 hover:shadow-sm"
                >
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-[var(--primary)]/10">
                    <Icon className="h-5 w-5 text-[var(--primary)]" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-baseline justify-between gap-2">
                      <h3 className="font-semibold text-[var(--text-dark)] truncate">
                        {c.title}
                      </h3>
                      <span className="shrink-0 text-[10px] font-medium text-[var(--primary)]">
                        {c.law}
                      </span>
                    </div>
                    <p className="mt-0.5 text-sm text-[var(--text-muted)] truncate">
                      {c.desc}
                    </p>
                  </div>
                </Link>
              );
            })}
          </div>
        </div>
      </section>
    </FadeIn>
  );
}
