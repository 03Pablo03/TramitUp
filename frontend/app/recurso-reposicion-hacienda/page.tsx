import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Recurso de reposición ante Hacienda (2026)",
  description:
    "Guía para recurrir liquidaciones, sanciones o actos de la AEAT. Ley 58/2003 LGT. Plazo 1 mes.",
  openGraph: {
    title: "Recurso reposición Hacienda | Tramitup",
    description: "Recurso de reposición ante la AEAT según la Ley General Tributaria.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Recurso de reposición ante Hacienda (2026)"
      description="Guía para recurrir liquidaciones, sanciones o actos de la AEAT. Ley 58/2003 LGT. Plazo 1 mes."
      h1="Recurso de reposición ante Hacienda (2026)"
      intro="El recurso de reposición es el primer recurso que debes interponer contra actos de la Agencia Tributaria (liquidaciones, sanciones, requerimientos). La Ley 58/2003 General Tributaria establece que debe presentarse en el plazo de un mes desde la notificación del acto, ante el mismo órgano que lo dictó. Si el recurso es desestimado (o no se resuelve en 1 mes), puedes acudir a la vía económico-administrativa o contenciosa."
      steps={[
        {
          title: "Comprueba el plazo",
          content: "1 mes desde la notificación del acto. Cuenta desde el día siguiente a la notificación.",
        },
        {
          title: "Presenta el recurso de reposición",
          content: "Dirigido al órgano que dictó el acto (Delegación de Hacienda, AEAT). Indica motivos y solicita la revocación.",
        },
        {
          title: "Respuesta de Hacienda",
          content: "Tienen 1 mes para resolver. Si no lo hacen, puedes entender desestimado y acudir a reclamación económico-administrativa.",
        },
      ]}
      lawRefs={[
        "Ley 58/2003 General Tributaria (LGT)",
        "Art. 232 y ss. (recurso de reposición)",
      ]}
      ctaText="Genera tu modelo de recurso gratis →"
      faqs={[
        {
          q: "¿Puedo presentar el recurso online?",
          a: "Sí, a través del portal de la AEAT o de la sede electrónica de la Agencia Tributaria.",
        },
        {
          q: "¿Qué pasa si no presento el recurso a tiempo?",
          a: "Si no presentas en plazo, el acto se convierte en firme y pierdes la posibilidad de recurrir por esa vía.",
        },
      ]}
    />
  );
}
