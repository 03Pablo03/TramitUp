"use client";

import Link from "next/link";
import { Lock } from "@/lib/icons";
import type { ComponentType } from "react";
import type { LucideProps } from "lucide-react";

interface ProGateProps {
  feature: string;
  description: string;
  icon?: ComponentType<LucideProps>;
}

export function ProGate({ feature, description, icon: Icon = Lock }: ProGateProps) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 to-orange-500 text-white shadow-lg">
          <Icon className="h-10 w-10" />
        </div>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 px-3 py-1 text-xs font-bold text-white mb-4 shadow-sm">
          <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
          Exclusivo PRO
        </span>
        <h2 className="mt-2 text-2xl font-bold text-slate-900">{feature}</h2>
        <p className="mt-3 text-slate-500">{description}</p>

        <div className="mt-8 space-y-3">
          <Link
            href="/pricing"
            className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 py-3.5 font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            Probar 3 días gratis
          </Link>
          <p className="text-xs text-slate-400">
            Luego 9,99 €/mes. Cancela cuando quieras.
          </p>
          <Link
            href="/chat"
            className="flex w-full items-center justify-center gap-1.5 rounded-xl border border-slate-200 py-3 text-sm font-medium text-slate-600 hover:bg-slate-50 transition-colors"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            Volver al chat
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
