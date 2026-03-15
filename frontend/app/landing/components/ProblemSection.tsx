export function ProblemSection() {
  return (
    <section className="bg-[var(--surface)] px-4 py-12 lg:py-14">
      <div className="mx-auto max-w-3xl text-center">
        <p className="font-display text-2xl font-semibold leading-relaxed text-[var(--text-dark)] sm:text-3xl">
          Sabemos lo que sientes cuando abres una notificación de Hacienda. Cuando tu
          casero no te devuelve la fianza. Cuando la aerolínea te cancela el vuelo y no
          sabes qué te corresponde.
        </p>
        <p className="mt-10 text-xl leading-relaxed text-[var(--text-body)]">
          Tramitup no es un chatbot genérico. Es un servicio especializado en la
          normativa española, que te explica exactamente qué dice la ley en tu caso.
        </p>
      </div>
    </section>
  );
}
