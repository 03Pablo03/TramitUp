import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Cómo reclamar una factura de luz incorrecta (2026)",
  description:
    "Guía para reclamar facturas incorrectas a la comercializadora. Ley 24/2013, CNMC. Modelo de reclamación gratis.",
  openGraph: {
    title: "Reclamar factura luz incorrecta | Tramitup",
    description: "Reclama facturas de luz incorrectas ante la comercializadora y la CNMC.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Cómo reclamar una factura de luz incorrecta (2026)"
      description="Guía para reclamar facturas incorrectas a la comercializadora. Ley 24/2013, CNMC. Modelo de reclamación gratis."
      h1="Cómo reclamar una factura de luz incorrecta (2026)"
      intro="Si tu factura de luz no corresponde a tu consumo real, tienes derecho a reclamar. La Ley 24/2013 del sector eléctrico y el Real Decreto 1955/2000 establecen el procedimiento. Primero debes contactar con tu comercializadora (Endesa, Iberdrola, Naturgy, etc.). Si no resuelven en un plazo razonable, puedes reclamar ante la CNMC (Comisión Nacional de los Mercados y la Competencia)."
      steps={[
        {
          title: "Revisa tu factura y consumo",
          content: "Compara con lecturas anteriores, comprueba que el número de contrato y la potencia son correctos.",
        },
        {
          title: "Contacta con la comercializadora",
          content: "Presenta una reclamación por escrito (email o carta). Adjunta justificantes si los tienes.",
        },
        {
          title: "Si no te responden o no rectifican",
          content: "Puedes reclamar ante la CNMC. Tienes 2 años desde el conocimiento del hecho.",
        },
      ]}
      lawRefs={[
        "Ley 24/2013 del sector eléctrico",
        "Real Decreto 1955/2000",
        "CNMC: cnmc.es",
      ]}
      faqs={[
        {
          q: "¿Qué plazo tiene la empresa para responder?",
          a: "Suele ser de 1-2 meses. Si no responden, puedes escalar a la CNMC.",
        },
        {
          q: "¿Puedo reclamar facturas antiguas?",
          a: "El plazo de reclamación suele ser de 2 años desde que conociste el error.",
        },
      ]}
    />
  );
}
