"use client";

import { useState } from "react";

const faqs = [
  {
    q: "¿Tramitup es un servicio legal?",
    a: "No. Tramitup es un servicio de información jurídica. Te explicamos qué dice la normativa española vigente y te ofrecemos modelos de escritos orientativos. No prestamos asesoramiento legal ni sustituimos a un abogado. Para casos complejos, recomendamos consultar con un profesional.",
  },
  {
    q: "¿Cuánto cuesta usar Tramitup?",
    a: "Tramitup tiene un plan gratuito con 2 consultas al día. Puedes suscribirte a PRO por 9,99€/mes para consultas ilimitadas, documentos ilimitados y alertas de plazos.",
  },
  {
    q: "¿Puedo usar Tramitup para reclamar a una aerolínea?",
    a: "Sí. Tramitup te explica qué dice el Reglamento UE 261/2004 sobre vuelos cancelados o retrasados y puede generar un modelo de reclamación personalizado para que lo presentes a la aerolínea.",
  },
  {
    q: "¿Los modelos de escritos que genera Tramitup son válidos?",
    a: "Los modelos son orientativos y se basan en la normativa vigente. Debes revisarlos y adaptarlos a tu caso antes de presentarlos. Tramitup no garantiza resultados ni sustituye el criterio de un abogado.",
  },
  {
    q: "¿Qué normativa usa Tramitup para sus respuestas?",
    a: "Usamos normativa española vigente: Reglamento UE 261/2004 (vuelos), Ley 24/2013 (suministros), LAU 29/1994 (alquiler), RDL 2/2015 (laboral), Ley 58/2003 (Hacienda), entre otras. Siempre citamos referencias concretas.",
  },
  {
    q: "¿Tramitup sirve para trámites de la Seguridad Social?",
    a: "Sí. Tramitup cubre prestaciones, paro, bajas, cotizaciones y otros trámites ante el SEPE y la Seguridad Social. Te explicamos el procedimiento y podemos generar modelos de solicitud o reclamación.",
  },
  {
    q: "¿Puedo cancelar la suscripción PRO cuando quiera?",
    a: "Sí. Puedes cancelar la suscripción PRO en cualquier momento desde tu cuenta. Seguirás teniendo acceso hasta el final del periodo de facturación.",
  },
  {
    q: "¿Tramitup funciona para todas las comunidades autónomas?",
    a: "Sí. La normativa estatal que cubrimos aplica en todo el territorio. Para normativa autonómica específica, te indicamos si hay particularidades de tu comunidad.",
  },
  {
    q: "¿Qué diferencia hay entre el plan gratuito y el PRO?",
    a: "Gratis: 2 consultas/día, información normativa, sin documentos descargables. PRO: consultas ilimitadas, modelos de escritos en PDF y Word, alertas de plazos legales, historial completo.",
  },
  {
    q: "¿Tramitup guarda mis datos personales?",
    a: "Guardamos tu historial de conversaciones y documentos generados para ofrecerte el servicio. Puedes revisar nuestra Política de privacidad para más detalles. No compartimos tus datos con terceros.",
  },
];

export function FAQ() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="bg-[var(--surface)] px-4 py-20">
      <div className="mx-auto max-w-3xl">
        <h2 className="font-display text-center text-3xl font-bold text-[var(--text-dark)] sm:text-4xl">
          Preguntas frecuentes
        </h2>
        <div className="mt-12 space-y-2">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="rounded-xl border border-[var(--border)] bg-white"
            >
              <button
                onClick={() => setOpen(open === i ? null : i)}
                className="flex w-full items-center justify-between px-6 py-4 text-left font-medium text-[var(--text-dark)] hover:bg-[var(--surface)]"
              >
                {faq.q}
                <span className="text-xl text-[var(--text-muted)]">
                  {open === i ? "−" : "+"}
                </span>
              </button>
              {open === i && (
                <div className="border-t border-[var(--border)] px-6 py-4 text-[var(--text-body)]">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
