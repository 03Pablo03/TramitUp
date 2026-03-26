"use client";

import { useState } from "react";

export type DetectedDeadline = {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
};

export type CreateAlertModalProps = {
  open: boolean;
  onClose: () => void;
  onCreated: () => void;
  deadline: DetectedDeadline;
  conversationId?: string | null;
  hasAccess: boolean;
  onUpgradeRequired?: () => void;
};

function addBusinessDays(from: Date, days: number): Date {
  const d = new Date(from);
  let remaining = days;
  while (remaining > 0) {
    d.setDate(d.getDate() + 1);
    if (d.getDay() !== 0 && d.getDay() !== 6) remaining--;
  }
  return d;
}

function formatDateISO(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export function CreateAlertModal({
  open,
  onClose,
  onCreated,
  deadline,
  conversationId,
  hasAccess,
  onUpgradeRequired,
}: CreateAlertModalProps) {
  const [description, setDescription] = useState(deadline.description);
  const [notify7, setNotify7] = useState(true);
  const [notify3, setNotify3] = useState(true);
  const [notify1, setNotify1] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  let defaultDeadline: string;
  if (deadline.reference_date) {
    const start = new Date(deadline.reference_date);
    const end = deadline.business_days
      ? addBusinessDays(start, deadline.days)
      : new Date(start.getTime() + deadline.days * 24 * 60 * 60 * 1000);
    defaultDeadline = formatDateISO(end);
  } else {
    const d = new Date();
    d.setDate(d.getDate() + deadline.days);
    defaultDeadline = formatDateISO(d);
  }
  const [deadlineDate, setDeadlineDate] = useState(defaultDeadline);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!hasAccess) {
      onUpgradeRequired?.();
      return;
    }
    setError("");
    setSaving(true);
    try {
      const { apiFetch } = await import("@/lib/api");
      await apiFetch("/alerts/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          description,
          deadline_date: deadlineDate,
          law_reference: deadline.law_reference || undefined,
          notify_days_before: [
            ...(notify7 ? [7] : []),
            ...(notify3 ? [3] : []),
            ...(notify1 ? [1] : []),
          ].sort((a, b) => b - a),
        }),
      });
      onCreated();
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al crear alerta");
    } finally {
      setSaving(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
        <h2 className="mb-4 text-lg font-semibold text-slate-800">Crear alerta de plazo</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Descripción
            </label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
              required
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Fecha límite
            </label>
            <input
              type="date"
              value={deadlineDate}
              onChange={(e) => setDeadlineDate(e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
              required
            />
          </div>
          <div>
            <span className="mb-2 block text-sm font-medium text-slate-700">
              Avisarme
            </span>
            <div className="flex gap-4">
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={notify7}
                  onChange={(e) => setNotify7(e.target.checked)}
                />
                7 días antes
              </label>
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={notify3}
                  onChange={(e) => setNotify3(e.target.checked)}
                />
                3 días antes
              </label>
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={notify1}
                  onChange={(e) => setNotify1(e.target.checked)}
                />
                1 día antes
              </label>
            </div>
          </div>
          {deadline.law_reference && (
            <p className="text-xs text-slate-500">
              Referencia legal: {deadline.law_reference}
            </p>
          )}
          {error && <p className="text-sm text-red-600">{error}</p>}
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={saving}
              className="rounded-lg bg-[#1A56DB] px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
            >
              {saving ? "Creando..." : "Crear alerta →"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
