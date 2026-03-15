import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Cómo reclamar un vuelo cancelado en España (2026)",
  description:
    "Guía completa para reclamar la compensación por vuelo cancelado según el Reglamento EU 261/2004. Genera tu modelo de reclamación gratis.",
  openGraph: {
    title: "Cómo reclamar un vuelo cancelado en España (2026)",
    description:
      "Guía para reclamar compensación por vuelo cancelado según EU 261/2004. Hasta 600€.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Cómo reclamar un vuelo cancelado en España (2026)"
      description="Guía para reclamar compensación por vuelo cancelado. Reglamento UE 261/2004. Hasta 600€. Modelo de reclamación gratis."
      h1="Cómo reclamar un vuelo cancelado en España (2026)"
      intro="Si tu aerolínea ha cancelado tu vuelo con menos de 14 días de antelación, el Reglamento (CE) 261/2004 de la UE te otorga derecho a compensación económica: 250€ en trayectos cortos (menos de 1.500 km), 400€ en medios (1.500-3.500 km) y 600€ en largos (más de 3.500 km). La aerolínea debe pagarte en un plazo de 7 días. Si no lo hace, puedes reclamar por escrito."
      steps={[
        {
          title: "Recopila los datos",
          content:
            "Número de vuelo, fecha, reserva, importe pagado. La aerolínea debe informarte del motivo de la cancelación.",
        },
        {
          title: "Presenta la reclamación",
          content:
            "Envía una reclamación por escrito (carta o email) a la aerolínea. Tienes hasta 1 año desde la fecha del vuelo para reclamar.",
        },
        {
          title: "Si no responden",
          content:
            "Puedes acudir a la autoridad nacional competente (AESA en España) o plantear demanda judicial.",
        },
      ]}
      lawRefs={[
        "Reglamento (CE) 261/2004 del Parlamento Europeo y del Consejo",
        "Real Decreto 389/2016 (transposición en España)",
      ]}
      faqs={[
        {
          q: "¿Cuánto tiempo tengo para reclamar?",
          a: "Tienes 1 año desde la fecha del vuelo para reclamar la compensación por cancelación.",
        },
        {
          q: "¿La aerolínea puede negarse a pagar?",
          a: "Solo en circunstancias extraordinarias (motivos de seguridad, mal tiempo grave). Una cancelación por overbooking o motivos operativos no exime del pago.",
        },
      ]}
    />
  );
}
