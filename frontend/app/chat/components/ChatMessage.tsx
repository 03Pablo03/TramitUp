"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { CategoryBadge } from "./CategoryBadge";
import { DocumentGenerator } from "@/components/DocumentGenerator";
import { DocumentPreview } from "@/components/DocumentPreview";
import { AlertBanner } from "@/components/alerts/AlertBanner";
import { ClipboardList, FileText } from "@/lib/icons";
import { Image } from "lucide-react";

const CATEGORY_WIZARD_MAP: Record<string, { id: string; label: string }> = {
  laboral: { id: "despido_improcedente", label: "Gestionar despido" },
  consumo: { id: "reclamar_factura", label: "Reclamar factura" },
  vivienda: { id: "reclamar_fianza", label: "Reclamar fianza" },
  trafico: { id: "recurrir_multa", label: "Recurrir multa" },
};

type DetectedDeadline = {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
};

type ChatMessageProps = {
  role: "user" | "assistant";
  content: string;
  category?: string;
  subcategory?: string;
  detectedDeadlines?: DetectedDeadline[];
  attachments?: { name: string; type: string }[];
  followUpSuggestions?: string[];
  onFollowUpClick?: (text: string) => void;
  onCopy?: () => void;
  showGenerateDoc?: boolean;
  conversationId?: string | null;
  messageIndex?: number;
  feedbackRating?: "positive" | "negative" | null;
  onFeedback?: (messageIndex: number, rating: "positive" | "negative") => void;
  hasDocumentAccess?: boolean;
  hasAlertAccess?: boolean;
  onProRequired?: () => void;
};

function getFileIcon(type: string) {
  if (type.startsWith("image/")) return <Image className="w-4 h-4 shrink-0" />;
  return <FileText className="w-4 h-4 shrink-0" />;
}

