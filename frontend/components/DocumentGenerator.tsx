"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { Bell, FileText, Star } from "@/lib/icons";
import { DocumentDownloadCard } from "./DocumentDownloadCard";

type DetectedDeadline = {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
};

export type DocumentGeneratorProps = {
  conversationId: string;
  hasAccess: boolean;
  onAccessRequired?: () => void;
  detectedDeadlines?: DetectedDeadline[];
};

type State = "idle" | "loading" | "success" | "error";

type SuccessResult = {
  document_id: string;
  pdf_url: string | null;
  docx_url: string | null;
  document_type: string;
  generated_at: string;
};

export function DocumentGenerator({
  conversationId,
  hasAccess,
  onAccessRequired,
  detectedDeadlines,
}: DocumentGeneratorProps) {
  const [state, setState] = useState<State>("idle");
  const [result, setResult] = useState<SuccessResult | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [alertsAdded, setAlertsAdded] = useState(0);

  const handleGenerate = async () => {
    if (!hasAccess) {
      onAccessRequired?.();
      return;
    }
    setState("loading");
    setErrorMessage("");
    try {
      const res = await apiFetch("/document/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          conversation_id: conversationId,
          format: "both",
        }),
      });
      const data = await res.json();
      if (!res.ok) {
        if (res.status === 403) {
          setErrorMessage("Necesitas plan PRO o desbloquear el documento");
          onAccessRequired?.();
        } else {
          setErrorMessage(data.detail || "Error al generar");
        }
        setState("error");
        return;
      }
      setResult(data);

      // Auto-create alerts for detected deadlines
      if (detectedDeadlines && detectedDeadlines.length > 0) {
        let added = 0;
        for (const deadline of detectedDeadlines) {
          try {
            const deadlineDate = new Date();
            deadlineDate.setDate(deadlineDate.getDate() + deadline.days);
            const dateStr = deadlineDate.toISOString().split("T")[0];
            await apiFetch("/alerts/create", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                conversation_id: conversationId,
                description: deadline.description,
                deadline_date: dateStr,
                law_reference: deadline.law_reference,
                notify_days_before: [1, 3, 7],
              }),
            });
            added++;
          } catch {
            // Silently ignore individual failures
          }
        }
        setAlertsAdded(added);
      }

      setState("success");
    } catch {
      setErrorMessage("Error de conexión");
      setState("error");
    }
  };

  const handleRefreshUrls = async () => {
    if (!result?.document_id) return;
    try {
      const res = await apiFetch(`/document/${result.document_id}/download`);
      const data = await res.json();
      if (res.ok && (data.pdf_url || data.docx_url)) {
        setResult((prev) =>
          prev
            ? {
                ...prev,
                pdf_url: data.pdf_url ?? prev.pdf_url,
                docx_url: data.docx_url ?? prev.docx_url,
              }
            : null
        );
      }
    } catch {
      /* ignore */
    }
  };

  if (state === "success" && result) {
    return (
      <div className="mt-3 space-y-2">
        <DocumentDownloadCard
          documentId={result.document_id}
          documentType={result.document_type}
          createdAt={result.generated_at}
          pdfUrl={result.pdf_url}
          docxUrl={result.docx_url}
          onRefreshUrls={handleRefreshUrls}
        />
        {alertsAdded > 0 && (
          <p className="flex items-center gap-1.5 text-xs text-green-600">
            <Bell className="h-3.5 w-3.5" /> Se han añadido {alertsAdded} {alertsAdded === 1 ? "alerta" : "alertas"} al calendario automáticamente.
          </p>
        )}
      </div>
    );
  }

  return (
    <div className="mt-2 flex flex-wrap items-center gap-2">
      {state === "idle" && hasAccess && (
        <button
          onClick={handleGenerate}
          className="inline-flex items-center gap-2 rounded-lg border border-[#1A56DB] bg-[#1A56DB]/5 px-3 py-2 text-sm font-medium text-[#1A56DB] hover:bg-[#1A56DB]/15"
        >
          <FileText className="h-4 w-4" /> Generar modelo de escrito
        </button>
      )}
      {state === "idle" && !hasAccess && (
        <button
          onClick={() => onAccessRequired?.()}
          className="inline-flex items-center gap-2 rounded-lg border-2 border-[#1A56DB] bg-[#1A56DB]/10 px-3 py-2 text-sm font-semibold text-[#1A56DB] hover:bg-[#1A56DB]/20"
        >
          <Star className="h-4 w-4" /> Hazte PRO para generar modelo de escrito
        </button>
      )}
      {state === "loading" && (
        <span className="flex items-center gap-2 text-sm text-slate-600">
          <span className="inline-block h-4 w-4 animate-spin rounded-full border-2 border-slate-400 border-t-transparent" />
          Preparando tu modelo...
        </span>
      )}
      {state === "error" && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-red-600">{errorMessage}</span>
          {hasAccess ? (
            <button
              onClick={handleGenerate}
              className="text-xs font-medium text-[#1A56DB] hover:underline"
            >
              Reintentar
            </button>
          ) : (
            <button
              onClick={() => onAccessRequired?.()}
              className="text-xs font-medium text-[#1A56DB] hover:underline"
            >
              Hazte PRO
            </button>
          )}
        </div>
      )}
    </div>
  );
}
