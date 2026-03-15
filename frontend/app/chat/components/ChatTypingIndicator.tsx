"use client";

export function ChatTypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="flex gap-1 rounded-2xl bg-slate-100 px-4 py-3">
        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
      </div>
    </div>
  );
}
