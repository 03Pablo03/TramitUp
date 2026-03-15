"use client";

import { useState } from "react";
import { Alert } from "@/hooks/useAlerts";

type Props = {
  alerts: Alert[];
  onDismiss: (id: string) => void;
  onDelete: (id: string) => void;
};

const DAYS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"];
const MONTHS = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
];

function getUrgencyColor(urgency: string, status: string) {
  if (status !== "active") return "bg-slate-200 text-slate-500";
  if (urgency === "high") return "bg-red-100 text-red-700 border border-red-200";
  if (urgency === "medium") return "bg-orange-100 text-orange-700 border border-orange-200";
  return "bg-green-100 text-green-700 border border-green-200";
}

export function AlertCalendar({ alerts, onDismiss, onDelete }: Props) {
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth());
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);

  const firstDay = new Date(year, month, 1);
  // Monday-first: getDay() returns 0=Sun..6=Sat → shift
  const startOffset = (firstDay.getDay() + 6) % 7;
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const alertsByDay: Record<number, Alert[]> = {};
  for (const alert of alerts) {
    const d = new Date(alert.deadline_date + "T00:00:00");
    if (d.getFullYear() === year && d.getMonth() === month) {
      const day = d.getDate();
      if (!alertsByDay[day]) alertsByDay[day] = [];
      alertsByDay[day].push(alert);
    }
  }

  const cells: (number | null)[] = [
    ...Array(startOffset).fill(null),
    ...Array.from({ length: daysInMonth }, (_, i) => i + 1),
  ];
  const rows: (number | null)[][] = [];
  for (let i = 0; i < cells.length; i += 7) rows.push(cells.slice(i, i + 7));
  while (rows[rows.length - 1]?.length < 7) rows[rows.length - 1].push(null);

  const prevMonth = () => {
    if (month === 0) { setMonth(11); setYear(y => y - 1); }
    else setMonth(m => m - 1);
  };
  const nextMonth = () => {
    if (month === 11) { setMonth(0); setYear(y => y + 1); }
    else setMonth(m => m + 1);
  };

  const isToday = (day: number) =>
    day === today.getDate() && month === today.getMonth() && year === today.getFullYear();

  return (
    <div>
      {/* Navigation */}
      <div className="mb-4 flex items-center justify-between">
        <button
          onClick={prevMonth}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          ← Anterior
        </button>
        <h2 className="text-base font-semibold text-slate-800">
          {MONTHS[month]} {year}
        </h2>
        <button
          onClick={nextMonth}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
        >
          Siguiente →
        </button>
      </div>

      {/* Grid */}
      <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
        {/* Day headers */}
        <div className="grid grid-cols-7 border-b border-slate-200 bg-slate-50">
          {DAYS.map((d) => (
            <div key={d} className="py-2 text-center text-xs font-semibold uppercase tracking-wide text-slate-500">
              {d}
            </div>
          ))}
        </div>

        {/* Weeks */}
        {rows.map((row, ri) => (
          <div key={ri} className={`grid grid-cols-7 ${ri < rows.length - 1 ? "border-b border-slate-100" : ""}`}>
            {row.map((day, di) => (
              <div
                key={di}
                className={`min-h-[80px] p-1.5 ${di < 6 ? "border-r border-slate-100" : ""} ${
                  day ? "hover:bg-slate-50" : "bg-slate-50/50"
                }`}
              >
                {day && (
                  <>
                    <span
                      className={`mb-1 flex h-6 w-6 items-center justify-center rounded-full text-xs font-medium ${
                        isToday(day)
                          ? "bg-[#1A56DB] text-white"
                          : "text-slate-700"
                      }`}
                    >
                      {day}
                    </span>
                    <div className="space-y-0.5">
                      {(alertsByDay[day] || []).map((alert) => (
                        <button
                          key={alert.alert_id}
                          onClick={() => setSelectedAlert(alert)}
                          className={`w-full truncate rounded px-1 py-0.5 text-left text-[10px] font-medium leading-tight ${getUrgencyColor(alert.urgency, alert.status)}`}
                          title={alert.description}
                        >
                          {alert.description}
                        </button>
                      ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-slate-500">
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-2.5 w-2.5 rounded bg-red-100 border border-red-200"></span> Alta urgencia (≤3 días)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-2.5 w-2.5 rounded bg-orange-100 border border-orange-200"></span> Media urgencia (≤7 días)
        </span>
        <span className="flex items-center gap-1.5">
          <span className="inline-block h-2.5 w-2.5 rounded bg-green-100 border border-green-200"></span> Baja urgencia (&gt;7 días)
        </span>
      </div>

      {/* Detail popover */}
      {selectedAlert && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
            <h3 className="mb-1 text-base font-semibold text-slate-800">{selectedAlert.description}</h3>
            {selectedAlert.law_reference && (
              <p className="mb-2 text-xs text-slate-500">{selectedAlert.law_reference}</p>
            )}
            <p className="mb-1 text-sm text-slate-600">
              📅 Fecha límite: <span className="font-medium">{selectedAlert.deadline_date}</span>
            </p>
            <p className="mb-4 text-sm text-slate-600">
              ⏳ {selectedAlert.days_remaining > 0
                ? `${selectedAlert.days_remaining} días restantes`
                : "Vencida"}
            </p>
            <div className="flex gap-2">
              {selectedAlert.status === "active" && (
                <button
                  onClick={() => { onDismiss(selectedAlert.alert_id); setSelectedAlert(null); }}
                  className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-50"
                >
                  Descartar
                </button>
              )}
              <button
                onClick={() => { onDelete(selectedAlert.alert_id); setSelectedAlert(null); }}
                className="rounded-lg border border-red-200 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50"
              >
                Eliminar
              </button>
              <button
                onClick={() => setSelectedAlert(null)}
                className="ml-auto rounded-lg bg-[#1A56DB] px-3 py-1.5 text-sm font-medium text-white hover:bg-[#1545a8]"
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
