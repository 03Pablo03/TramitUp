import type { Metadata } from "next";
import { Playfair_Display, DM_Sans } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import { NotificationProvider } from "@/context/NotificationContext";
import { NotificationContainer } from "@/components/NotificationContainer";
import { ErrorBoundary } from "@/components/ErrorBoundary";

const playfair = Playfair_Display({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-playfair",
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-dm-sans",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://tramitup.com"),
  title: {
    default: "TramitUp — Asistente jurídico para ciudadanos españoles",
    template: "%s | TramitUp",
  },
  description:
    "TramitUp te ayuda a entender tus derechos y actuar. Calcula tu indemnización por despido, analiza cláusulas abusivas en contratos de alquiler o laborales, y gestiona tus reclamaciones en un expediente propio. Gratis y sin registro previo.",
  keywords: [
    "calculadora indemnización despido",
    "calcular finiquito España",
    "analizar contrato alquiler cláusulas abusivas",
    "analizar contrato laboral",
    "reclamación despido improcedente",
    "derechos ciudadano España",
    "asistente jurídico online",
    "información legal gratuita",
    "normativa española",
    "trámites legales",
    "expediente legal",
    "reclamar vuelo cancelado",
    "reclamar factura incorrecta",
  ],
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: "https://tramitup.com",
    siteName: "TramitUp",
    title: "TramitUp — Asistente jurídico para ciudadanos españoles",
    description:
      "Calcula tu indemnización por despido, analiza tu contrato de alquiler o laboral, y gestiona tus reclamaciones. Gratis.",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    site: "@tramitup",
    title: "TramitUp — Asistente jurídico gratuito",
    description:
      "Calcula tu indemnización, analiza cláusulas abusivas en contratos y gestiona tus reclamaciones. Sin letra pequeña.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true },
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" className={`${playfair.variable} ${dmSans.variable}`} suppressHydrationWarning>
      <body className="font-sans antialiased" suppressHydrationWarning>
        <ErrorBoundary>
          <NotificationProvider>
            <AuthProvider>
              {children}
              <NotificationContainer />
            </AuthProvider>
          </NotificationProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}
