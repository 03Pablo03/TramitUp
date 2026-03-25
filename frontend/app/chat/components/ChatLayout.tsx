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
        userPlan={userPlan}
        urgentAlertsCount={urgentAlertsCount}
        remainingChats={remainingChats}
      />
      <div className="flex flex-1 flex-col min-w-0">
        <header className="flex h-14 items-center justify-between border-b border-slate-200/60 bg-white/90 backdrop-blur-md px-6 shadow-sm">
          <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
            TramitUp
          </span>
          <Link
            href="/account"
            className="rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition-all duration-200 hover:from-[var(--primary-dark)] hover:to-blue-700"
          >
            Cuenta
          </Link>
        </header>
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
