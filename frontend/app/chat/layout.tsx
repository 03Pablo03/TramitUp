import { Suspense } from "react";

export default function ChatLayout({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-[#F9FAFB]">Cargando...</div>}>{children}</Suspense>;
}
