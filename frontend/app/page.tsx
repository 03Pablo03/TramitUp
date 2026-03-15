import { Hero } from "./landing/components/Hero";
import { ProblemSection } from "./landing/components/ProblemSection";
import { HowItWorks } from "./landing/components/HowItWorks";
import { UseCasesGrid } from "./landing/components/UseCasesGrid";
import { PricingSection } from "./landing/components/PricingSection";
import { LegalNotice } from "./landing/components/LegalNotice";
import { Footer } from "./landing/components/Footer";
import { LandingNav } from "./landing/components/LandingNav";

const faqsForSchema = [
  {
    q: "¿Tramitup es un servicio legal?",
    a: "No. Tramitup es un servicio de información jurídica. Te explicamos qué dice la normativa española vigente y te ofrecemos modelos de escritos orientativos. No prestamos asesoramiento legal ni sustituimos a un abogado.",
  },
  {
    q: "¿Cuánto cuesta usar Tramitup?",
    a: "Tramitup tiene un plan gratuito con 2 consultas al día. Puedes suscribirte a PRO por 9,99€/mes para consultas ilimitadas, documentos y alertas.",
  },
  {
    q: "¿Puedo usar Tramitup para reclamar a una aerolínea?",
    a: "Sí. Tramitup te explica el Reglamento UE 261/2004 y puede generar un modelo de reclamación personalizado.",
  },
  {
    q: "¿Los modelos de escritos son válidos?",
    a: "Los modelos son orientativos y se basan en normativa vigente. Debes revisarlos antes de presentarlos.",
  },
  {
    q: "¿Qué normativa usa Tramitup?",
    a: "Normativa española vigente: Reglamento UE 261/2004, Ley 24/2013, LAU 29/1994, RDL 2/2015, Ley 58/2003, entre otras.",
  },
];

export default function LandingPage() {
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqsForSchema.map((faq) => ({
      "@type": "Question",
      name: faq.q,
      acceptedAnswer: {
        "@type": "Answer",
        text: faq.a,
      },
    })),
  };

  const orgSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: "Tramitup",
    url: "https://tramitup.com",
    email: "soportetramitup@gmail.com",
    description: "Servicio de información jurídica para ciudadanos españoles",
    serviceType: "Información jurídica",
  };

  return (
    <div className="min-h-screen">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(orgSchema),
        }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(faqSchema),
        }}
      />
      <div className="relative min-h-screen">
        <div
          className="absolute inset-0 -z-20 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: "url(/SEO.png)" }}
        />
        <div className="absolute inset-0 -z-10 bg-gradient-to-r from-stone-900/50 via-stone-900/15 to-transparent" />
        <LandingNav />
        <Hero noBackground />
      </div>
      <main>
        <ProblemSection />
        <HowItWorks />
        <UseCasesGrid />
        <PricingSection />
        <LegalNotice />
        <Footer />
      </main>
    </div>
  );
}
