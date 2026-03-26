"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  MessageSquare,
  ChevronLeft,
  ChevronRight,
  Plus,
  Calculator,
  FileText,
  ListChecks,
  FolderOpen,
  type LucideIcon,
} from "lucide-react";
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
  userPlan?: string;
  urgentAlertsCount?: number;
  remainingChats?: number | null;
};

type NavItem = {
  href: string;
  label: string;
  icon: LucideIcon;
};

function formatDate(dateStr: string): string {
  try {
    const date = new Date(dateStr);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    if (diffDays === 1) return "Ayer";
    if (diffDays <= 7) return `Hace ${diffDays} días`;
    return date.toLocaleDateString("es-ES", { day: "numeric", month: "short" });
  } catch {
    return "";
  }
}

const NAV_ITEMS: NavItem[] = [
  { href: "/calculadora", label: "Indemnizaciones", icon: Calculator },
  { href: "/contrato", label: "Contratos", icon: FileText },
  { href: "/wizard", label: "Trámite guiado", icon: ListChecks },
  { href: "/casos", label: "Expedientes", icon: FolderOpen },
];

export function ChatSidebar({
  conversations,
  currentId,
  onSelect,
  onNewChat,
  collapsed = false,
  onToggleCollapse,
  onRenameConversation,
  onDeleteConversation,
  remainingChats = null,
}: ChatSidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={`flex flex-col bg-slate-900 transition-all duration-300 ease-out md:w-64 ${
        collapsed ? "w-0 overflow-hidden md:w-14" : "w-full"
      }`}
    >
      {/* Header */}
      <div className="flex h-14 items-center justify-between gap-2 border-b border-white/10 px-3">
        {!collapsed && (
          <Link
            href="/chat"
            className="pl-1 text-sm font-semibold text-white hover:opacity-70 transition-opacity"
          >
            TramitUp
          </Link>
        )}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="rounded-lg p-2 text-white/50 hover:bg-white/10 hover:text-white transition-colors duration-200 flex-shrink-0"
            aria-label={collapsed ? "Expandir" : "Colapsar"}
          >
            {collapsed ? (
              <ChevronRight className="w-4 h-4" strokeWidth={1.5} />
            ) : (
              <ChevronLeft className="w-4 h-4" strokeWidth={1.5} />
            )}
          </button>
        )}
      </div>

      {/* Scrollable body */}
      <div className="flex flex-1 flex-col overflow-y-auto">
        {/* Nueva conversación */}
        <div className="px-3 pt-3">
          {collapsed ? (
            <button
              onClick={onNewChat}
              className="flex w-full items-center justify-center rounded-lg p-2.5 text-white/70 hover:bg-white/10 hover:text-white transition-colors duration-200"
              aria-label="Nueva conversación"
            >
              <Plus className="w-4 h-4" strokeWidth={1.5} />
            </button>
          ) : (
            <button
              onClick={onNewChat}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-white/10 px-4 py-2.5 text-sm font-medium text-white transition-all duration-200 hover:bg-white/20"
            >
              <Plus className="h-4 w-4" strokeWidth={1.5} />
              Nueva conversación
            </button>
          )}
        </div>

        {/* Separador */}
        <div className="mx-3 mt-3 border-t border-white/10" />

        {/* Herramientas */}
        <nav className="px-2 pt-3 pb-2">
          {!collapsed && (
            <p className="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-white/50">
              Herramientas
            </p>
          )}
          <ul className="space-y-0.5">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");

              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    title={collapsed ? item.label : undefined}
                    className={`relative flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium transition-all duration-300 ease-out group ${
                      isActive
                        ? "border-l-2 border-white bg-white/15 text-white"
                        : "text-white/70 hover:text-white hover:bg-white/10 border-l-2 border-transparent"
                    } ${collapsed ? "justify-center" : ""}`}
                  >
                    <Icon
                      className="w-4 h-4 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"
                      strokeWidth={1.5}
                    />
                    {!collapsed && (
                      <span className="flex-1 truncate">{item.label}</span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Separador */}
        <div className="mx-3 border-t border-white/10" />

        {/* Conversaciones */}
        <div className="flex-1 px-2 pt-3 pb-3">
          {!collapsed && remainingChats !== null && remainingChats !== -1 && (
            <p className="mb-2 px-2 text-xs text-white/40">
              {remainingChats} consultas restantes hoy
            </p>
          )}

          {conversations.length > 0 && !collapsed && (
            <>
              <p className="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-white/50">
                Conversaciones
              </p>
              <ul className="space-y-0.5">
                {conversations.map((conv) => (
                  <li key={conv.id}>
                    <div
                      className={`group flex w-full items-center gap-2 rounded-lg px-2 py-2 transition-all duration-200 ${
                        currentId === conv.id
                          ? "bg-white/15 text-white"
                          : "hover:bg-white/10"
                      }`}
                    >
                      <button
                        onClick={() => onSelect(conv.id)}
                        className="flex items-center gap-2.5 flex-1 min-w-0 text-left"
                      >
                        <MessageSquare
                          className="h-3.5 w-3.5 flex-shrink-0 text-white/40"
                          strokeWidth={1.5}
                        />
                        <div className="min-w-0 flex-1">
                          <p className={`truncate text-sm font-medium ${
                            currentId === conv.id ? "text-white" : "text-white/60 hover:text-white"
                          }`}>
                            {conv.title}
                          </p>
                          <p className="truncate text-xs text-white/40">
                            {formatDate(conv.created_at)}
                          </p>
                        </div>
                      </button>

                      {(onRenameConversation || onDeleteConversation) && (
                        <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
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
      </div>
    </aside>
  );
}
