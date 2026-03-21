"use client";

import { useStripeCheckout } from "@/hooks/useStripeCheckout";

type RateLimitModalProps = {
  open: boolean;
  onClose: () => void;
  message?: string;
};

export function RateLimitModal({ open, onClose, message }: RateLimitModalProps) {
  const { startCheckout, loading } = useStripeCheckout();
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="mx-4 max-w-sm rounded-2xl bg-white p-6 shadow-xl">
        <h3 className="mb-2 text-lg font-semibold text-slate-800">
          Límite alcanzado
        </h3>
        <p className="mb-6 text-slate-600">
          {message ||
            "Has usado tus 2 consultas gratuitas de hoy. Con PRO tienes consultas ilimitadas."}
        </p>
        <div className="flex gap-2">
          <button
            onClick={onClose}
            className="flex-1 rounded-lg border border-slate-300 py-2 text-slate-700 hover:bg-slate-50"
          >
            Cerrar
          </button>
          <button
            onClick={startCheckout}
            disabled={loading}
            className="flex-1 inline-flex items-center justify-center gap-1.5 rounded-lg bg-gradient-to-r from-[var(--primary)] to-blue-600 py-2.5 font-bold text-white hover:from-[var(--primary-dark)] hover:to-blue-700 disabled:opacity-70"
          >
            ★ Hazte PRO
          </button>
        </div>
      </div>
    </div>
  );
}
