import type { Metadata } from "next";
import { SEOLandingTemplate } from "../landing/components/SEOLandingTemplate";

export const metadata: Metadata = {
  title: "Calcular finiquito por despido o baja voluntaria (2026)",
  description:
    "Guía para entender cómo se calcula el finiquito. Estatuto de los Trabajadores. Salarios, vacaciones, indemnización.",
  openGraph: {
    title: "Calcular finiquito | Tramitup",
    description: "Cómo se calcula el finiquito según el Estatuto de los Trabajadores.",
  },
};

export default function Page() {
  return (
    <SEOLandingTemplate
      title="Calcular finiquito por despido o baja voluntaria (2026)"
      description="Guía para entender cómo se calcula el finiquito. Estatuto de los Trabajadores. Salarios, vacaciones, indemnización."
      h1="Calcular finiquito por despido o baja voluntaria (2026)"
      intro="El finiquito es el documento que liquida la relación laboral e incluye: salario del mes en curso (parte proporcional), vacaciones no disfrutadas, pluses y extras proporcionales. Si hay despido, además incluye la indemnización según el tipo (improcedente: 33 días por año con tope de 24 mensualidades; objetivo: 20 días por año con tope de 12; etc.). El Estatuto de los Trabajadores (RDL 2/2015) regula cada concepto."
      steps={[
        {
          title: "Salarios pendientes",
          content: "Parte proporcional del salario desde el último cobro hasta la fecha de cese.",
        },
        {
          title: "Vacaciones no disfrutadas",
          content: "Días de vacaciones pendientes según convenio (habitualmente 2,5 días por mes trabajado).",
        },
        {
          title: "Indemnización (si hay despido)",
          content:
            "Según tipo de despido: improcedente 33 días/año (tope 24 mensualidades), objetivo 20 días/año (tope 12).",
        },
      ]}
      lawRefs={[
        "RDL 2/2015 Estatuto de los Trabajadores",
        "Art. 45 (despido colectivo), Art. 53 (objetivo), Art. 56 (improcedente)",
      ]}
      ctaText="Comprueba tu finiquito con Tramitup →"
      faqs={[
        {
          q: "¿Qué incluye el finiquito en una baja voluntaria?",
          a: "Salarios pendientes, vacaciones no disfrutadas, parte proporcional de pagas extras. No indemnización.",
        },
        {
          q: "¿Puedo reclamar si el finiquito está mal?",
          a: "Sí. Tienes 20 días hábiles desde la firma para demandar ante el Juzgado de lo Social.",
        },
      ]}
    />
  );
}
