"use client";

import Link from "next/link";

interface ToolHeaderProps {
  title: string;
  backHref?: string;
  backLabel?: string;
  actions?: React.ReactNode;
}

export function ToolHeader({
  title,
  backHref = "/chat",
  backLabel = "Chat",
  actions,
}: ToolHeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/60 bg-white/90 backdrop-blur-md shadow-sm">
      <div className="mx-auto flex max-w-3xl items-center justify-between px-6 py-3">
        <div className="flex items-center gap-3 min-w-0">
          <Link
            href={backHref}
            className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm font-medium text-slate-600 transition-all hover:bg-slate-100 hover:border-slate-300 shrink-0"
          >
            <svg
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={2}
              stroke="currentColor"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
            </svg>
            {backLabel}
          </Link>
          <span className="h-5 w-px bg-slate-200 shrink-0" />
          <span className="text-sm font-semibold text-slate-800 truncate">{title}</span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {actions}
          {backHref !== "/chat" && (
            <Link
              href="/chat"
              className="inline-flex items-center gap-1.5 rounded-lg bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
            >
              <svg
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M2.25 12.76c0 1.6 1.123 2.994 2.707 3.227 1.087.16 2.185.283 3.293.369V21l4.076-4.076a1.526 1.526 0 011.037-.443 48.282 48.282 0 005.68-.494c1.584-.233 2.707-1.626 2.707-3.228V6.741c0-1.602-1.123-2.995-2.707-3.228A48.394 48.394 0 0012 3c-2.392 0-4.744.175-7.043.513C3.373 3.746 2.25 5.14 2.25 6.741v6.018z"
                />
              </svg>
              Ir al chat
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
