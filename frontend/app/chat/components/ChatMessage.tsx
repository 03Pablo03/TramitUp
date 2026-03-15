"use client";

import ReactMarkdown from "react-markdown";
import { CategoryBadge } from "./CategoryBadge";
import { DocumentGenerator } from "@/components/DocumentGenerator";
import { AlertBanner } from "@/components/alerts/AlertBanner";

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
  onCopy?: () => void;
  showGenerateDoc?: boolean;
  conversationId?: string | null;
  hasDocumentAccess?: boolean;
  hasAlertAccess?: boolean;
  onProRequired?: () => void;
};

export function ChatMessage({
  role,
  content,
  category,
  subcategory,
  detectedDeadlines,
  onCopy,
  showGenerateDoc,
  conversationId,
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
            <div className="whitespace-pre-wrap text-sm">{content}</div>
          ) : (
            <div className="prose prose-sm max-w-none prose-p:my-1 prose-ul:my-1 prose-li:my-0">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>
        {!isUser && content && (
          <div className="mt-2 flex flex-col gap-2">
            <div className="flex gap-2">
              {onCopy && (
                <button
                  onClick={onCopy}
                  className="text-xs text-slate-500 hover:text-slate-700"
                >
                  Copiar respuesta
                </button>
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
              <DocumentGenerator
                conversationId={conversationId}
                hasAccess={hasDocumentAccess ?? false}
                onAccessRequired={onProRequired}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
