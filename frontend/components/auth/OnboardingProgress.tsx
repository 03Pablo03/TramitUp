"use client";

type OnboardingProgressProps = {
  step: number;
  total?: number;
};

export function OnboardingProgress({ step, total = 3 }: OnboardingProgressProps) {
  return (
    <div className="mb-8">
      <p className="mb-2 text-sm font-medium text-slate-600">
        Paso {step} de {total}
      </p>
      <div className="flex gap-2">
        {Array.from({ length: total }).map((_, i) => (
          <div
            key={i}
            className={`h-1.5 flex-1 rounded-full ${
              i + 1 <= step ? "bg-[#1A56DB]" : "bg-slate-200"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
