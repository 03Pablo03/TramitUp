"use client";

import Link from "next/link";
import { Bell } from "@/lib/icons";

export type AlertNavBadgeProps = {
  count: number;
};

export function AlertNavBadge({ count }: AlertNavBadgeProps) {
  if (count <= 0) return null;

  return (
    <Link
      href="/alerts"
      className="relative inline-flex items-center gap-1 text-slate-600 hover:text-slate-800"
    >
      <Bell className="h-5 w-5" />
      <span
        className="absolute -right-2 -top-1 flex h-5 min-w-[20px] items-center justify-center rounded-full bg-red-500 px-1.5 text-xs font-bold text-white"
      >
        {count > 99 ? "99+" : count}
      </span>
    </Link>
  );
}
