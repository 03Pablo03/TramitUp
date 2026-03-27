"use client";

import Link from "next/link";
import { Star } from "@/lib/icons";

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
              className="inline-flex items-center rounded-xl bg-[var(--primary)] px-8 py-4 text-lg font-semibold text-white shadow-lg transition-colors hover:bg-[var(--primary-dark)] active:scale-[0.98]"
            >
              Empezar gratis
            </Link>
            <a
              href="#como-funciona"
              className="inline-flex items-center rounded-xl border-2 border-white/60 bg-white/10 px-8 py-4 text-lg font-semibold text-white backdrop-blur-sm transition-colors hover:bg-white/20 active:scale-[0.98]"
            >
              Ver cómo funciona
            </a>
          </div>
          <p className="mt-8 flex items-center gap-1 text-sm font-bold text-white drop-shadow-md">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star key={i} className="h-4 w-4 fill-amber-400 text-amber-400" />
            ))}
            <span className="ml-1">Más de 2.400 ciudadanos ya han resuelto sus trámites</span>
          </p>
        </div>
        <div className="relative flex items-center justify-center">
          <div className="w-full max-w-md rounded-2xl border border-white/20 bg-white/[0.07] backdrop-blur-md p-5 shadow-xl shadow-black/10">
            {/* Chat header */}
            <div className="flex items-center gap-2 border-b border-white/10 pb-3 mb-4">
              <div className="h-8 w-8 rounded-full bg-[var(--primary)] flex items-center justify-center text-xs font-bold text-white">T</div>
              <div>
                <p className="text-sm font-semibold text-white">TramitUp</p>
                <p className="text-[10px] text-emerald-400">En linea</p>
              </div>
            </div>

            {/* Messages */}
            <div className="space-y-3 text-sm">
              {/* User bubble - right aligned */}
              <div className="flex justify-end">
                <div className="max-w-[85%] rounded-2xl rounded-br-md bg-[var(--primary)] px-4 py-2.5 text-white shadow-sm">
                  <p className="leading-relaxed">
                    Iberia me canceló el vuelo Madrid-Barcelona del 15 de enero. ¿Qué me corresponde?
                  </p>
                  <p className="mt-1 text-right text-[10px] text-white/50">14:32</p>
                </div>
              </div>

              {/* Bot bubble - left aligned */}
              <div className="flex justify-start gap-2">
                <div className="h-6 w-6 shrink-0 rounded-full bg-[var(--primary)]/20 flex items-center justify-center mt-1">
                  <span className="text-[10px] font-bold text-white">T</span>
                </div>
                <div className="max-w-[85%] rounded-2xl rounded-bl-md bg-white/95 px-4 py-2.5 shadow-sm">
                  <p className="leading-relaxed text-stone-800">
                    Según el <span className="font-semibold text-[var(--primary)]">Reglamento UE 261/2004</span>, en vuelos cancelados con menos de 14 días de antelación tienes derecho a compensación:
                  </p>
                  <ul className="mt-2 space-y-1 text-stone-700">
                    <li className="flex items-center gap-1.5"><span className="h-1.5 w-1.5 rounded-full bg-[var(--primary)]" />Trayecto corto: <span className="font-semibold">250€</span></li>
                    <li className="flex items-center gap-1.5"><span className="h-1.5 w-1.5 rounded-full bg-[var(--primary)]" />Trayecto medio: <span className="font-semibold">400€</span></li>
                    <li className="flex items-center gap-1.5"><span className="h-1.5 w-1.5 rounded-full bg-[var(--primary)]" />Trayecto largo: <span className="font-semibold">600€</span></li>
                  </ul>
                  <p className="mt-1 text-right text-[10px] text-stone-400">14:32</p>
                </div>
              </div>

              {/* Typing indicator */}
              <div className="flex justify-start gap-2">
                <div className="h-6 w-6 shrink-0 rounded-full bg-[var(--primary)]/20 flex items-center justify-center">
                  <span className="text-[10px] font-bold text-white">T</span>
                </div>
                <div className="rounded-2xl rounded-bl-md bg-white/95 px-4 py-3 shadow-sm">
                  <div className="flex gap-1">
                    <span className="h-1.5 w-1.5 rounded-full bg-stone-400 animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="h-1.5 w-1.5 rounded-full bg-stone-400 animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="h-1.5 w-1.5 rounded-full bg-stone-400 animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
