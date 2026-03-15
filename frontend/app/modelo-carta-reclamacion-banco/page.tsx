import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Modelo de carta de reclamación al banco (2026)",
  description:
    "Plantilla de reclamación a banco o entidad financiera. Ley 7/1998, Banco de España. Descarga gratis.",
  openGraph: {
    title: "Modelo carta reclamación banco | Tramitup",
    description: "Modelo de reclamación ante el banco y Banco de España.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Modelo de carta de reclamación al banco (2026)"
      description="Plantilla de reclamación a banco o entidad financiera. Ley 7/1998, Banco de España. Descarga gratis."
      h1="Modelo de carta de reclamación al banco (2026)"
      intro="Para reclamar a tu banco (comisiones indebidas, cláusulas abusivas, cobros incorrectos) debes enviar una reclamación formal. Primero a la propia entidad; si no te resuelven, puedes reclamar ante el Servicio de Reclamaciones del Banco de España. La Ley 7/1998 de condiciones generales de la contratación y la Ley 16/2011 de contratos de crédito regulan tus derechos."
      steps={[
        {
          title: "Reclamación a la entidad",
          content: "Presenta por escrito tu reclamación con los datos de la operación, motivos y documentación.",
        },
        {
          title: "Respuesta del banco",
          content: "La entidad debe responder en un plazo razonable (suele ser 2 meses).",
        },
        {
          title: "Reclamación ante el Banco de España",
          content: "Si no te satisfacen, puedes reclamar gratuitamente ante el Servicio de Reclamaciones del BdE.",
        },
      ]}
      lawRefs={[
        "Ley 7/1998 de condiciones generales de la contratación",
        "Ley 16/2011 de contratos de crédito inmobiliario",
        "Banco de España: reclamaciones.bde.es",
      ]}
      ctaText="Genera tu modelo de reclamación gratis →"
      faqs={[
        {
          q: "¿Hay plazo para reclamar al banco?",
          a: "El plazo general de prescripción es de 5 años para reclamar cantidades indebidamente cobradas.",
        },
        {
          q: "¿La reclamación al Banco de España tiene coste?",
          a: "No. El Servicio de Reclamaciones del BdE es gratuito para el consumidor.",
        },
      ]}
    />
  );
}
