"use client";

import { FileText, Lightbulb } from "@/lib/icons";

interface WizardStepDocumentProps {
  title: string;
  content: string | null;
  loading: boolean;
  legalNotice?: string;
  onContinue: () => void;
}

export function WizardStepDocument({
  title,
  content,
  loading,
  legalNotice,
  onContinue,
}: WizardStepDocumentProps) {
  const handleCopy = () => {
    if (content) {
      navigator.clipboard.writeText(content);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-500 to-teal-500 shadow-lg shadow-emerald-500/20">
          <svg className="h-8 w-8 animate-spin text-white" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        </div>
        <h3 className="text-lg font-semibold text-slate-800">Generando documento...</h3>
        <p className="mt-2 text-sm text-slate-500">
          Redactando tu documento con los datos del caso y la normativa aplicable.
        </p>
      </div>
    );
  }

  if (!content) return null;

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-emerald-100 bg-emerald-50/50 p-1">
        <div className="flex items-center justify-between px-4 py-2">
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-emerald-600" />
            <span className="text-sm font-semibold text-emerald-800">{title}</span>
          </div>
          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-200 bg-white px-3 py-1.5 text-xs font-medium text-emerald-700 transition-colors hover:bg-emerald-50"
          >
            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.666 3.888A2.25 2.25 0 0013.5 2.25h-3c-1.03 0-1.9.693-2.166 1.638m7.332 0c.055.194.084.4.084.612v0a.75.75 0 01-.75.75H9.75a.75.75 0 01-.75-.75v0c0-.212.03-.418.084-.612m7.332 0c.646.049 1.288.11 1.927.184 1.1.128 1.907 1.077 1.907 2.185V19.5a2.25 2.25 0 01-2.25 2.25H6.75A2.25 2.25 0 014.5 19.5V6.257c0-1.108.806-2.057 1.907-2.185a48.208 48.208 0 011.927-.184" />
            </svg>
            Copiar
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-slate-700">
          {content}
        </pre>
      </div>

      <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
        <div className="flex gap-3">
          <Lightbulb className="h-5 w-5 shrink-0 text-blue-500" />
          <div className="text-xs text-blue-700 space-y-1">
            <p className="font-medium">Antes de enviar el documento:</p>
            <ul className="ml-4 list-disc space-y-0.5">
              <li>Completa los campos marcados entre corchetes [...]</li>
              <li>Revisa que todos los datos sean correctos</li>
              <li>Firma el documento antes de enviarlo</li>
            </ul>
          </div>
        </div>
      </div>

      {legalNotice && (
        <p className="text-[10px] text-slate-400 text-center">{legalNotice}</p>
      )}

      <button
        onClick={onContinue}
        className="w-full rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
      >
        Continuar — Ver instrucciones
      </button>
    </div>
  );
}
