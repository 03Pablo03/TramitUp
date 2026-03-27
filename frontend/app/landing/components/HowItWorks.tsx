"use client";

import Link from "next/link";
import { MessageSquare, ClipboardList, CheckCircle } from "@/lib/icons";
import { FadeIn } from "@/components/ui/FadeIn";
import type { ComponentType } from "react";
import type { LucideProps } from "lucide-react";

interface Step {
  num: number;
  title: string;
  desc: string;
  icon: ComponentType<LucideProps>;
}

const steps: Step[] = [
  {
    num: 1,
    title: "Describe tu situación",
    desc: "Escribe con tus propias palabras. Sin formularios. Sin elegir categorías.",
    icon: MessageSquare,
  },
  {
    num: 2,
    title: "Entendemos la normativa",
    desc: "Identificamos la legislación aplicable y te explicamos tus opciones en lenguaje claro.",
    icon: ClipboardList,
  },
  {
    num: 3,
    title: "Obtienes lo que necesitas",
    desc: "Guía paso a paso, plazos importantes y modelo de escrito personalizado.",
    icon: CheckCircle,
  },
];

export function HowItWorks() {
  return (
    <section id="como-funciona" className="scroll-mt-20 bg-white px-4 py-20">
      <div className="mx-auto max-w-4xl">
        <FadeIn>
          <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
            Cómo funciona
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
            Tres pasos para entender tus derechos y actuar con información
          </p>

          {/* Timeline vertical */}
          <div className="mt-14 space-y-0">
            {steps.map((step, i) => {
              const Icon = step.icon;
              const isLast = i === steps.length - 1;
              return (
                <div key={step.num} className="flex gap-5">
                  {/* Left: number + line */}
                  <div className="flex flex-col items-center">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--primary)] text-sm font-bold text-white shadow-md shadow-blue-500/20">
                      {step.num}
                    </div>
                    {!isLast && (
                      <div className="w-px flex-1 bg-[var(--border)]" />
                    )}
                  </div>

                  {/* Right: content */}
                  <div className={`${isLast ? "pb-0" : "pb-10"}`}>
                    <div className="flex items-center gap-3">
                      <Icon className="h-5 w-5 text-[var(--primary)]" />
                      <h3 className="font-display text-lg font-semibold text-[var(--text-dark)]">
                        {step.title}
                      </h3>
                    </div>
                    <p className="mt-1.5 text-[var(--text-body)] leading-relaxed">
                      {step.desc}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-10 text-center">
            <Link
              href="/login"
              className="inline-flex rounded-xl bg-[var(--primary)] px-6 py-3 font-semibold text-white hover:bg-[var(--primary-dark)] active:scale-[0.98] transition-colors"
            >
              Empezar ahora
            </Link>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
