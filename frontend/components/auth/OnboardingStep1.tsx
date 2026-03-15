"use client";

type OnboardingStep1Props = {
  onNext: () => void;
};

export function OnboardingStep1({ onNext }: OnboardingStep1Props) {
  return (
    <div className="mx-auto max-w-lg space-y-8 text-center">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">Bienvenido a Tramitup</h1>
        <p className="mt-2 text-slate-600">Tu servicio de información jurídica</p>
      </div>
      <p className="text-left text-slate-600">
        Tramitup te explica qué dice la normativa española sobre tu situación y te
        ayuda a entender tus opciones. No somos abogados — somos información clara
        y accesible.
      </p>
      <button
        type="button"
        onClick={() => onNext()}
        className="w-full rounded-xl bg-[#1A56DB] py-3 font-medium text-white hover:bg-[#1542a8]"
      >
        Empezar →
      </button>
    </div>
  );
}
