"use client";

import Link from "next/link";

export function Hero({ noBackground }: { noBackground?: boolean }) {
  return (
    <section className="relative overflow-hidden px-4 py-20 lg:py-28 min-h-screen flex items-center">
      {!noBackground && (
        <>
          <div
            className="absolute inset-0 -z-20 bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: "url(/SEO.png)" }}
          />
          <div className="absolute inset-0 -z-10 bg-gradient-to-r from-stone-900/50 via-stone-900/15 to-transparent" />
        </>
      )}

      <div className="relative z-10 mx-auto grid max-w-6xl gap-12 lg:grid-cols-2 lg:gap-16">
        <div className="flex flex-col justify-center">
          <h1 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl drop-shadow-lg">
            La burocracia española, explicada en humano.
          </h1>
          <p className="mt-6 max-w-xl text-lg font-medium text-stone-200 leading-relaxed drop-shadow-md">
            Describe tu situación y te explicamos qué dice la normativa, qué opciones
            contempla la ley y cómo proceder — sin tecnicismos.
          </p>
          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              href="/login"
              className="inline-flex items-center rounded-xl bg-[var(--primary)] px-8 py-4 text-lg font-semibold text-white shadow-lg transition-colors hover:bg-[var(--primary-dark)]"
            >
              Empezar gratis →
            </Link>
            <a
              href="#como-funciona"
              className="inline-flex items-center rounded-xl border-2 border-white/60 bg-white/10 px-8 py-4 text-lg font-semibold text-white backdrop-blur-sm transition-colors hover:bg-white/20"
            >
              Ver cómo funciona ↓
            </a>
          </div>
          <p className="mt-8 text-sm font-bold text-white drop-shadow-md">
            ★★★★★ Más de 2.400 ciudadanos ya han resuelto sus trámites
          </p>
        </div>
        <div className="relative flex items-center justify-center">
          <div className="w-full max-w-md rounded-2xl border border-white/20 bg-white/[0.07] backdrop-blur-md p-6 shadow-xl shadow-black/10">
            <div className="space-y-3 text-sm">
              <div className="rounded-xl bg-white/95 backdrop-blur-sm border border-stone-200/80 p-4 shadow-sm">
                <p className="font-bold text-stone-900">Usuario</p>
                <p className="mt-1 text-stone-800 leading-relaxed">
                  Iberia me canceló el vuelo Madrid-Barcelona del 15 de enero. ¿Qué me
                  corresponde?
                </p>
              </div>
              <div className="rounded-xl bg-amber-50/95 backdrop-blur-sm border border-amber-200/80 p-4 shadow-sm">
                <p className="font-bold text-[var(--primary)]">Tramitup</p>
                <p className="mt-1 text-stone-800 leading-relaxed">
                  Según el Reglamento UE 261/2004, en vuelos cancelados con menos de 14
                  días de antelación tienes derecho a compensación económica: 250€ en
                  trayectos cortos, 400€ en medios, 600€ en largos. Te explico los pasos
                  para reclamar...
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
