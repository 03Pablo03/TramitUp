import { Suspense } from "react";

export default function AccountLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <Suspense fallback={<div className="flex min-h-screen items-center justify-center">Cargando...</div>}>{children}</Suspense>;
}
