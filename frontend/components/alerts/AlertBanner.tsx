"use client";

import { useState } from "react";
import { CreateAlertModal, type DetectedDeadline } from "./CreateAlertModal";

export type AlertBannerProps = {
  deadlines: DetectedDeadline[];
  conversationId?: string | null;
  hasAccess: boolean;
  onUpgradeRequired?: () => void;
  onAlertCreated?: () => void;
};

export function AlertBanner({
  deadlines,
  conversationId,
  hasAccess,
  onUpgradeRequired,
  onAlertCreated,
}: AlertBannerProps) {
  const [showModal, setShowModal] = useState(false);
  const [selectedDeadline, setSelectedDeadline] = useState<DetectedDeadline | null>(null);
  const [showInfo, setShowInfo] = useState(false);

  if (!deadlines?.length) return null;

  const first = deadlines[0];
  // Calculate urgency locally from days (internal, not shown to user)
  const calcUrgency = (days: number) => 
    days < 10 ? "high" : days <= 30 ? "medium" : "low";
  const firstUrgency = calcUrgency(first.days);
  
  const urgencyClass =
    firstUrgency === "high"
      ? "border-l-amber-500 bg-amber-50"
      : firstUrgency === "medium"
        ? "border-l-amber-400 bg-amber-50/50"
        : "border-l-blue-400 bg-blue-50/50";

  const handleCreate = (d: DetectedDeadline) => {
    if (!hasAccess) {
      onUpgradeRequired?.();
      return;
    }
    setSelectedDeadline(d);
    setShowModal(true);
  };

  return (
    <>
      <div
        className={`mt-3 rounded-lg border-l-4 ${urgencyClass} p-3 text-sm text-slate-800`}
      >
        <div className="flex items-start justify-between gap-2">
          <div>
            <p className="font-medium">⏰ Plazo detectado</p>
            {deadlines.map((d, i) => (
              <div key={i} className="mt-1">
                <p className="text-slate-700">{d.description}</p>
                <p className="text-xs text-slate-500">{d.law_reference}</p>
              </div>
            ))}
          </div>
          <div className="flex shrink-0 flex-col gap-1">
            <button
              onClick={() => handleCreate(first)}
              className="rounded-lg border border-[#1A56DB] bg-[#1A56DB]/10 px-3 py-1.5 text-xs font-medium text-[#1A56DB] hover:bg-[#1A56DB]/20"
            >
              {hasAccess ? "★ Crear alerta (PRO)" : "★ Crear alerta (PRO)"}
            </button>
            <button
              onClick={() => setShowInfo(!showInfo)}
              className="text-xs text-slate-500 hover:text-slate-700"
            >
              ¿Qué es esto?
            </button>
          </div>
        </div>
        {showInfo && (
          <p className="mt-2 text-xs text-slate-600">
            Tramitup puede avisarte por email antes de que venza un plazo legal.
            Las alertas son exclusivas del plan PRO.
          </p>
        )}
      </div>
      {selectedDeadline && (
        <CreateAlertModal
          open={showModal}
          onClose={() => {
            setShowModal(false);
            setSelectedDeadline(null);
          }}
          onCreated={onAlertCreated ?? (() => {})}
          deadline={selectedDeadline}
          conversationId={conversationId}
          hasAccess={hasAccess}
          onUpgradeRequired={onUpgradeRequired}
        />
      )}
    </>
  );
}
