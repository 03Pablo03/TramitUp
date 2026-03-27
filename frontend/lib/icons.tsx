import {
  Briefcase,
  Home,
  ShoppingCart,
  Users,
  Car,
  Landmark,
  Calculator,
  Scale,
  ClipboardList,
  Plane,
  Lightbulb,
  MessageSquare,
  Bell,
  FileText,
  FolderOpen,
  Search,
  Lock,
  Check,
  CheckCircle,
  X,
  Info,
  Calendar,
  Eye,
  Star,
  Circle,
  Hand,
  Monitor,
  GraduationCap,
  Sunset,
  Shirt,
  AlertTriangle,
  Clock,
  FileSignature,
  ArrowRight,
  type LucideProps,
} from "lucide-react";
import type { ComponentType } from "react";

// ── Category icon map ──────────────────────────────────────────────
// Replaces the emoji CATEGORY_ICONS maps duplicated across many files.

type CategoryKey =
  | "laboral"
  | "vivienda"
  | "consumo"
  | "familia"
  | "trafico"
  | "administrativo"
  | "fiscal"
  | "penal"
  | "otro"
  | "reclamaciones"
  | "vuelo"
  | "factura";

interface CategoryDef {
  icon: ComponentType<LucideProps>;
  color: string;       // Tailwind text color
  bg: string;          // Tailwind bg color (light)
  label: string;
}

const CATEGORY_MAP: Record<string, CategoryDef> = {
  laboral:         { icon: Briefcase,     color: "text-blue-600",    bg: "bg-blue-100",    label: "Laboral" },
  vivienda:        { icon: Home,          color: "text-emerald-600", bg: "bg-emerald-100", label: "Vivienda" },
  consumo:         { icon: ShoppingCart,  color: "text-orange-500",  bg: "bg-orange-100",  label: "Consumo" },
  familia:         { icon: Users,         color: "text-purple-600",  bg: "bg-purple-100",  label: "Familia" },
  trafico:         { icon: Car,           color: "text-red-500",     bg: "bg-red-100",     label: "Tráfico" },
  administrativo:  { icon: Landmark,      color: "text-slate-600",   bg: "bg-slate-100",   label: "Administrativo" },
  fiscal:          { icon: Calculator,    color: "text-amber-600",   bg: "bg-amber-100",   label: "Fiscal" },
  penal:           { icon: Scale,         color: "text-rose-600",    bg: "bg-rose-100",    label: "Penal" },
  otro:            { icon: ClipboardList, color: "text-slate-500",   bg: "bg-slate-100",   label: "Otro" },
  reclamaciones:   { icon: Plane,         color: "text-sky-500",     bg: "bg-sky-100",     label: "Reclamaciones" },
  vuelo:           { icon: Plane,         color: "text-sky-500",     bg: "bg-sky-100",     label: "Vuelo" },
  factura:         { icon: Lightbulb,     color: "text-yellow-500",  bg: "bg-yellow-100",  label: "Factura" },
};

const DEFAULT_CATEGORY: CategoryDef = {
  icon: ClipboardList,
  color: "text-slate-500",
  bg: "bg-slate-100",
  label: "Otro",
};

export function getCategoryDef(category: string | undefined | null): CategoryDef {
  if (!category) return DEFAULT_CATEGORY;
  return CATEGORY_MAP[category.toLowerCase()] ?? DEFAULT_CATEGORY;
}

interface CategoryIconProps extends LucideProps {
  category: string | undefined | null;
}

export function CategoryIcon({ category, className, ...props }: CategoryIconProps) {
  const def = getCategoryDef(category);
  const Icon = def.icon;
  return <Icon className={className ?? `h-5 w-5 ${def.color}`} {...props} />;
}

// ── Status dots (alerts) ───────────────────────────────────────────

type UrgencyLevel = "past" | "urgent" | "warning" | "normal" | "inactive";

const URGENCY_COLORS: Record<string, string> = {
  past:     "fill-slate-400 text-slate-400",
  inactive: "fill-slate-400 text-slate-400",
  urgent:   "fill-red-500 text-red-500",
  warning:  "fill-amber-500 text-amber-500",
  normal:   "fill-blue-500 text-blue-500",
};

interface StatusDotProps extends LucideProps {
  urgency: string;
}

export function StatusDot({ urgency, className, ...props }: StatusDotProps) {
  const colors = URGENCY_COLORS[urgency] ?? URGENCY_COLORS.normal;
  return <Circle className={className ?? `h-3 w-3 ${colors}`} {...props} />;
}

// ── Re-exports for convenience ─────────────────────────────────────

export {
  Briefcase,
  Home,
  ShoppingCart,
  Users,
  Car,
  Landmark,
  Calculator,
  Scale,
  ClipboardList,
  Plane,
  Lightbulb,
  MessageSquare,
  Bell,
  FileText,
  FolderOpen,
  Search,
  Lock,
  Check,
  CheckCircle,
  X,
  Info,
  Calendar,
  Eye,
  Star,
  Circle,
  Hand,
  Monitor,
  GraduationCap,
  Sunset,
  Shirt,
  AlertTriangle,
  Clock,
  FileSignature,
  ArrowRight,
};
