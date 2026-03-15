"use client";

const CATEGORY_ICONS: Record<string, string> = {
  reclamaciones: "✈️",
  laboral: "💼",
  vivienda: "🏠",
  burocracia_general: "📋",
  otro: "📌",
};

const CATEGORY_LABELS: Record<string, string> = {
  reclamaciones: "Reclamación",
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
  const icon = CATEGORY_ICONS[category] || "📌";
  const label = subcategory
    ? `${CATEGORY_LABELS[category] || category} · ${subcategory}`
    : (CATEGORY_LABELS[category] || category);
  return (
    <span className="inline-flex items-center gap-1 rounded-full bg-blue-50 border border-blue-200 px-3 py-1 text-xs font-medium text-blue-700">
      <span>{icon}</span>
      <span>{label}</span>
    </span>
  );
}
