export function LegalNotice() {
  const disclaimer =
    "Tramitup es un servicio de información jurídica basado en normativa pública española. No prestamos asesoramiento legal, no somos abogados y no garantizamos resultados. Los modelos de escritos generados son orientativos y deben ser revisados por el usuario antes de su presentación. Para situaciones complejas, recomendamos consultar con un profesional.";

  return (
    <section className="bg-[var(--primary-light)] px-4 py-16">
      <div className="mx-auto max-w-4xl">
        <div className="flex gap-4 rounded-xl border border-[var(--primary)]/20 bg-white p-6">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--primary)]/10 text-xl">
            ℹ️
          </div>
          <div>
            <h3 className="font-display text-lg font-semibold text-[var(--text-dark)]">
              Aviso legal
            </h3>
            <p className="mt-2 text-[var(--text-body)]">{disclaimer}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
