"use client";

import { useState } from "react";
import Link from "next/link";
import { Star, User } from "lucide-react";
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
        <header className="flex h-14 items-center justify-between border-b border-slate-200/80 bg-white/95 backdrop-blur-sm px-6 shadow-sm">
          <Link
            href="/"
            className="text-lg font-bold text-blue-600 hover:text-blue-700 transition-colors duration-200"
            title="Volver a inicio"
          >
            TramitUp
          </Link>
          <div className="flex items-center gap-2">
            {userPlan !== "pro" && userPlan !== "document" ? (
              <Link
                href="/pricing"
                className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-amber-400 to-yellow-500 px-4 py-1.5 text-sm font-semibold text-amber-900 shadow-sm transition-all duration-200 hover:brightness-110"
              >
                <Star className="h-3.5 w-3.5 shrink-0" strokeWidth={2} fill="currentColor" />
                <span className="hidden sm:inline">Hazte PRO</span>
              </Link>
            ) : (
              <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-bold text-amber-700">
                <Star className="h-3.5 w-3.5 fill-amber-600 text-amber-600" /> PRO
              </span>
            )}
            <Link
              href="/account"
              className="inline-flex items-center gap-1.5 rounded-lg bg-blue-600 px-4 py-1.5 text-sm font-medium text-white transition-colors duration-200 hover:bg-blue-700"
            >
              <User className="h-3.5 w-3.5 shrink-0" strokeWidth={1.5} />
              <span className="hidden sm:inline">Cuenta</span>
            </Link>
          </div>
        </header>
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
