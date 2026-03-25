"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ProBadge } from "@/components/ProBadge";
import {
  MessageSquare,
  ChevronLeft,
  ChevronRight,
  Plus,
  Calculator,
  FileSearch,
  ClipboardList,
  FolderOpen,
  Files,
  Bell,
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
  pro?: boolean;
  badge?: number;
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

export function ChatSidebar({
  conversations,
  currentId,
  onSelect,
  onNewChat,
  collapsed = false,
  onToggleCollapse,
  onRenameConversation,
  onDeleteConversation,
  userPlan = "free",
  urgentAlertsCount = 0,
  remainingChats = null,
}: ChatSidebarProps) {
  const pathname = usePathname();
  const isPro = userPlan === "pro" || userPlan === "document";

  const NAV_ITEMS: NavItem[] = [
    { href: "/calculadora", label: "Calculadora", icon: Calculator },
    { href: "/contrato", label: "Analizar contrato", icon: FileSearch, pro: true },
    { href: "/wizard", label: "Trámite guiado", icon: ClipboardList },
    { href: "/casos", label: "Expedientes", icon: FolderOpen },
    { href: "/documents", label: "Documentos", icon: Files },
    { href: "/alerts", label: "Alertas", icon: Bell, badge: urgentAlertsCount },
  ];

  return (
    <aside
      className={`flex flex-col border-r border-slate-100 bg-white transition-all duration-300 ease-out md:w-64 ${
        collapsed ? "w-0 overflow-hidden md:w-14" : "w-full"
      }`}
    >
      {/* Header */}
      <div className="flex h-14 items-center justify-between gap-2 border-b border-slate-100 px-3">
        {!collapsed && (
          <Link
            href="/chat"
            className="pl-1 text-sm font-semibold text-slate-900 hover:opacity-70 transition-opacity"
          >
            TramitUp
          </Link>
        )}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-50 hover:text-slate-600 transition-colors duration-200 flex-shrink-0"
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
        {/* Navigation section */}
        <nav className="px-2 pt-3 pb-2">
          {!collapsed && (
            <p className="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              Herramientas
            </p>
          )}
          <ul className="space-y-0.5">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              const hasBadge = (item.badge ?? 0) > 0;

              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    title={collapsed ? item.label : undefined}
                    className={`relative flex items-center gap-3 rounded-lg px-2.5 py-2 text-sm font-medium transition-all duration-200 ease-out ${
                      isActive
                        ? "bg-blue-50 text-blue-700"
                        : "text-slate-700 hover:bg-slate-50 hover:text-slate-900"
                    } ${collapsed ? "justify-center" : ""}`}
                  >
                    {isActive && !collapsed && (
                      <span className="absolute left-0 top-1 bottom-1 w-0.5 rounded-full bg-blue-600" />
                    )}
                    <div className="relative flex-shrink-0">
                      <Icon
                        className={`w-4 h-4 ${isActive ? "text-blue-600" : "text-slate-400"}`}
                        strokeWidth={1.5}
                      />
                      {hasBadge && (
                        <span className="absolute -right-1 -top-1 flex h-3.5 min-w-[14px] items-center justify-center rounded-full bg-red-500 px-0.5 text-[9px] font-bold text-white">
                          {(item.badge ?? 0) > 99 ? "99+" : item.badge}
                        </span>
                      )}
                    </div>
                    {!collapsed && (
                      <>
                        <span className="flex-1 truncate">{item.label}</span>
                        {item.pro && !isPro && <ProBadge />}
                      </>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* Divider */}
        <div className="mx-3 border-t border-slate-100" />

        {/* Conversations section */}
        <div className="flex-1 px-2 pt-3 pb-3">
          {collapsed ? (
            <button
              onClick={onNewChat}
              className="mb-2 flex w-full items-center justify-center rounded-lg p-2.5 text-slate-400 hover:bg-slate-50 hover:text-slate-700 transition-colors duration-200"
              aria-label="Nueva conversación"
            >
              <Plus className="w-4 h-4" strokeWidth={1.5} />
            </button>
          ) : (
            <button
              onClick={onNewChat}
              className="mb-3 flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition-all duration-200 hover:bg-blue-700"
            >
              <Plus className="h-4 w-4" strokeWidth={1.5} />
              Nueva conversación
            </button>
          )}

          {!collapsed && remainingChats !== null && remainingChats !== -1 && (
            <p className="mb-2 px-2 text-xs text-slate-400">
              {remainingChats} consultas restantes hoy
            </p>
          )}

          {conversations.length > 0 && !collapsed && (
            <>
              <p className="mb-1.5 px-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                Conversaciones
              </p>
              <ul className="space-y-0.5">
                {conversations.map((conv) => (
                  <li key={conv.id}>
                    <div
                      className={`group flex w-full items-center gap-2 rounded-lg px-2 py-2 transition-all duration-200 ${
                        currentId === conv.id
                          ? "bg-slate-100 text-slate-900"
                          : "hover:bg-slate-50"
                      }`}
                    >
                      <button
                        onClick={() => onSelect(conv.id)}
                        className="flex items-center gap-2.5 flex-1 min-w-0 text-left"
                      >
                        <MessageSquare className="h-3.5 w-3.5 flex-shrink-0 text-slate-400" strokeWidth={1.5} />
                        <div className="min-w-0 flex-1">
                          <p className="truncate text-sm font-medium text-slate-700">{conv.title}</p>
                          <p className="truncate text-xs text-slate-400">
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
