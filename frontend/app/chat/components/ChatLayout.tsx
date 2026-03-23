"use client";

import { useState } from "react";
import Link from "next/link";
import { ChatSidebar } from "./ChatSidebar";
import { ProBadge } from "@/components/ProBadge";

type Conversation = { id: string; title: string; category?: string; created_at: string };

type ChatLayoutProps = {
  children: React.ReactNode;
  conversations: Conversation[];
  currentConversationId: string | null;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  remainingChats: number | null;
  urgentAlertsCount?: number;
  userPlan?: string;
  onRenameConversation?: (conversationId: string, newTitle: string) => Promise<void>;
  onDeleteConversation?: (conversationId: string) => Promise<void>;
};

export function ChatLayout({
  children,
  conversations,
  currentConversationId,
  onSelectConversation,
  onNewChat,
  remainingChats,
  urgentAlertsCount = 0,
  userPlan = "free",
  onRenameConversation,
  onDeleteConversation,
}: ChatLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <div className="flex h-screen">
      <ChatSidebar
        conversations={conversations}
        currentId={currentConversationId}
        onSelect={onSelectConversation}
        onNewChat={onNewChat}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        onRenameConversation={onRenameConversation}
        onDeleteConversation={onDeleteConversation}
      />
      <div className="flex flex-1 flex-col">
        <header className="flex h-14 items-center justify-between border-b border-slate-200/60 bg-white/90 backdrop-blur-md px-6 shadow-sm">
          <div className="flex items-center gap-6">
            <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
              TramitUp
            </span>
            {remainingChats !== null && remainingChats !== -1 && (
              <span className="text-sm text-slate-500">
                {remainingChats} consultas restantes hoy
              </span>
            )}
          </div>
          <nav className="flex items-center gap-2">
            {/* Herramientas destacadas */}
            <Link
              href="/calculadora"
              className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 transition-all hover:bg-emerald-100 hover:border-emerald-300"
            >
              🧮 Calculadora
            </Link>
            <Link
              href="/contrato"
              className="inline-flex items-center gap-1.5 rounded-lg border border-violet-200 bg-violet-50 px-3 py-1.5 text-xs font-semibold text-violet-700 transition-all hover:bg-violet-100 hover:border-violet-300"
            >
              📄 Analizar contrato
              <ProBadge />
            </Link>

            {/* Separador */}
            <span className="mx-1 h-5 w-px bg-slate-200" />

            {/* Navegación secundaria */}
            <Link
              href="/alerts"
              className="relative flex items-center gap-1 text-sm font-medium text-slate-500 transition-colors hover:text-slate-800"
            >
              🔔
              {urgentAlertsCount > 0 && (
                <span className="absolute -right-1.5 -top-1.5 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
                  {urgentAlertsCount > 99 ? "99+" : urgentAlertsCount}
                </span>
              )}
            </Link>
            <Link
              href="/casos"
              className="inline-flex items-center gap-1.5 text-sm font-medium text-slate-500 transition-colors hover:text-slate-800"
            >
              Expedientes
              <ProBadge />
            </Link>
            <Link
              href="/documents"
              className="text-sm font-medium text-slate-500 transition-colors hover:text-slate-800"
            >
              Documentos
            </Link>

            {/* Separador */}
            <span className="mx-1 h-5 w-px bg-slate-200" />

            {/* PRO + Cuenta */}
            {userPlan !== "pro" && userPlan !== "document" && (
              <Link
                href="/pricing"
                className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 px-3 py-1.5 text-xs font-bold text-white shadow-md hover:from-amber-500 hover:to-orange-600 transition-all"
              >
                <svg className="h-3.5 w-3.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                PRO
              </Link>
            )}
            <Link
              href="/account"
              className="rounded-lg bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
            >
              Cuenta
            </Link>
          </nav>
        </header>
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
