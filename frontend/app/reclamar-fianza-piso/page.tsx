import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Cómo reclamar la devolución de la fianza del piso (2026)",
  description:
    "Guía para reclamar la fianza al arrendador. LAU 29/1994. Plazo legal 1 mes. Modelo de reclamación gratis.",
  openGraph: {
    title: "Reclamar fianza del piso | Tramitup",
    description: "Reclama la devolución de la fianza según la LAU. Plazo: 1 mes.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Cómo reclamar la devolución de la fianza del piso (2026)"
      description="Guía para reclamar la fianza al arrendador. LAU 29/1994. Plazo legal 1 mes. Modelo de reclamación gratis."
      h1="Cómo reclamar la devolución de la fianza del piso (2026)"
      intro="La Ley de Arrendamientos Urbanos (LAU 29/1994) establece que el arrendador debe devolver la fianza en el plazo de un mes desde la entrega de las llaves. Si no lo hace, puedes reclamar por escrito exigiendo la devolución más los intereses legales. La fianza no puede retenerse sin justificación: solo por daños reales acreditados que superen el desgaste normal."
      steps={[
        {
          title: "Deja el piso en buen estado",
          content: "Haz entrega de llaves con acta o documento acreditativo. El arrendador debe inspeccionar y señalar desperfectos si los hay.",
        },
        {
          title: "Exige la devolución por escrito",
          content: "Si pasan 30 días sin devolución, envía una reclamación formal (carta o burofax) exigiendo la fianza más intereses.",
        },
        {
          title: "Si no responde",
          content:
            "Puedes interponer demanda en el Juzgado de Primera Instancia. La prescripción es de 3 años para reclamar la fianza.",
        },
      ]}
      lawRefs={[
        "Ley 29/1994 de Arrendamientos Urbanos (LAU)",
        "Art. 36 (obligación de devolver la fianza en 1 mes)",
      ]}
      ctaText="Genera tu modelo de reclamación gratis →"
      faqs={[
        {
          q: "¿Cuánto tiempo tiene el casero para devolver la fianza?",
          a: "Un mes desde la entrega de las llaves. Pasado ese plazo puedes reclamar intereses de demora.",
        },
        {
          q: "¿Puede retener parte por reparaciones?",
          a: "Solo por daños que superen el desgaste normal de uso. Debe acreditarlo con presupuestos o facturas.",
        },
      ]}
    />
  );
}
