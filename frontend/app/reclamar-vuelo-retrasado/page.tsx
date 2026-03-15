import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Cómo reclamar un vuelo retrasado en España (2026)",
  description:
    "Guía para reclamar compensación por vuelo retrasado según EU 261/2004. Hasta 600€ según distancia.",
  openGraph: {
    title: "Cómo reclamar un vuelo retrasado en España (2026)",
    description: "Reclama tu compensación por retraso según el Reglamento UE 261/2004.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Cómo reclamar un vuelo retrasado en España (2026)"
      description="Guía para reclamar compensación por vuelo retrasado +3h. Reglamento UE 261/2004. Hasta 600€. Modelo gratis."
      h1="Cómo reclamar un vuelo retrasado en España (2026)"
      intro="Cuando un vuelo llega con más de 3 horas de retraso al destino final (o se cancela en el último momento), el Reglamento EU 261/2004 prevé compensación económica. Las cuantías son las mismas que en cancelación: 250€, 400€ o 600€ según la distancia. El retraso debe deberse a causas imputables a la compañía, no a circunstancias extraordinarias."
      steps={[
        {
          title: "Comprueba que cumples los requisitos",
          content:
            "Retraso de al menos 3 horas en la llegada al destino final. El retraso no debe deberse a circunstancias extraordinarias (tormentas, huelga de controladores, etc.).",
        },
        {
          title: "Presenta la reclamación",
          content:
            "Por escrito a la aerolínea con los datos del vuelo, reserva y fecha. Plazo: 1 año desde el vuelo.",
        },
        {
          title: "Espera respuesta",
          content:
            "La aerolínea tiene 7 días para pagar. Si no responde o rechaza, puedes recurrir a AESA o vía judicial.",
        },
      ]}
      lawRefs={["Reglamento (CE) 261/2004", "Real Decreto 389/2016"]}
      faqs={[
        {
          q: "¿Cuánto retraso cuenta?",
          a: "Debe ser de al menos 3 horas en la llegada al aeropuerto de destino final para vuelos de más de 3.500 km, o proporcional en trayectos más cortos.",
        },
        {
          q: "¿Qué son circunstancias extraordinarias?",
          a: "Motivos de seguridad, condiciones meteorológicas que impiden el vuelo, huelgas que afecten al servicio. La sobreventa o motivos organizativos no son extraordinarios.",
        },
      ]}
    />
  );
}
