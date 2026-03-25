import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mi panel | TramitUp",
  description:
    "Tu centro de control legal. Ve tus plazos urgentes, expedientes activos y acciones pendientes de un vistazo.",
  robots: { index: false, follow: false },
};

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
