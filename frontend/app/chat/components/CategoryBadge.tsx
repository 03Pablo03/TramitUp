"use client";

import { getCategoryDef } from "@/lib/icons";

const CATEGORY_LABELS: Record<string, string> = {
  reclamaciones: "Reclamacion",
  laboral: "Laboral",
  vivienda: "Vivienda",
  burocracia_general: "Burocracia",
  otro: "General",
};

type CategoryBadgeProps = {
  category: string;
  subcategory?: string;
};

export function CategoryBadge({ category, subcategory }: CategoryBadgeProps) {
  const def = getCategoryDef(category);
  const Icon = def.icon;
  const label = subcategory
    ? `${CATEGORY_LABELS[category] || category} · ${subcategory}`
    : (CATEGORY_LABELS[category] || category);
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 border border-blue-200 px-3 py-1 text-xs font-medium text-blue-700">
      <Icon className="h-4 w-4" />
      <span>{label}</span>
    </span>
  );
}
