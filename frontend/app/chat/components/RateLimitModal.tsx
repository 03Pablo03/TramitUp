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
            className="flex-1 inline-flex items-center justify-center gap-1.5 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 py-2.5 font-bold text-white hover:from-amber-500 hover:to-orange-600 disabled:opacity-70 shadow-md"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            Probar 3 días gratis
          </button>
        </div>
      </div>
    </div>
  );
}
