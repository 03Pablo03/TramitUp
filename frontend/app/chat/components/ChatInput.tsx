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

export function ChatInput({ onSend, disabled, loading }: ChatInputProps) {
  const [message, setMessage] = useState("");
  const [attachments, setAttachments] = useState<AttachedFile[]>([]);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea without scroll
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = textarea.scrollHeight + 'px'; // No max limit
    }
  }, [message]);

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
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* File upload area */}
      {showFileUpload && (
        <div className="mb-4 p-4 bg-slate-50/90 rounded-2xl border border-slate-200/80 shadow-inner">
          <FileUpload
            onFilesSelected={(newFiles) => setAttachments(prev => [...prev, ...newFiles])}
            onFileRemoved={(fileId) => setAttachments(prev => prev.filter(f => f.id !== fileId))}
            attachedFiles={attachments}
            disabled={disabled || loading}
          />
        </div>
      )}

      {/* Input container */}
      <div className="flex items-end gap-3">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe tu situación... ej: 'Iberia me canceló el vuelo del viernes'"
            disabled={disabled || loading}
            rows={1}
            className="w-full resize-none overflow-hidden rounded-2xl border-2 border-slate-200 bg-white pl-12 pr-4 py-3.5 text-slate-800 placeholder-slate-400 shadow-sm transition-all focus:border-[var(--primary)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/25 focus:shadow-md disabled:opacity-50"
            style={{ minHeight: '52px' }}
          />
          
          <button
            type="button"
            onClick={() => setShowFileUpload(!showFileUpload)}
            disabled={disabled || loading}
            className={`absolute left-3.5 top-3.5 p-2 rounded-xl transition-all ${
              showFileUpload || attachments.length > 0
                ? 'text-[var(--primary)] bg-[var(--primary-light)]'
                : 'text-slate-400 hover:text-slate-600 hover:bg-slate-100'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
            title="Adjuntar archivos"
          >
            <Paperclip className="w-5 h-5" />
          </button>
        </div>
        
        <button
          type="button"
          onClick={handleSubmit}
          disabled={disabled || loading || (!message.trim() && attachments.length === 0)}
          className="flex h-[52px] w-[52px] shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[var(--primary)] to-blue-600 text-white shadow-md shadow-blue-500/25 transition-all hover:shadow-lg hover:shadow-blue-500/30 hover:from-[var(--primary-dark)] hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-[var(--primary)] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
          title="Enviar"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>

      {/* Hints and disclaimer */}
      <div className="mt-3 flex flex-col items-center gap-1">
        <span className="text-xs text-slate-500">
          ↵ Enter para enviar · Shift+Enter nueva línea
          {attachments.length > 0 && (
            <span className="ml-2 font-medium text-[var(--primary)]">
              · {attachments.length} archivo{attachments.length > 1 ? 's' : ''} adjunto{attachments.length > 1 ? 's' : ''}
            </span>
          )}
        </span>
        <LegalDisclaimer />
      </div>
    </div>
  );
}
