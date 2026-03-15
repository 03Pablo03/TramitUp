"use client";

import Link from "next/link";

export type AlertCardProps = {
  alert: {
    alert_id: string;
    description: string;
    deadline_date: string;
    law_reference: string | null;
    days_remaining: number;
    urgency: string;
    status: string;
  };
  onDismiss: () => void;
  onDelete: () => void;
};

function formatDate(iso: string): string {
  try {
    const d = new Date(iso);
    return d.toLocaleDateString("es-ES", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  } catch {
    return iso;
  }
}

export function AlertCard({ alert, onDismiss, onDelete }: AlertCardProps) {
  const isExpired = alert.status === "expired";
  const isDismissed = alert.status === "dismissed";
  const isPast = isExpired || isDismissed;

  const badgeClass =
    isPast
      ? "bg-slate-200 text-slate-600"
      : alert.days_remaining <= 3
        ? "bg-red-100 text-red-800"
        : alert.days_remaining <= 7
          ? "bg-amber-100 text-amber-800"
          : "bg-blue-100 text-blue-800";

  const emoji = isPast ? "⚫" : alert.days_remaining <= 3 ? "🔴" : alert.days_remaining <= 7 ? "🟡" : "🔵";

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div className="flex items-center gap-2">
          <span>{emoji}</span>
          <span
            className={`rounded-full px-2 py-0.5 text-xs font-medium ${badgeClass}`}
          >
            {isPast
              ? alert.status === "expired"
                ? "Vencida"
                : "Descartada"
              : `${alert.days_remaining} días`}
          </span>
        </div>
        <div className="flex gap-2">
          {alert.status === "active" && (
            <button
              onClick={onDismiss}
              className="text-xs text-slate-500 hover:text-slate-700"
            >
              Descartar
            </button>
          )}
          <button
            onClick={onDelete}
            className="text-xs text-red-500 hover:text-red-700"
          >
            Eliminar
          </button>
        </div>
      </div>
      <h3 className="font-medium text-slate-800">{alert.description}</h3>
      <p className="mt-1 text-sm text-slate-500">
        Vence: {formatDate(alert.deadline_date)}
      </p>
      {alert.law_reference && (
        <p className="mt-1 text-xs text-slate-400">{alert.law_reference}</p>
      )}
      <div className="mt-3">
        <Link
          href="/chat"
          className="text-sm text-[#1A56DB] hover:underline"
        >
          Ver conversación →
        </Link>
      </div>
    </div>
  );
}
