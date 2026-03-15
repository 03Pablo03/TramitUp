import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Modelo de carta de disconformidad con el finiquito (2026)",
  description:
    "Plantilla de carta para impugnar un finiquito incorrecto. Estatuto de los Trabajadores. Genera tu modelo gratis.",
  openGraph: {
    title: "Modelo carta finiquito | Tramitup",
    description: "Carta de disconformidad con el finiquito según el Estatuto de los Trabajadores.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Modelo de carta de disconformidad con el finiquito (2026)"
      description="Plantilla de carta para impugnar un finiquito incorrecto. Estatuto de los Trabajadores. Genera tu modelo gratis."
      h1="Modelo de carta de disconformidad con el finiquito (2026)"
      intro="Si crees que tu finiquito no está bien calculado, puedes firmarlo «en disconformidad» y presentar una reclamación. El Estatuto de los Trabajadores (RDL 2/2015) regula el finiquito y los conceptos que debe incluir: salarios pendientes, vacaciones no disfrutadas, indemnización si procede, etc. Tienes 20 días hábiles desde la firma del finiquito para impugnar ante el Juzgado de lo Social."
      steps={[
        {
          title: "Revisa el desglose del finiquito",
          content: "Comprueba que incluye salario, vacaciones, indemnización (si hay despido), partes proporcionales.",
        },
        {
          title: "Firma en disconformidad si no estás de acuerdo",
          content: "Puedes firmar el finiquito «recibido en disconformidad» para no perder el cobro y reservar tu derecho a reclamar.",
        },
        {
          title: "Presenta reclamación en 20 días hábiles",
          content: "Debes demandar ante el Juzgado de lo Social en el plazo de 20 días hábiles desde la firma del finiquito.",
        },
      ]}
      lawRefs={[
        "Real Decreto Legislativo 2/2015, Estatuto de los Trabajadores",
        "Art. 80 (extinción) y desarrollo reglamentario",
      ]}
      ctaText="Genera tu carta de disconformidad gratis →"
      faqs={[
        {
          q: "¿Pierdo el dinero si firmo en disconformidad?",
          a: "No. Puedes cobrar el finiquito y a la vez reservar tu derecho a reclamar la diferencia ante el Juzgado.",
        },
        {
          q: "¿Cuándo prescriben las cantidades del finiquito?",
          a: "Las acciones para reclamar salarios prescriben a el año desde que debían ser pagadas.",
        },
      ]}
    />
  );
}
