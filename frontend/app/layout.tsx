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
    default: "Tramitup — Entiende tus derechos. Actúa con información.",
    template: "%s | Tramitup",
  },
  description:
    "Servicio de información jurídica para ciudadanos españoles. Explica qué dice la normativa sobre tu situación y genera modelos de escritos personalizados.",
  keywords: [
    "reclamación",
    "trámites",
    "burocracia",
    "normativa española",
    "derechos ciudadano",
  ],
  openGraph: {
    type: "website",
    locale: "es_ES",
    url: "https://tramitup.com",
    siteName: "Tramitup",
    images: [{ url: "/og-image.png", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    site: "@tramitup",
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
