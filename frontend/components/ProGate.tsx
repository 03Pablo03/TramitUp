"use client";

import Link from "next/link";

interface ProGateProps {
  feature: string;
  description: string;
  icon?: string;
}

export function ProGate({ feature, description, icon = "🔒" }: ProGateProps) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 text-4xl shadow-lg">
          {icon}
        </div>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-100 px-3 py-1 text-xs font-bold text-amber-700 mb-4">
          ★ Exclusivo PRO
        </span>
        <h2 className="mt-2 text-2xl font-bold text-slate-900">{feature}</h2>
        <p className="mt-3 text-slate-500">{description}</p>

        <div className="mt-8 space-y-3">
          <Link
            href="/pricing"
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 py-3.5 font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all"
          >
            ★ Ver planes PRO
          </Link>
          <Link
            href="/chat"
            className="flex w-full items-center justify-center rounded-xl border border-slate-200 py-3 text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors"
          >
            ← Volver al chat
          </Link>
        </div>

        <p className="mt-6 text-xs text-slate-400">
          ¿Ya tienes PRO?{" "}
          <Link href="/account" className="underline hover:text-slate-600">
            Comprueba tu cuenta
          </Link>
        </p>
      </div>
    </div>
  );
}
