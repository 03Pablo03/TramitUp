"use client";

import Link from "next/link";
import { getCategoryDef, MessageSquare, Bell } from "@/lib/icons";

export interface CaseData {
  id: string;
  title: string;
  category?: string | null;
  status: "open" | "resolved" | "archived";
  summary?: string | null;
  created_at: string;
  conversation_count?: number;
  alert_count?: number;
}

const STATUS_CONFIG = {
  open: { label: "Abierto", bg: "bg-green-100", text: "text-green-700" },
  resolved: { label: "Resuelto", bg: "bg-blue-100", text: "text-blue-700" },
  archived: { label: "Archivado", bg: "bg-slate-100", text: "text-slate-500" },
};


export function CaseCard({ data }: { data: CaseData }) {
  const statusCfg = STATUS_CONFIG[data.status] ?? STATUS_CONFIG.open;
  const catDef = getCategoryDef(data.category);
  const CatIcon = catDef.icon;
  const categoryLabel = data.category ? catDef.label : null;
  const date = new Date(data.created_at).toLocaleDateString("es-ES", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });

  return (
    <Link href={`/casos/${data.id}`} className="block group">
      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:border-[var(--primary)] hover:shadow-md hover:-translate-y-0.5">
        <div className="flex items-start gap-3">
          <div className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-xl ${catDef.bg}`}>
            <CatIcon className={`h-5 w-5 ${catDef.color}`} />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="truncate font-semibold text-slate-900 group-hover:text-[var(--primary)] transition-colors">
                {data.title}
              </h3>
              <span className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${statusCfg.bg} ${statusCfg.text}`}>
                {statusCfg.label}
              </span>
            </div>

            <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-500">
              {categoryLabel && (
                <span className="rounded-full bg-slate-100 px-2 py-0.5 font-medium capitalize">
                  {categoryLabel}
                </span>
              )}
              <span>{date}</span>
            </div>

            {data.summary && (
              <p className="mt-2 line-clamp-2 text-sm text-slate-500">{data.summary}</p>
            )}

            <div className="mt-3 flex gap-4 text-xs text-slate-400">
              {(data.conversation_count ?? 0) > 0 && (
                <span className="flex items-center gap-1">
                  <MessageSquare className="h-3.5 w-3.5" /> {data.conversation_count} conversación{data.conversation_count !== 1 ? "es" : ""}
                </span>
              )}
              {(data.alert_count ?? 0) > 0 && (
                <span className="flex items-center gap-1 text-amber-500">
                  <Bell className="h-3.5 w-3.5" /> {data.alert_count} alerta{data.alert_count !== 1 ? "s" : ""}
                </span>
              )}
              {(data.conversation_count ?? 0) === 0 && (data.alert_count ?? 0) === 0 && (
                <span>Sin elementos vinculados aún</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}
