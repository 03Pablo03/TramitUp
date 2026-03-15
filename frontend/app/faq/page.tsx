import { FAQ } from "../landing/components/FAQ";
import { LandingNav } from "../landing/components/LandingNav";
import { Footer } from "../landing/components/Footer";

export const metadata = {
  title: "Preguntas Frecuentes | Tramitup",
  description: "Respuestas a las preguntas más frecuentes sobre Tramitup, el servicio de información jurídica para ciudadanos españoles.",
};

export default function FAQPage() {
  return (
    <div className="min-h-screen bg-white">
      <LandingNav />
      <main className="py-16">
        <FAQ />
      </main>
      <Footer />
    </div>
  );
}