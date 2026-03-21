import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mis expedientes legales",
  description:
    "Organiza todas tus reclamaciones y problemas legales en expedientes propios. Agrupa conversaciones, documentos y alertas de plazo en un mismo sitio para no perder ningún detalle.",
  openGraph: {
    title: "Mis expedientes legales | TramitUp",
    description:
      "Gestiona tus reclamaciones como un profesional. Crea expedientes, vincula conversaciones y controla los plazos.",
    url: "https://tramitup.com/casos",
  },
  robots: {
    index: false,
    follow: false,
  },
};

export default function CasosLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
