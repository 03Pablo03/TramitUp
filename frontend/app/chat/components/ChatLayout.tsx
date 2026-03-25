"use client";

import { useState } from "react";
import Link from "next/link";
import { Star } from "lucide-react";
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
        <header className="flex h-14 items-center justify-between border-b border-slate-100 bg-white px-6">
          <span className="text-sm font-semibold text-slate-900">
            TramitUp
          </span>
          <div className="flex items-center gap-2">
            {userPlan !== "pro" && userPlan !== "document" ? (
              <Link
                href="/pricing"
                className="inline-flex items-center gap-1.5 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 px-4 py-1.5 text-sm font-semibold text-white transition-all duration-200 hover:brightness-110"
              >
                <Star className="h-3.5 w-3.5 shrink-0" strokeWidth={1.5} />
                <span className="hidden sm:inline">PRO</span>
              </Link>
            ) : (
              <span className="rounded-full bg-purple-100 px-2 py-0.5 text-xs font-bold text-purple-700">
                PRO
              </span>
            )}
            <Link
              href="/account"
              className="rounded-lg border border-slate-200 px-4 py-1.5 text-sm font-medium text-slate-700 transition-colors duration-200 hover:bg-slate-50"
            >
              Cuenta
            </Link>
          </div>
        </header>
        <main className="flex-1 overflow-hidden">{children}</main>
      </div>
    </div>
  );
}
