"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";
import { Eye, FileText } from "@/lib/icons";

type Section = {
  type: string;
  label: string;
  content: string;
};

type PreviewData = {
  title: string;
  document_type: string;
  sections: Section[];
  disclaimer: string;
};

interface DocumentPreviewProps {
  conversationId: string;
  hasAccess: boolean;
  onAccessRequired?: () => void;
  onGenerate: () => void;
}

export function DocumentPreview({
  conversationId,
  hasAccess,
  onAccessRequired,
  onGenerate,
}: DocumentPreviewProps) {
  const [preview, setPreview] = useState<PreviewData | null>(null);
  const [editedSections, setEditedSections] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const handlePreview = async () => {
    if (!hasAccess) {
      onAccessRequired?.();
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/document/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ conversation_id: conversationId }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.detail || "Error al generar preview");
        setLoading(false);
        return;
      }
      setPreview(data.data);
      setEditedSections({});
      setIsOpen(true);
    } catch {
      setError("Error de conexión");
    } finally {
      setLoading(false);
    }
  };

  const handleSectionEdit = (index: number, value: string) => {
    setEditedSections((prev) => ({ ...prev, [index]: value }));
  };

  const handleCopyAll = () => {
    if (!preview) return;
    const text = preview.sections
      .map((s, i) => editedSections[i] ?? s.content)
      .join("\n\n");
    navigator.clipboard.writeText(text);
  };

  if (!isOpen) {
    return (
      <button
        onClick={handlePreview}
        disabled={loading}
        className="inline-flex items-center gap-2 rounded-lg border border-violet-200 bg-violet-50 px-3 py-2 text-sm font-medium text-violet-700 transition-all hover:bg-violet-100 hover:border-violet-300 disabled:opacity-50"
      >
        {loading ? (
          <>
            <span className="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-violet-400 border-t-transparent" />
            Generando preview...
          </>
        ) : (
          <>
            <Eye className="h-4 w-4" /> Vista previa del documento
          </>
        )}
      </button>
    );
  }

  if (!preview) return null;

  const SECTION_STYLES: Record<string, string> = {
    header: "bg-slate-50 border-slate-200",
    subject: "bg-blue-50 border-blue-200",
    body: "bg-white border-slate-200",
    signature: "bg-slate-50 border-slate-200",
  };

  return (
    <div className="mt-3 rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 bg-gradient-to-r from-violet-50 to-blue-50 px-4 py-3">
        <div className="flex items-center gap-2">
          <FileText className="h-5 w-5 text-violet-600" />
          <div>
            <h3 className="text-sm font-semibold text-slate-800">{preview.title}</h3>
            <p className="text-[10px] text-slate-500">Puedes editar el contenido antes de generar</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopyAll}
            className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50"
          >
            Copiar todo
          </button>
          <button
            onClick={() => setIsOpen(false)}
            className="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
          >
            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      {/* Sections */}
      <div className="max-h-[400px] overflow-y-auto p-4 space-y-3">
        {preview.sections.map((section, i) => (
          <div
            key={i}
            className={`rounded-lg border p-3 ${SECTION_STYLES[section.type] || "bg-white border-slate-200"}`}
          >
            <div className="mb-1.5 flex items-center justify-between">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                {section.label}
              </span>
            </div>
            <textarea
              value={editedSections[i] ?? section.content}
              onChange={(e) => handleSectionEdit(i, e.target.value)}
              className="w-full resize-none rounded border-0 bg-transparent p-0 text-sm text-slate-700 leading-relaxed focus:outline-none focus:ring-0"
              rows={Math.max(2, (editedSections[i] ?? section.content).split("\n").length)}
            />
          </div>
        ))}
      </div>

      {/* Disclaimer */}
      {preview.disclaimer && (
        <div className="border-t border-slate-100 px-4 py-2">
          <p className="text-[10px] text-slate-400 text-center">{preview.disclaimer}</p>
        </div>
      )}

      {/* Actions */}
      <div className="border-t border-slate-200 bg-slate-50 px-4 py-3 flex items-center gap-3">
        <button
          onClick={onGenerate}
          className="flex-1 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-2.5 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
        >
          Generar PDF y Word
        </button>
        <button
          onClick={() => setIsOpen(false)}
          className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-600 hover:bg-slate-50"
        >
          Cerrar
        </button>
      </div>

      {error && (
        <div className="border-t border-red-100 bg-red-50 px-4 py-2">
          <p className="text-xs text-red-600">{error}</p>
        </div>
      )}
    </div>
  );
}
