"use client";

import { useEffect, useRef } from "react";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./ChatMessage";
import { ChatTypingIndicator } from "./ChatTypingIndicator";
import ChatEmptyState from "./ChatEmptyState";
import { AttachedFile } from "@/components/chat/FileUpload";

type DetectedDeadline = {
  description: string;
  days: number;
  reference_date: string | null;
  law_reference: string;
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
  attachments?: { name: string; type: string }[];
  followUpSuggestions?: string[];
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
  feedbackMap?: Record<number, "positive" | "negative">;
  onFeedback?: (messageIndex: number, rating: "positive" | "negative") => void;
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
  feedbackMap = {},
  onFeedback,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  return (
    <div className="h-full flex flex-col overflow-hidden bg-white">
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 && !sending && (
          <ChatEmptyState onSuggestionClick={onSend} />
        )}
        <div className={`mx-auto max-w-3xl space-y-6 px-6 lg:px-8 ${messages.length > 0 ? "py-6 lg:py-8" : ""}`}>
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
                attachments={m.attachments}
                followUpSuggestions={m.followUpSuggestions}
                onFollowUpClick={(text) => onSend(text)}
                onCopy={m.role === "assistant" ? () => onCopy(m.content) : undefined}
                showGenerateDoc={
                  m.role === "assistant" &&
                  !!m.content &&
                  i === messages.length - 1 &&
                  !sending &&
                  !!conversationId
                }
                conversationId={conversationId}
                messageIndex={i}
                feedbackRating={m.role === "assistant" ? feedbackMap[i] || null : null}
                onFeedback={m.role === "assistant" ? onFeedback : undefined}
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
