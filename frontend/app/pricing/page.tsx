import { Suspense } from "react";
import PricingContent from "./PricingContent";

export default function PricingPage() {
  return (
    <Suspense fallback={<div className="flex min-h-screen items-center justify-center bg-white"><div className="text-slate-500">Cargando...</div></div>}>
      <PricingContent />
    </Suspense>
  );
}
