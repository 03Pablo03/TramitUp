"use client";

/**
 * Inline PRO badge — small pill used next to feature names in navigation.
 */
export function ProBadge() {
  return (
    <span className="inline-flex items-center gap-0.5 rounded-full bg-gradient-to-r from-amber-400 to-orange-500 px-2 py-0.5 text-[10px] font-bold uppercase leading-none text-white shadow-sm">
      PRO
    </span>
  );
}

interface ProButtonProps {
  onClick: () => void;
  disabled?: boolean;
  label?: string;
  size?: "sm" | "md";
}

/**
 * Standardized "Hazte PRO" CTA button used across the app.
 */
export function ProButton({
  onClick,
  disabled = false,
  label = "Hazte PRO",
  size = "md",
}: ProButtonProps) {
  const sizeClasses =
    size === "sm"
      ? "px-3 py-1.5 text-xs"
      : "px-5 py-2.5 text-sm";

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`inline-flex items-center gap-1.5 rounded-xl bg-gradient-to-r from-amber-400 to-orange-500 font-bold text-white shadow-md transition-all hover:from-amber-500 hover:to-orange-600 hover:shadow-lg disabled:opacity-70 ${sizeClasses}`}
    >
      <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
      </svg>
      {label}
    </button>
  );
}
