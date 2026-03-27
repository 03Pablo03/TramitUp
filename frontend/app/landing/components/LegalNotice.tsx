import { Info } from "@/lib/icons";

export function LegalNotice() {
  const disclaimer =
    "Tramitup es un servicio de información jurídica basado en normativa pública española. No prestamos asesoramiento legal, no somos abogados y no garantizamos resultados. Los modelos de escritos generados son orientativos y deben ser revisados por el usuario antes de su presentación. Para situaciones complejas, recomendamos consultar con un profesional.";

  return (
    <section className="bg-slate-50 px-4 py-4">
      <div className="mx-auto max-w-6xl">
        <div className="flex items-start gap-2">
          <Info className="h-4 w-4 shrink-0 text-slate-400 mt-0.5" />
          <p className="text-xs text-slate-500 leading-relaxed">{disclaimer}</p>
        </div>
      </div>
    </section>
  );
}
