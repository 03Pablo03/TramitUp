"use client";

import { useEffect, useRef } from "react";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";
import { ChatTypingIndicator } from "./ChatTypingIndicator";
import { DocumentGenerator } from "@/components/DocumentGenerator";
import { AlertBanner } from "@/components/alerts/AlertBanner";
import { AttachedFile } from "@/components/chat/FileUpload";

const QUICK_SUGGESTIONS = [
  { text: "Me han cancelado el vuelo", icon: "✈️", accent: "from-blue-500 to-cyan-500", bg: "bg-blue-50", border: "border-blue-200/60", hover: "hover:border-blue-400/50 hover:bg-blue-50/90" },
  { text: "Quiero reclamar una factura incorrecta", icon: "💡", accent: "from-amber-500 to-orange-500", bg: "bg-amber-50", border: "border-amber-200/60", hover: "hover:border-amber-400/50 hover:bg-amber-50/90" },
  { text: "Me han despedido y no sé qué hacer", icon: "💼", accent: "from-slate-600 to-slate-700", bg: "bg-slate-50", border: "border-slate-200/60", hover: "hover:border-slate-400/50 hover:bg-slate-50/90" },
  { text: "Tengo un problema con mi arrendador", icon: "🏠", accent: "from-emerald-500 to-teal-500", bg: "bg-emerald-50", border: "border-emerald-200/60", hover: "hover:border-emerald-400/50 hover:bg-emerald-50/90" },
];

type DetectedDeadline = {
  description: string;
  days: number;
  business_days: boolean;
  reference_date: string | null;
  law_reference: string;
  urgency: string;
};

type CompensationEstimate = {
  amount_eur?: number;
  reduced_amount_eur?: number;
  applies: boolean;
  reason: string;
};

type PortalInfo = {
  portal_key: string;
  name: string;
  url: string;
  needs_digital_cert: boolean;
  also_by_post: boolean;
  notes?: string;
  official_form_url?: string | null;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  category?: string;
  subcategory?: string;
  detectedDeadlines?: DetectedDeadline[];
  portalInfo?: PortalInfo;
  compensationEstimate?: CompensationEstimate;
};

type ChatWindowProps = {
  messages: Message[];
  sending: boolean;
  currentCategory?: string;
  currentSubcategory?: string;
  onSend: (text: string, attachments?: AttachedFile[]) => void;
  onCopy: (content: string) => void;
  conversationId: string | null;
  hasDocumentAccess: boolean;
  hasAlertAccess?: boolean;
  onProRequired?: () => void;
  error?: string;
};

export function ChatWindow({
  messages,
  sending,
  currentCategory,
  currentSubcategory,
  onSend,
  onCopy,
  conversationId,
  hasDocumentAccess,
  hasAlertAccess = false,
  onProRequired,
  error,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  return (
    <div className="h-full flex flex-col overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50/30 to-amber-50/40">
      <div className="flex-1 overflow-y-auto p-6 lg:p-8">
        {messages.length === 0 && !sending && (
          <div className="mx-auto max-w-2xl space-y-12 pt-10 lg:pt-16">
            <div className="text-center space-y-4">
              <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-2xl shadow-lg shadow-blue-500/20">
                💬
              </div>
              <h1 className="font-display text-2xl font-bold text-slate-800 sm:text-3xl leading-tight">
                Hola, soy Tramitup
              </h1>
              <p className="text-slate-600 text-base sm:text-lg max-w-lg mx-auto leading-relaxed">
                Cuéntame tu situación y te explico qué dice la normativa.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
              {QUICK_SUGGESTIONS.map((s) => (
                <button
                  key={s.text}
                  onClick={() => onSend(s.text)}
                  className={`group flex items-center gap-4 p-5 text-left rounded-2xl border shadow-sm transition-all duration-200 ${s.bg} ${s.border} ${s.hover} hover:shadow-lg hover:scale-[1.02] active:scale-[0.99]`}
                >
                  <span className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gradient-to-br ${s.accent} text-xl shadow-md`}>
                    {s.icon}
                  </span>
                  <span className="text-sm font-semibold text-slate-800 group-hover:text-slate-900">
                    {s.text}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
        <div className="mx-auto max-w-3xl space-y-6">
          {messages.map((m, i) => {
            if (m.role === "assistant" && !m.content && sending && i === messages.length - 1) {
              return <ChatTypingIndicator key={i} />;
            }
            return (
              <ChatMessage
                key={i}
                role={m.role}
                content={m.content}
                category={m.category}
                subcategory={m.subcategory}
                detectedDeadlines={m.detectedDeadlines}
                onCopy={m.role === "assistant" ? () => onCopy(m.content) : undefined}
                showGenerateDoc={
                  m.role === "assistant" &&
                  !!m.content &&
                  i === messages.length - 1 &&
                  !sending &&
                  !!conversationId
                }
                conversationId={conversationId}
                hasDocumentAccess={hasDocumentAccess}
                hasAlertAccess={hasAlertAccess}
                onProRequired={onProRequired}
              />
            );
          })}
        </div>
        <div ref={bottomRef} />
      </div>
      <div className="border-t border-slate-200/60 bg-white/90 backdrop-blur-md p-4 lg:p-6 shadow-[0_-8px_30px_-8px_rgba(15,23,42,0.08)]">
        {error && <p className="mb-3 text-sm text-red-600 font-medium">{error}</p>}
        <ChatInput onSend={onSend} disabled={sending} loading={sending} />
      </div>
    </div>
  );
}
