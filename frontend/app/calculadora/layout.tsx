import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Calculadora de indemnización por despido",
  description:
    "Calcula gratis la indemnización que te corresponde por despido improcedente, despido procedente o fin de contrato temporal. Aplica la fórmula legal española actualizada (ET art. 56 y Ley 3/2012). Resultado instantáneo y desglose por tramos.",
  keywords: [
    "calculadora indemnización despido",
    "despido improcedente cuánto me corresponde",
    "calcular finiquito despido",
    "indemnización 33 días por año",
    "indemnización 45 días por año",
    "reforma laboral 2012 indemnización",
    "ET artículo 56",
    "calculadora laboral España",
  ],
  openGraph: {
    title: "Calculadora de indemnización por despido | TramitUp",
    description:
      "¿Te han despedido? Calcula en segundos cuánto te corresponde según la ley española. Gratis, sin registro.",
    url: "https://tramitup.com/calculadora",
  },
};

export default function CalculadoraLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
