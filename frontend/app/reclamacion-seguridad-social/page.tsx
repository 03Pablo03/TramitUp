import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Reclamación ante la Seguridad Social (2026)",
  description:
    "Guía para reclamar prestaciones, cotizaciones o decisiones ante la Seguridad Social. INSS, SEPE. RDL 8/2015 LGSS.",
  openGraph: {
    title: "Reclamación Seguridad Social | Tramitup",
    description: "Reclama ante INSS, TGSS o SEPE según la LGSS.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Reclamación ante la Seguridad Social (2026)"
      description="Guía para reclamar decisiones del INSS y TGSS. Ley General de la Seguridad Social. Modelo de reclamación previa gratis."
      h1="Reclamación ante la Seguridad Social (2026)"
      intro="Para reclamar una decisión del INSS (prestaciones, incapacidad, jubilación) o de la Tesorería de la Seguridad Social (TGSS), debes presentar una reclamación previa ante el mismo organismo. La Ley General de la Seguridad Social (RDL 8/2015) regula el procedimiento. Tras la reclamación previa, si no estás de acuerdo con la resolución, puedes interponer demanda ante el orden jurisdiccional social."
      steps={[
        {
          title: "Reclamación previa",
          content: "Presenta escrito ante la Dirección Provincial del INSS o la TGSS correspondiente.",
        },
        {
          title: "Plazo de resolución",
          content: "El organismo tiene 45 días para resolver. Si no lo hace, se entiende desestimado.",
        },
        {
          title: "Vía judicial",
          content: "Si desestiman, tienes 30 días para demandar ante el Juzgado de lo Social.",
        },
      ]}
      lawRefs={[
        "Real Decreto Legislativo 8/2015, Ley General de la Seguridad Social",
        "Ley 36/2011 reguladora de la jurisdicción social",
      ]}
      ctaText="Genera tu modelo de reclamación gratis →"
      faqs={[
        {
          q: "¿Ante quién reclamo una prestación denegada?",
          a: "Ante la Dirección Provincial del INSS correspondiente a tu domicilio.",
        },
        {
          q: "¿Y para reclamar al SEPE (paro)?",
          a: "La reclamación va dirigida a la Dirección Provincial del SEPE. El procedimiento es similar.",
        },
      ]}
    />
  );
}
