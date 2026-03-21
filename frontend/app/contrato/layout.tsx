import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Analiza tu contrato: cláusulas abusivas y derechos",
  description:
    "Sube tu contrato de alquiler o laboral y TramitUp detecta automáticamente las cláusulas abusivas o ilegales según la LAU y el Estatuto de los Trabajadores. Análisis con IA, resultado inmediato.",
  keywords: [
    "analizar contrato alquiler cláusulas abusivas",
    "cláusulas nulas contrato alquiler",
    "LAU cláusulas ilegales",
    "analizar contrato laboral",
    "cláusulas abusivas trabajador",
    "revisar contrato online",
    "derechos inquilino España",
    "contrato alquiler ilegal fianza",
  ],
  openGraph: {
    title: "Analiza tu contrato y detecta cláusulas abusivas | TramitUp",
    description:
      "Sube tu contrato de alquiler o laboral. La IA detecta qué cláusulas son ilegales o abusivas y qué puedes reclamar.",
    url: "https://tramitup.com/contrato",
  },
};

export default function ContratoLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
