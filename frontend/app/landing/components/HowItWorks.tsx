import Link from "next/link";

const steps = [
  {
    num: "①",
    title: "Describe tu situación",
    desc: "Escribe con tus propias palabras. Sin formularios. Sin elegir categorías. Solo cuéntanos qué pasó.",
    icon: "💬",
  },
  {
    num: "②",
    title: "Entendemos qué dice la normativa",
    desc: "Identificamos la legislación aplicable y te explicamos tus opciones en lenguaje claro, con referencias legales reales.",
    icon: "📋",
  },
  {
    num: "③",
    title: "Obtienes lo que necesitas",
    desc: "Guía paso a paso del proceso, plazos importantes y modelo de escrito personalizado listo para presentar.",
    icon: "✅",
  },
];

export function HowItWorks() {
  return (
    <section id="como-funciona" className="scroll-mt-20 bg-white px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
          Cómo funciona
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
          Tres pasos para entender tus derechos y actuar con información
        </p>
        <div className="mt-16 grid gap-12 md:grid-cols-3">
          {steps.map((step) => (
            <div
              key={step.num}
              className="rounded-2xl border border-[var(--border)] bg-white p-8 shadow-sm transition-shadow hover:shadow-md"
            >
              <div className="mb-4 text-4xl">{step.icon}</div>
              <p className="text-sm font-semibold text-[var(--primary)]">{step.num}</p>
              <h3 className="mt-2 font-display text-xl font-semibold text-[var(--text-dark)]">
                {step.title}
              </h3>
              <p className="mt-3 text-[var(--text-body)]">{step.desc}</p>
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <Link
            href="/login"
            className="inline-flex rounded-xl bg-[var(--primary)] px-6 py-3 font-semibold text-white hover:bg-[var(--primary-dark)]"
          >
            Empezar ahora →
          </Link>
        </div>
      </div>
    </section>
  );
}
