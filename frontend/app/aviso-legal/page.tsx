import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Aviso legal",
  description: "Aviso legal y condiciones de uso del servicio Tramitup.",
};

const disclaimer =
  "Tramitup es un servicio de información jurídica basado en normativa pública española. No prestamos asesoramiento legal, no somos abogados y no garantizamos resultados. Los modelos de escritos generados son orientativos y deben ser revisados por el usuario antes de su presentación. Para situaciones complejas, recomendamos consultar con un profesional.";

export default function AvisoLegalPage() {
  return (
    <div className="min-h-screen bg-white">
      <header className="border-b border-[var(--border)] bg-white px-4 py-4">
        <div className="mx-auto flex max-w-3xl items-center justify-between">
          <span className="font-display text-lg font-bold tracking-tight text-[var(--primary)]">
            TramitUp
          </span>
          <Link href="/" className="text-sm text-[var(--primary)] hover:underline">
            Volver
          </Link>
        </div>
      </header>
      <main className="mx-auto max-w-3xl px-4 py-16">
        <h1 className="font-display text-3xl font-bold text-[var(--text-dark)]">
          Aviso legal
        </h1>
        <div className="mt-8 space-y-6 text-[var(--text-body)]">
          <p>{disclaimer}</p>
          <p>
            Tramitup opera como servicio de información. Los contenidos se generan a
            partir de normativa pública española vigente y tienen carácter
            exclusivamente informativo.
          </p>
          <p>
            Para cualquier consulta:{" "}
            <a href="mailto:soportetramitup@gmail.com" className="text-[var(--primary)] hover:underline">
              soportetramitup@gmail.com
            </a>
          </p>
        </div>
      </main>
    </div>
  );
}