export function ChatMessage({
  role,
  content,
  category,
  subcategory,
  detectedDeadlines,
  attachments,
  followUpSuggestions,
  onFollowUpClick,
  onCopy,
  showGenerateDoc,
  conversationId,
  messageIndex,
  feedbackRating,
  onFeedback,
  hasDocumentAccess,
  hasAlertAccess = false,
  onProRequired,
}: ChatMessageProps) {
  const isUser = role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="max-w-[85%]">
        {!isUser && (category || subcategory) && (
          <div className="mb-1">
            <CategoryBadge category={category || "otro"} subcategory={subcategory} />
          </div>
        )}
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? "bg-gradient-to-br from-[var(--primary)] to-blue-600 text-white shadow-md shadow-blue-500/20"
              : "border border-slate-200/80 bg-white text-slate-800 shadow-md"
          }`}
        >
          {isUser ? (
            <div className="space-y-2">
              {attachments && attachments.length > 0 && (
                <div className="flex flex-wrap gap-2 pb-1">
                  {attachments.map((a, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-1.5 rounded-lg bg-white/20 px-2.5 py-1.5 text-xs font-medium text-white/90 border border-white/25"
                    >
                      {getFileIcon(a.type)}
                      <span className="max-w-[160px] truncate">{a.name}</span>
                    </div>
                  ))}
                </div>
              )}
              {content && <div className="whitespace-pre-wrap text-sm">{content}</div>}
            </div>
          ) : (
            <div className="prose prose-sm max-w-none prose-p:my-1 prose-ul:my-1 prose-li:my-0 prose-ol:my-1">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
            </div>
          )}
        </div>
        {!isUser && content && (
          <div className="mt-2 flex flex-col gap-2">
            <div className="flex items-center gap-2">
              {onCopy && (
                <button
                  onClick={onCopy}
                  className="text-xs text-slate-500 hover:text-slate-700"
                >
                  Copiar respuesta
                </button>
              )}
              {onFeedback && messageIndex !== undefined && (
                <div className="flex items-center gap-1 ml-1">
                  <button
                    onClick={() => onFeedback(messageIndex, "positive")}
                    className={`rounded-md p-1 transition-all ${
                      feedbackRating === "positive"
                        ? "bg-green-100 text-green-600"
                        : "text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                    }`}
                    title="Respuesta útil"
                  >
                    <svg className="h-3.5 w-3.5" fill={feedbackRating === "positive" ? "currentColor" : "none"} viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6.633 10.25c.806 0 1.533-.446 2.031-1.08a9.041 9.041 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V2.75a.75.75 0 01.75-.75 2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282m0 0H20.25a2.25 2.25 0 012.25 2.25v1.372c0 .516-.125.977-.348 1.384a4.5 4.5 0 01-1.27 1.59c-.422.335-.703.813-.703 1.327a4.5 4.5 0 01-1.265 3.13A2.25 2.25 0 0116.5 21H8.68a4.5 4.5 0 01-3.394-1.542l-.547-.605A2.25 2.25 0 014.25 17.34V10.5a2.25 2.25 0 012.25-2.25h.133z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => onFeedback(messageIndex, "negative")}
                    className={`rounded-md p-1 transition-all ${
                      feedbackRating === "negative"
                        ? "bg-red-100 text-red-600"
                        : "text-slate-400 hover:bg-slate-100 hover:text-slate-600"
                    }`}
                    title="Respuesta mejorable"
                  >
                    <svg className="h-3.5 w-3.5" fill={feedbackRating === "negative" ? "currentColor" : "none"} viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M7.498 15.25H4.372c-1.026 0-1.945-.694-2.054-1.715a12.137 12.137 0 01-.068-1.285c0-2.848.992-5.464 2.649-7.521C5.287 4.247 5.886 4 6.504 4h4.016a4.5 4.5 0 011.423.23l3.114 1.04a4.5 4.5 0 001.423.23h.327M7.498 15.25c.618 0 .991.724.725 1.282A7.471 7.471 0 007.5 19.75 2.25 2.25 0 009.75 22a.75.75 0 00.75-.75v-.633c0-.573.11-1.14.322-1.672.304-.76.93-1.33 1.653-1.715a9.04 9.04 0 002.86-2.4c.498-.634 1.226-1.08 2.032-1.08h.384" />
                    </svg>
                  </button>
                </div>
              )}
            </div>
            {detectedDeadlines?.length ? (
              <AlertBanner
                deadlines={detectedDeadlines}
                conversationId={conversationId}
                hasAccess={hasAlertAccess ?? false}
                onUpgradeRequired={onProRequired}
              />
            ) : null}
            {showGenerateDoc && conversationId && (
              <div className="space-y-2">
                <DocumentPreview
                  conversationId={conversationId}
                  hasAccess={hasDocumentAccess ?? false}
                  onAccessRequired={onProRequired}
                  onGenerate={() => {}}
                />
                <DocumentGenerator
                  conversationId={conversationId}
                  hasAccess={hasDocumentAccess ?? false}
                  onAccessRequired={onProRequired}
                />
              </div>
            )}
            {/* Action cards: wizard link based on category */}
            {showGenerateDoc && category && CATEGORY_WIZARD_MAP[category] && (
              <Link
                href={`/wizard/${CATEGORY_WIZARD_MAP[category].id}`}
                className="flex items-center gap-3 rounded-xl border border-amber-200 bg-amber-50 p-3 transition-all hover:border-amber-300 hover:shadow-sm"
              >
                <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-100">
                  <ClipboardList className="h-4 w-4 text-amber-700" />
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-semibold text-amber-800">Trámite guiado disponible</p>
                  <p className="text-[11px] text-amber-600">{CATEGORY_WIZARD_MAP[category].label} paso a paso</p>
                </div>
                <svg className="h-4 w-4 text-amber-400 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
                </svg>
              </Link>
            )}
            {followUpSuggestions && followUpSuggestions.length > 0 && onFollowUpClick && (
              <div className="flex flex-wrap gap-2 mt-1">
                {followUpSuggestions.map((suggestion, idx) => (
                  <button
                    key={idx}
                    onClick={() => onFollowUpClick(suggestion)}
                    className="inline-flex items-center gap-1 rounded-full border border-[var(--primary)]/20 bg-blue-50 px-3 py-1.5 text-xs font-medium text-[var(--primary)] transition-all hover:bg-[var(--primary)] hover:text-white hover:border-[var(--primary)] hover:shadow-sm"
                  >
                    {suggestion}
                    <svg className="h-3 w-3 opacity-50" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                    </svg>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
