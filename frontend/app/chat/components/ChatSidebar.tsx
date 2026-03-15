"use client";

import { MessageSquare, ChevronLeft, ChevronRight, Plus } from "lucide-react";
import { ConversationMenu } from "@/components/chat/ConversationMenu";

type Conversation = { id: string; title: string; category?: string; created_at: string };

type ChatSidebarProps = {
  conversations: Conversation[];
  currentId: string | null;
  onSelect: (id: string) => void;
  onNewChat: () => void;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
  onRenameConversation?: (conversationId: string, newTitle: string) => Promise<void>;
  onDeleteConversation?: (conversationId: string) => Promise<void>;
};

function formatDate(dateStr: string): string {
  try {
    const date = new Date(dateStr);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return "Ayer";
    if (diffDays <= 7) return `Hace ${diffDays} días`;
    return date.toLocaleDateString("es-ES", { 
      day: "numeric", 
      month: "short" 
    });
  } catch {
    return "Fecha inválida";
  }
}

export function ChatSidebar({
  conversations,
  currentId,
  onSelect,
  onNewChat,
  collapsed = false,
  onToggleCollapse,
  onRenameConversation,
  onDeleteConversation,
}: ChatSidebarProps) {
  return (
    <aside
      className={`flex flex-col border-r border-slate-200/60 bg-gradient-to-b from-white to-slate-50/80 transition-all md:w-64 ${
        collapsed ? "w-0 overflow-hidden md:w-14" : "w-full"
      }`}
    >
      <div className="flex h-14 items-center justify-between gap-2 border-b border-slate-200/60 px-4 bg-white/80">
        {collapsed ? (
          <button
            onClick={onNewChat}
            className="rounded-lg p-2 text-[var(--primary)] hover:bg-blue-50 transition-colors"
            aria-label="Nueva conversación"
          >
            <Plus className="w-4 h-4" />
          </button>
        ) : (
          <span className="font-display text-sm font-bold tracking-tight text-[var(--primary)]">TramitUp</span>
        )}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-700 transition-colors md:block flex-shrink-0"
            aria-label={collapsed ? "Expandir" : "Colapsar"}
          >
            {collapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
          </button>
        )}
      </div>
      
      <div className="flex-1 overflow-y-auto p-3">
        {!collapsed && (
          <button
            onClick={onNewChat}
            className="mb-4 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[var(--primary)] to-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-md transition-all hover:from-[var(--primary-dark)] hover:to-blue-700"
          >
            <Plus className="h-4 w-4" />
            Nueva conversación
          </button>
        )}
        {conversations.length > 0 && !collapsed && (
          <>
            <h3 className="mb-2 px-2 text-xs font-semibold uppercase tracking-wider text-slate-500">Conversaciones</h3>
            <ul className="space-y-1">
              {conversations.map((conv) => (
                <li key={conv.id}>
                  <div
                    className={`group flex w-full items-center gap-3 rounded-xl p-3 transition-all ${
                      currentId === conv.id
                        ? "bg-blue-50 border border-blue-200/60 shadow-sm"
                        : "border border-transparent hover:bg-slate-50 hover:border-slate-200/60"
                    }`}
                  >
                    <button
                      onClick={() => onSelect(conv.id)}
                      className="flex items-center gap-3 flex-1 min-w-0 text-left"
                    >
                      <MessageSquare className="h-4 w-4 flex-shrink-0" />
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-sm font-medium">{conv.title}</p>
                        <p className="truncate text-xs text-slate-500">
                          {formatDate(conv.created_at)}
                        </p>
                      </div>
                    </button>
                    
                    {(onRenameConversation || onDeleteConversation) && (
                      <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                        <ConversationMenu
                          conversationId={conv.id}
                          conversationTitle={conv.title}
                          onRename={onRenameConversation || (async () => {})}
                          onDelete={onDeleteConversation || (async () => {})}
                        />
                      </div>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </>
        )}
      </div>
    </aside>
  );
}
