import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Cómo recurrir una multa de tráfico (2026)",
  description:
    "Guía para recurrir multas de tráfico. Plazo 20 días hábiles. RDL 6/2015 LSV. Modelo de recurso gratis.",
  openGraph: {
    title: "Recurrir multa de tráfico | Tramitup",
    description: "Recurso de multa de tráfico en 20 días hábiles según RDL 6/2015.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Cómo recurrir una multa de tráfico (2026)"
      description="Guía para recurrir multas de tráfico. Plazo 20 días hábiles. RDL 6/2015 LSV. Modelo de recurso gratis."
      h1="Cómo recurrir una multa de tráfico (2026)"
      intro="Si crees que una multa de tráfico es injusta o incorrecta, puedes recurrirla. El Real Decreto Legislativo 6/2015 (Ley de Seguridad Vial) establece que el recurso de reposición debe presentarse ante el órgano que impuso la sanción en un plazo de 20 días hábiles desde la notificación. Si el recurso es desestimado, puedes acudir a la vía contencioso-administrativa."
      steps={[
        {
          title: "Comprueba el plazo",
          content: "20 días hábiles desde que recibiste la notificación. Cuentan solo días laborables.",
        },
        {
          title: "Presenta el recurso de reposición",
          content: "Dirigido al órgano sancionador (DGT, ayuntamiento, etc.). Indica los motivos y adjunta pruebas si las tienes.",
        },
        {
          title: "Espera la resolución",
          content: "El órgano tiene 1 mes para resolver. Si no lo hace, se entiende desestimado y puedes recurrir ante los tribunales.",
        },
      ]}
      lawRefs={[
        "Real Decreto Legislativo 6/2015, Ley de Seguridad Vial",
        "Art. 97 (recurso de reposición)",
      ]}
      ctaText="Genera tu modelo de recurso gratis →"
      faqs={[
        {
          q: "¿Qué días cuentan como hábiles?",
          a: "Solo días laborables (lunes a viernes, excluyendo festivos). El día de notificación no cuenta.",
        },
        {
          q: "¿Puedo recurrir si ya he pagado la multa?",
          a: "Sí, si pagaste en los 20 días hábiles para obtener la reducción. Aún puedes reclamar la devolución si consideras que la multa es indebida.",
        },
      ]}
    />
  );
}
