import Link from "next/link";

const cases = [
  {
    icon: "✈️",
    title: "Vuelo cancelado",
    desc: '"Iberia me canceló el vuelo. ¿Qué me corresponde según la ley?"',
    law: "EU 261/2004 · Hasta 600€ de compensación",
  },
  {
    icon: "💡",
    title: "Factura incorrecta",
    desc: '"Endesa me cobró el doble este mes. ¿Cómo lo reclamo?"',
    law: "Ley 24/2013 · Reclamación ante la CNMC",
  },
  {
    icon: "💼",
    title: "Despido",
    desc: '"Me han despedido. ¿Está bien calculado el finiquito?"',
    law: "Estatuto de los Trabajadores · Cálculo automático",
  },
  {
    icon: "🏠",
    title: "Fianza no devuelta",
    desc: '"Me fui del piso hace 3 meses y el casero no devuelve la fianza."',
    law: "LAU 29/1994 · Plazo legal de 1 mes",
  },
  {
    icon: "🏛️",
    title: "Multa de tráfico",
    desc: '"Me pusieron una multa y creo que es injusta. ¿Puedo recurrirla?"',
    law: "RDL 6/2015 · Recurso en 20 días hábiles",
  },
  {
    icon: "📋",
    title: "Hacienda",
    desc: '"La renta me sale a pagar pero creo que hay un error."',
    law: "Ley 58/2003 LGT · Recurso de reposición",
  },
];

export function UseCasesGrid() {
  return (
    <section className="bg-[var(--surface)] px-4 py-20">
      <div className="mx-auto max-w-6xl">
        <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
          Casos de uso
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-center text-[var(--text-body)]">
          Situaciones reales que Tramitup puede ayudarte a resolver
        </p>
        <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {cases.map((c) => (
            <Link
              key={c.title}
              href="/login"
              className="rounded-2xl border border-[var(--border)] bg-white p-6 shadow-sm transition-all hover:border-[var(--primary)]/30 hover:shadow-md"
            >
              <div className="text-3xl">{c.icon}</div>
              <h3 className="mt-4 font-display text-lg font-semibold text-[var(--text-dark)]">
                {c.title}
              </h3>
              <p className="mt-2 text-sm text-[var(--text-body)]">{c.desc}</p>
              <p className="mt-3 text-xs font-medium text-[var(--primary)]">
                {c.law}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
