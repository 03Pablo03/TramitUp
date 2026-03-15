"use client";

import { useState } from "react";
import Link from "next/link";
import { ChatSidebar } from "./ChatSidebar";

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
          <nav className="flex items-center gap-4">
            {userPlan !== "pro" && userPlan !== "document" && (
              <Link
                href="/account"
                className="inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2 text-sm font-bold text-white shadow-md hover:from-[var(--primary-dark)] hover:to-blue-700 transition-all"
              >
                <span className="text-amber-300">★</span> Hazte PRO
              </Link>
            )}
            <Link
              href="/alerts"
              className="relative flex items-center gap-1.5 text-sm font-medium text-slate-600 transition-colors hover:text-slate-900"
            >
              <span className="text-amber-500">🔔</span>
              Alertas
              {urgentAlertsCount > 0 && (
                <span className="flex h-5 min-w-[20px] items-center justify-center rounded-full bg-red-500 px-1.5 text-xs font-bold text-white">
                  {urgentAlertsCount > 99 ? "99+" : urgentAlertsCount}
                </span>
              )}
            </Link>
            <Link
              href="/documents"
              className="text-sm font-medium text-slate-600 transition-colors hover:text-slate-900"
            >
              Documentos
            </Link>
            <Link
              href="/account"
              className="rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-5 py-2.5 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:shadow-lg hover:from-[var(--primary-dark)] hover:to-blue-700"
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
