"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Loader2, Paperclip } from "lucide-react";
import { FileUpload, AttachedFile } from "@/components/chat/FileUpload";
import { LegalDisclaimer } from "./LegalDisclaimer";

type ChatInputProps = {
  onSend: (message: string, attachments?: AttachedFile[]) => void;
  disabled?: boolean;
  loading?: boolean;
};

const ROTATING_PLACEHOLDERS = [
  "Iberia me canceló el vuelo...",
  "Me han despedido después de 3 años...",
  "Mi casero no me devuelve la fianza...",
  "Me pusieron una multa injusta...",
];

export function ChatInput({ onSend, disabled, loading }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [attachments, setAttachments] = useState<AttachedFile[]>([]);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [placeholderOpacity, setPlaceholderOpacity] = useState(1);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea without scroll
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    }
  }, [message]);

  // Rotating placeholder — only when unfocused and no text
  useEffect(() => {
    if (isFocused || message) return;

    const interval = setInterval(() => {
      // Fade out
      setPlaceholderOpacity(0);
      setTimeout(() => {
        setPlaceholderIndex((prev) => (prev + 1) % ROTATING_PLACEHOLDERS.length);
        setPlaceholderOpacity(1);
      }, 500);
    }, 5000);

    return () => clearInterval(interval);
  }, [isFocused, message]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if ((message.trim() || attachments.length > 0) && !disabled && !loading) {
      onSend(message.trim(), attachments);
      setMessage("");
      setAttachments([]);
      setShowFileUpload(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const showRotatingPlaceholder = !isFocused && !message;
  const placeholderText = showRotatingPlaceholder
    ? ROTATING_PLACEHOLDERS[placeholderIndex]
    : "Describe tu situación...";

  return (
    <div className="max-w-4xl mx-auto">
      {/* File upload area */}
      {showFileUpload && (
        <div className="mb-4 p-4 bg-slate-50/90 rounded-2xl border border-slate-200/80 shadow-inner">
          <FileUpload
            onFilesSelected={(newFiles) =>
              setAttachments((prev) => [...prev, ...newFiles])
            }
            onFileRemoved={(fileId) =>
              setAttachments((prev) => prev.filter((f) => f.id !== fileId))
            }
            attachedFiles={attachments}
            disabled={disabled || loading}
          />
        </div>
      )}

      {/* Input container with focus glow */}
      <div className="flex items-end gap-3">
        <div
          className={`flex-1 relative rounded-2xl transition-all duration-200 ease-out ${
            isFocused
              ? "ring-2 ring-blue-400/40"
              : ""
          }`}
        >
          {/* Rotating placeholder overlay */}
          {showRotatingPlaceholder && (
            <span
              className="pointer-events-none absolute left-12 top-3.5 text-slate-400 text-sm select-none transition-opacity duration-500"
              style={{ opacity: placeholderOpacity }}
            >
              {placeholderText}
            </span>
          )}

          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            placeholder={showRotatingPlaceholder ? "" : "Describe tu situación..."}
            disabled={disabled || loading}
            rows={1}
            className={`w-full resize-none overflow-hidden rounded-2xl border-2 bg-white pl-12 pr-4 py-3.5 text-slate-800 placeholder-slate-400 shadow-sm transition-all duration-200 ease-out focus:outline-none disabled:opacity-50 ${
              isFocused
                ? "border-blue-400"
                : "border-slate-200 focus:border-blue-400"
            }`}
            style={{ minHeight: "52px" }}
          />

          <button
            type="button"
            onClick={() => setShowFileUpload(!showFileUpload)}
            disabled={disabled || loading}
            className={`absolute left-3.5 top-3.5 p-2 rounded-xl transition-all duration-200 ease-out ${
              showFileUpload || attachments.length > 0
                ? "text-[var(--primary)] bg-[var(--primary-light)]"
                : "text-slate-400 hover:text-slate-600 hover:bg-slate-100"
            } disabled:opacity-50 disabled:cursor-not-allowed`}
            title="Adjuntar archivos"
          >
            <Paperclip className="w-5 h-5" strokeWidth={1.5} />
          </button>
        </div>

        <button
          type="button"
          onClick={handleSubmit}
          disabled={
            disabled || loading || (!message.trim() && attachments.length === 0)
          }
          className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-white shadow-md shadow-blue-500/25 transition-all duration-200 ease-out hover:bg-blue-700 hover:from-[var(--primary-dark)] hover:to-blue-700 hover:shadow-lg hover:shadow-blue-500/30 focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
          title="Enviar"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" strokeWidth={1.5} />
          ) : (
            <Send className="w-5 h-5" strokeWidth={1.5} />
          )}
        </button>
      </div>

      {/* Hints and disclaimer */}
      <div className="mt-3 flex flex-col items-center gap-1">
        {attachments.length > 0 && (
          <span className="text-xs font-medium text-[var(--primary)]">
            {attachments.length} archivo{attachments.length > 1 ? "s" : ""} adjunto
            {attachments.length > 1 ? "s" : ""}
          </span>
        )}
        <LegalDisclaimer />
      </div>
    </div>
  );
}
