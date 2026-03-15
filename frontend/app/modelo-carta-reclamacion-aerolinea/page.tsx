import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Modelo de carta de reclamación a aerolínea (2026)",
  description:
    "Plantilla y modelo de reclamación a aerolínea por vuelo cancelado o retrasado. Basado en EU 261/2004. Descarga gratis.",
  openGraph: {
    title: "Modelo de carta reclamación aerolínea | Tramitup",
    description: "Modelo de reclamación por vuelo cancelado/retrasado según EU 261/2004.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Modelo de carta de reclamación a aerolínea (2026)"
      description="Plantilla y modelo de reclamación a aerolínea por vuelo cancelado o retrasado. Basado en EU 261/2004. Descarga gratis."
      h1="Modelo de carta de reclamación a aerolínea (2026)"
      intro="Necesitas un escrito formal para reclamar la compensación por vuelo cancelado o retrasado a tu aerolínea. Según el Reglamento EU 261/2004, la reclamación debe incluir: datos del vuelo, fecha, importe reclamado y fundamento legal. Tramitup genera un modelo personalizado con tus datos listo para enviar por carta o email."
      steps={[
        {
          title: "Incluye los datos del vuelo",
          content: "Número de vuelo, fecha, aeropuertos de origen y destino, número de reserva.",
        },
        {
          title: "Indica la compensación solicitada",
          content: "250€, 400€ o 600€ según la distancia del trayecto según el Reglamento.",
        },
        {
          title: "Cita la normativa",
          content:
            "Reglamento (CE) 261/2004, artículos 5 (cancelación) y 6 (retraso). La aerolínea debe pagar en 7 días.",
        },
      ]}
      lawRefs={["Reglamento (CE) 261/2004", "Art. 5 (cancelación), Art. 6 (retraso)"]}
      ctaText="Genera tu modelo de reclamación gratis →"
      faqs={[
        {
          q: "¿Puedo enviar el modelo por email?",
          a: "Sí. La mayoría de aerolíneas aceptan reclamaciones por email. Guarda el acuse de recibo.",
        },
        {
          q: "¿El modelo es válido para cualquier aerolínea?",
          a: "Sí, para vuelos que salgan o lleguen a la UE. Aplica a Iberia, Ryanair, Vueling, etc.",
        },
      ]}
    />
  );
}
