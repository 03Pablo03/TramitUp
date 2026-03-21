"use client";

import Link from "next/link";

interface ToolHeaderProps {
  title: string;
}

export function ToolHeader({ title }: ToolHeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/60 bg-white/90 backdrop-blur-md shadow-sm">
      <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-3">
        <div className="flex items-center gap-4">
          <Link
            href="/chat"
            className="flex items-center gap-1.5 text-sm font-medium text-slate-500 hover:text-slate-800 transition-colors"
          >
            ← Chat
          </Link>
          <span className="h-4 w-px bg-slate-200" />
          <span className="text-sm font-semibold text-slate-800">{title}</span>
        </div>
        <Link
          href="/chat"
          className="rounded-lg bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
        >
          Ir al chat
        </Link>
      </div>
    </header>
  );
}
